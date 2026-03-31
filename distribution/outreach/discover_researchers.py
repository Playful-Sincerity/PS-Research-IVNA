#!/usr/bin/env python3
"""
IVNA Researcher Discovery Engine

Searches Semantic Scholar and OpenAlex APIs to find researchers working on
topics adjacent to IVNA: division by zero, nonstandard analysis, infinitesimals,
grossone, wheel algebra, numerosity, IEEE 754 extensions, etc.

Outputs a structured JSON database of researchers with:
- Name, affiliation, homepage
- Key papers (title, year, citation count, venue)
- Research focus summary
- Relevance score to IVNA
- Contact info (when available)

Usage:
    python discover_researchers.py              # Full discovery
    python discover_researchers.py --cluster grossone  # Single cluster
    python discover_researchers.py --enrich     # Enrich existing database
"""

import json
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime

# ---------- Configuration ----------

OUTPUT_DIR = Path(__file__).parent
DB_FILE = OUTPUT_DIR / "researchers.json"

# Semantic Scholar API (free, no key needed, 100 req/5min)
S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "title,year,citationCount,authors,venue,externalIds,abstract"
S2_AUTHOR_FIELDS = "name,affiliations,homepage,paperCount,citationCount,hIndex"

# OpenAlex API (free, no key needed, polite pool with email)
OA_BASE = "https://api.openalex.org"
OA_EMAIL = "wisdom@playfulsincerity.org"  # For polite pool

# Rate limiting
S2_DELAY = 3.5   # seconds between Semantic Scholar requests (100 req/5min = 1 per 3s)
OA_DELAY = 0.2   # seconds between OpenAlex requests (10/sec allowed)

# ---------- Search Clusters ----------

CLUSTERS = {
    "grossone": {
        "queries": [
            "grossone infinity computing",
            "Sergeyev numeral system infinite",
            "grossone arithmetic numerical methods",
        ],
        "key_authors": ["Yaroslav Sergeyev", "Maurice Margenstern"],
    },
    "numerosity": {
        "queries": [
            "numerosity theory Benci",
            "Euclidean numbers infinite sets",
            "numerosity Benci Di Nasso",
        ],
        "key_authors": ["Vieri Benci", "Mauro Di Nasso"],
    },
    "meadows": {
        "queries": [
            "meadow algebra division by zero",
            "Bergstra division by zero",
            "total division algebra equational",
        ],
        "key_authors": ["Jan Bergstra", "C.A. Middelburg"],
    },
    "nsa_pedagogy": {
        "queries": [
            "infinitesimal calculus pedagogy",
            "nonstandard analysis teaching",
            "Keisler infinitesimal approach calculus",
        ],
        "key_authors": ["H. Jerome Keisler", "Karel Hrbacek"],
    },
    "wheel_algebra": {
        "queries": [
            "wheels division by zero Carlstrom",
            "wheel theory commutative ring reciprocal",
            "total division ring algebra zero",
        ],
        "key_authors": ["Jesper Carlstrom"],
    },
    "transreal": {
        "queries": [
            "transreal arithmetic nullity",
            "transmathematica division zero",
        ],
        "key_authors": ["James Anderson"],
    },
    "ieee754": {
        "queries": [
            "IEEE 754 NaN propagation alternatives",
            "floating point division by zero handling",
            "extended arithmetic IEEE infinity",
            "posit number system",
        ],
        "key_authors": ["Agner Fog", "John Gustafson"],
    },
    "sia": {
        "queries": [
            "smooth infinitesimal analysis",
            "synthetic differential geometry nilpotent",
            "Bell infinitesimal methods",
        ],
        "key_authors": ["John L. Bell", "Anders Kock"],
    },
    "colombeau": {
        "queries": [
            "Colombeau algebra generalized functions",
            "multiplication distributions",
        ],
        "key_authors": ["Jean-Francois Colombeau"],
    },
    "surreal_hyperreal": {
        "queries": [
            "surreal numbers algebra",
            "hyperreal number systems",
            "nonstandard analysis ultrafilter construction",
        ],
        "key_authors": [],
    },
    "divergent_series": {
        "queries": [
            "divergent series regularization algebra",
            "Ramanujan summation rigorous",
            "zeta function regularization mathematics",
        ],
        "key_authors": [],
    },
    "division_by_zero_general": {
        "queries": [
            "division by zero algebraic framework",
            "division by zero consistent algebra",
            "algebraic structure extending fields zero",
        ],
        "key_authors": ["Brendan Santangelo"],
    },
}

# ---------- API Functions ----------

def api_get(url, delay=1.0, _retries=0):
    """Make a GET request with rate limiting and error handling."""
    time.sleep(delay)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "IVNA-Discovery/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429 and _retries < 3:
            wait = 30 * (_retries + 1)
            print(f"  Rate limited (attempt {_retries + 1}/3). Waiting {wait}s...")
            time.sleep(wait)
            return api_get(url, delay, _retries + 1)
        print(f"  HTTP {e.code}: {url[:80]}...")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def search_semantic_scholar(query, limit=50):
    """Search Semantic Scholar for papers matching query."""
    encoded = urllib.parse.quote(query)
    url = f"{S2_BASE}/paper/search?query={encoded}&limit={limit}&fields={S2_FIELDS}"
    data = api_get(url, S2_DELAY)
    if data and "data" in data:
        return data["data"]
    return []


def get_s2_author(author_id):
    """Get author details from Semantic Scholar."""
    url = f"{S2_BASE}/author/{author_id}?fields={S2_AUTHOR_FIELDS}"
    return api_get(url, S2_DELAY)


def search_openalex(query, limit=50):
    """Search OpenAlex for works matching query."""
    encoded = urllib.parse.quote(query)
    url = (
        f"{OA_BASE}/works?search={encoded}&per_page={limit}"
        f"&mailto={OA_EMAIL}&sort=cited_by_count:desc"
    )
    data = api_get(url, OA_DELAY)
    if data and "results" in data:
        return data["results"]
    return []


def get_openalex_author(author_id):
    """Get author details from OpenAlex."""
    url = f"{OA_BASE}/authors/{author_id}?mailto={OA_EMAIL}"
    return api_get(url, OA_DELAY)


# ---------- Processing Functions ----------

def extract_authors_from_s2_papers(papers):
    """Extract unique authors from Semantic Scholar paper results."""
    authors = {}
    for paper in papers:
        if not paper or "authors" not in paper:
            continue
        for author in paper["authors"]:
            aid = author.get("authorId")
            if not aid:
                continue
            if aid not in authors:
                authors[aid] = {
                    "s2_id": aid,
                    "name": author.get("name", "Unknown"),
                    "papers": [],
                }
            authors[aid]["papers"].append({
                "title": paper.get("title", ""),
                "year": paper.get("year"),
                "citations": paper.get("citationCount", 0),
                "venue": paper.get("venue", ""),
                "paperId": paper.get("paperId", ""),
            })
    return authors


def _get_venue(work):
    """Safely extract venue name from OpenAlex work."""
    loc = work.get("primary_location")
    if not loc:
        return ""
    source = loc.get("source")
    if not source:
        return ""
    return source.get("display_name", "")


def extract_authors_from_openalex(works):
    """Extract unique authors from OpenAlex work results."""
    authors = {}
    for work in works:
        if not work:
            continue
        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})
            oa_id = author.get("id", "")
            if not oa_id:
                continue
            # Extract the OpenAlex ID (last part of URL)
            oa_short = oa_id.split("/")[-1] if "/" in oa_id else oa_id
            name = author.get("display_name", "Unknown")

            if oa_short not in authors:
                inst = ""
                institutions = authorship.get("institutions", [])
                if institutions:
                    inst = institutions[0].get("display_name", "")

                authors[oa_short] = {
                    "oa_id": oa_short,
                    "name": name,
                    "affiliation": inst,
                    "papers": [],
                }

            authors[oa_short]["papers"].append({
                "title": work.get("title", ""),
                "year": work.get("publication_year"),
                "citations": work.get("cited_by_count", 0),
                "venue": _get_venue(work),
                "doi": work.get("doi", ""),
            })
    return authors


def score_relevance(researcher, cluster_name):
    """Score a researcher's relevance to IVNA (0-10)."""
    score = 0
    papers = researcher.get("papers", [])

    # More papers in the cluster = more relevant
    score += min(len(papers), 5)  # up to 5 points for paper count

    # Citation count indicates influence
    total_cites = sum(p.get("citations", 0) for p in papers)
    if total_cites > 1000:
        score += 3
    elif total_cites > 100:
        score += 2
    elif total_cites > 10:
        score += 1

    # Recent papers (last 5 years) indicate active research
    recent = [p for p in papers if p.get("year") and p["year"] >= 2021]
    if recent:
        score += 2

    return min(score, 10)


def merge_researcher_records(existing, new_record):
    """Merge a new researcher record into an existing one."""
    # Merge papers (deduplicate by title similarity)
    existing_titles = {p["title"].lower().strip() for p in existing.get("papers", [])}
    for paper in new_record.get("papers", []):
        if paper["title"].lower().strip() not in existing_titles:
            existing.setdefault("papers", []).append(paper)
            existing_titles.add(paper["title"].lower().strip())

    # Update fields if new record has better data
    for field in ["affiliation", "homepage", "email", "oa_id", "s2_id"]:
        if new_record.get(field) and not existing.get(field):
            existing[field] = new_record[field]

    # Merge clusters
    existing_clusters = set(existing.get("clusters", []))
    new_clusters = set(new_record.get("clusters", []))
    existing["clusters"] = list(existing_clusters | new_clusters)

    return existing


# ---------- Main Discovery Pipeline ----------

def discover_cluster(cluster_name, cluster_config):
    """Run discovery for a single research cluster."""
    print(f"\n{'='*60}")
    print(f"Cluster: {cluster_name}")
    print(f"{'='*60}")

    all_authors = {}

    # Search Semantic Scholar
    for query in cluster_config["queries"]:
        print(f"\n  S2 search: '{query}'")
        papers = search_semantic_scholar(query, limit=40)
        print(f"    Found {len(papers)} papers")

        authors = extract_authors_from_s2_papers(papers)
        for aid, author in authors.items():
            key = author["name"].lower().strip()
            author["clusters"] = [cluster_name]
            if key in all_authors:
                all_authors[key] = merge_researcher_records(all_authors[key], author)
            else:
                all_authors[key] = author

    # Search OpenAlex
    for query in cluster_config["queries"]:
        print(f"\n  OA search: '{query}'")
        works = search_openalex(query, limit=40)
        print(f"    Found {len(works)} works")

        authors = extract_authors_from_openalex(works)
        for oa_id, author in authors.items():
            key = author["name"].lower().strip()
            author["clusters"] = [cluster_name]
            if key in all_authors:
                all_authors[key] = merge_researcher_records(all_authors[key], author)
            else:
                all_authors[key] = author

    # Score relevance
    for key, author in all_authors.items():
        author["relevance_score"] = score_relevance(author, cluster_name)

    # Mark key authors
    key_names = {n.lower() for n in cluster_config.get("key_authors", [])}
    for key, author in all_authors.items():
        if any(kn in key for kn in key_names):
            author["priority"] = True
            author["relevance_score"] = 10  # Key authors always max

    print(f"\n  Total unique authors: {len(all_authors)}")
    top = sorted(all_authors.values(), key=lambda a: a["relevance_score"], reverse=True)[:5]
    for a in top:
        print(f"    - {a['name']} (score: {a['relevance_score']}, papers: {len(a.get('papers', []))})")

    return all_authors


def run_full_discovery(clusters_to_run=None):
    """Run discovery across all clusters and merge results."""
    if clusters_to_run is None:
        clusters_to_run = list(CLUSTERS.keys())

    # Load existing database
    if DB_FILE.exists():
        with open(DB_FILE) as f:
            db = json.load(f)
        print(f"Loaded existing database: {len(db['researchers'])} researchers")
    else:
        db = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": None,
                "total_researchers": 0,
                "clusters_searched": [],
            },
            "researchers": {},
        }

    # Run discovery for each cluster
    for cluster_name in clusters_to_run:
        if cluster_name not in CLUSTERS:
            print(f"Unknown cluster: {cluster_name}")
            continue

        authors = discover_cluster(cluster_name, CLUSTERS[cluster_name])

        # Merge into main database
        for key, author in authors.items():
            if key in db["researchers"]:
                db["researchers"][key] = merge_researcher_records(
                    db["researchers"][key], author
                )
            else:
                db["researchers"][key] = author

        if cluster_name not in db["metadata"]["clusters_searched"]:
            db["metadata"]["clusters_searched"].append(cluster_name)

    # Update metadata
    db["metadata"]["last_updated"] = datetime.now().isoformat()
    db["metadata"]["total_researchers"] = len(db["researchers"])

    # Sort by relevance and add tier
    for key, r in db["researchers"].items():
        score = r.get("relevance_score", 0)
        if r.get("priority"):
            r["tier"] = "A"
        elif score >= 7:
            r["tier"] = "B"
        else:
            r["tier"] = "C"

    # Save
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    # Summary
    tiers = {"A": 0, "B": 0, "C": 0}
    for r in db["researchers"].values():
        tiers[r.get("tier", "C")] += 1

    print(f"\n{'='*60}")
    print(f"DISCOVERY COMPLETE")
    print(f"{'='*60}")
    print(f"Total researchers: {db['metadata']['total_researchers']}")
    print(f"Tier A (priority): {tiers['A']}")
    print(f"Tier B (active):   {tiers['B']}")
    print(f"Tier C (broader):  {tiers['C']}")
    print(f"Saved to: {DB_FILE}")

    return db


def print_summary(db):
    """Print a human-readable summary of the database."""
    researchers = db["researchers"]
    sorted_r = sorted(
        researchers.values(),
        key=lambda r: ({"A": 0, "B": 1, "C": 2}.get(r.get("tier", "C"), 3), -r.get("relevance_score", 0)),
    )

    print(f"\n{'='*60}")
    print(f"RESEARCHER DATABASE SUMMARY")
    print(f"{'='*60}")

    current_tier = None
    for r in sorted_r:
        tier = r.get("tier", "C")
        if tier != current_tier:
            current_tier = tier
            print(f"\n--- Tier {tier} ---")

        clusters = ", ".join(r.get("clusters", []))
        n_papers = len(r.get("papers", []))
        affil = r.get("affiliation", "")
        print(f"  {r['name']:<30} | score: {r.get('relevance_score', 0):>2} | papers: {n_papers:>3} | {affil[:30]} | [{clusters}]")


# ---------- CLI ----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IVNA Researcher Discovery Engine")
    parser.add_argument("--cluster", help="Search a single cluster (e.g., 'grossone')")
    parser.add_argument("--summary", action="store_true", help="Print summary of existing database")
    parser.add_argument("--enrich", action="store_true", help="Enrich existing researcher profiles")
    parser.add_argument("--list-clusters", action="store_true", help="List available clusters")
    args = parser.parse_args()

    if args.list_clusters:
        print("Available clusters:")
        for name, config in CLUSTERS.items():
            print(f"  {name:<25} queries: {len(config['queries'])}, key authors: {len(config.get('key_authors', []))}")
    elif args.summary:
        if DB_FILE.exists():
            with open(DB_FILE) as f:
                db = json.load(f)
            print_summary(db)
        else:
            print("No database found. Run discovery first.")
    elif args.cluster:
        db = run_full_discovery([args.cluster])
        print_summary(db)
    else:
        db = run_full_discovery()
        print_summary(db)
