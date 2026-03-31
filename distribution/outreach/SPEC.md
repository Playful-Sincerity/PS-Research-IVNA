# IVNA Academic Outreach System — Specification

*Created: 2026-03-31*

---

## Goal

Build a semi-automated system that discovers researchers working on topics adjacent to IVNA (division by zero, NSA, infinitesimals, grossone, wheel algebra, numerosity, IEEE 754 extensions), enriches their profiles, generates personalized outreach drafts across multiple channels, and manages the sending/tracking pipeline — all grounded in PSSO principles of genuine relationship-building.

---

## Design Philosophy (from PSSO Social Architecture)

These principles govern every outreach touchpoint:

1. **"Start with what they have, not what you need"** — Lead with their contribution. Every message opens by engaging with THEIR specific work before mentioning IVNA.
2. **"Attract, don't impose"** — Ask genuine questions. Invite thought. Never push.
3. **"Invite them to show their strengths"** — Ask what they see in the division-by-zero space. What gaps remain? What would make them excited about a new approach?
4. **"Specificity signals presence"** — Reference exact papers, exact results, exact quotes when possible. Generic "I admire your work" is noise.
5. **"Contribution is found, not assigned"** — Don't prescribe how they relate to IVNA. Let them discover the connection.
6. **"Care genuinely and articulate value when it is real"** — Only reach out to people whose work genuinely connects. No spray-and-pray.

**Anti-patterns to avoid:**
- Mass-email feel (cc'd, template-obvious, no specificity)
- "I made something amazing, look at it" framing
- Asking for endorsement, review, or promotion
- Following up aggressively
- Overselling — the math should speak for itself

---

## Channels

### 1. Email (Primary)
- Most researchers check email daily and respond to well-crafted messages
- Expect 10-20% response rate for personalized academic emails
- Use personal email or university email lookup
- Subject line: specific, not clickbait

### 2. ResearchGate
- Many academics have profiles; messaging is free
- Lower response rate than email but reaches people without public emails
- Good for researchers who publish but aren't on social media

### 3. LinkedIn
- Growing in academic circles, especially applied math and CS
- Connection request + note (300 char limit) → follow-up message
- Best for: engineers, CS researchers, applied mathematicians
- Less effective for: pure mathematicians, senior theorists

### 4. Twitter/X (Math Twitter)
- Public engagement: comment on their threads, share their work first
- Only DM after establishing public rapport
- Best for: researchers who actively tweet about math
- Thread format for IVNA announcement reaches people organically

### 5. MathOverflow / Math StackExchange
- Don't message directly — participate in discussions
- Ask genuine questions that naturally reference IVNA
- Researchers active here are exactly the target audience
- Builds credibility through contribution, not promotion

### 6. arXiv / Google Scholar
- No direct messaging, but profiles link to personal pages
- Use for discovery and enrichment, not outreach
- arXiv trackbacks (if IVNA cites their paper) create automatic visibility

### 7. Conference / Seminar
- Virtual seminar talks (many departments do these now)
- Conference poster sessions or contributed talks
- Most direct relationship-building but requires accepted paper

---

## Pipeline Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   DISCOVER   │───▶│   ENRICH     │───▶│    DRAFT     │───▶│  REVIEW &    │
│              │    │              │    │              │    │   SEND       │
│ Semantic     │    │ Email lookup │    │ AI-generated │    │ Wisdom       │
│ Scholar API  │    │ Affiliation  │    │ personalized │    │ reviews each │
│ arXiv API    │    │ Recent pubs  │    │ emails per   │    │ draft, edits │
│ OpenAlex API │    │ Research     │    │ channel per  │    │ and approves │
│ Web search   │    │ interests    │    │ researcher   │    │ before send  │
│              │    │ Social media │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │                    │
       ▼                   ▼                   ▼                    ▼
  researchers.json    enriched.json    drafts/<name>/         sent-log.json
                                       email.md
                                       linkedin.md
                                       researchgate.md
```

### n8n Workflow Components

**Workflow 1: Researcher Discovery** (manual trigger or scheduled)
- HTTP Request nodes → Semantic Scholar, arXiv, OpenAlex APIs
- Search by keyword: "division by zero", "nonstandard analysis", etc.
- Code node → deduplicate, score relevance, structure output
- Google Sheets / Airtable → researcher database

**Workflow 2: Profile Enrichment** (triggered per researcher)
- Input: researcher name + known affiliation
- HTTP Request → university page scraping, Google Scholar profile
- AI node (Claude/OpenAI) → extract email, summarize research focus
- Update researcher record with contact info + research summary

**Workflow 3: Draft Generation** (triggered per researcher)
- Input: enriched researcher profile
- AI node → generate personalized email using template + their specific papers
- AI node → generate LinkedIn message (short version)
- Output to drafts folder or Airtable for review

**Workflow 4: Send & Track** (manual trigger per approved draft)
- Gmail node → send personalized email
- Airtable/Sheets → log sent date, channel, status
- Wait node → schedule follow-up reminder (14 days)

---

## Research Topic Clusters for Discovery

| Cluster | Search Terms | Key Figures |
|---------|-------------|-------------|
| Grossone / Infinity Computing | grossone, Sergeyev, infinity computing, numeral system | Ya. Sergeyev, M. Margenstern |
| Numerosity Theory | numerosity, Benci, Di Nasso, Euclidean numbers | V. Benci, M. Di Nasso |
| Meadow Theory / Division by Zero | meadow algebra, Bergstra, division by zero, total division | J. Bergstra, C.A. Middelburg |
| Nonstandard Analysis Pedagogy | infinitesimal calculus, Keisler, NSA pedagogy | H.J. Keisler, K.D. Stroyan |
| Wheel Algebra | wheel algebra, Carlstrom, total reciprocal | J. Carlstrom |
| S-Extension | S-extension, algebraic structure, Santangelo | B. Santangelo |
| Transreal / Transmathematica | transreal arithmetic, Anderson, nullity | J.A.D.W. Anderson |
| IEEE 754 Extensions | IEEE 754, NaN propagation, extended arithmetic | Agner Fog, W. Kahan |
| Surreal / Hyperreal | surreal numbers, Conway, hyperreal, ultrafilter | J.H. Conway (legacy), various |
| Smooth Infinitesimal Analysis | SIA, synthetic differential geometry | J.L. Bell, A. Kock |
| Colombeau Algebras | Colombeau, generalized functions, multiplication of distributions | J.F. Colombeau |
| Divergent Series | regularization, Ramanujan summation, zeta regularization | Various |

---

## Outreach Tiers

### Tier A: Priority Researchers (personal, hand-crafted emails)
- 6 researchers from distribution strategy
- Each gets a fully personalized email + LinkedIn connection
- Reference specific papers, specific results
- Genuine questions about their perspective on IVNA's approach

### Tier B: Active Field Researchers (semi-personalized)
- 20-50 researchers discovered through API search
- Template with personalized opening paragraph (their specific work)
- Standardized middle section (what IVNA is, key result)
- Personalized closing question based on their research focus

### Tier C: Broader Network (community-style)
- 50-150 researchers in adjacent fields
- Shorter message, less personalization
- Focus on the most shareable result (5/0₁ = ∞₅, roundtrip property)
- Invitation to the GitHub repo and VEX demo
- Best suited for ResearchGate batch messages or LinkedIn

---

## Message Templates (to be personalized per researcher)

### Email — Tier A (Priority Researchers)
See outreach-templates.md for full templates

### Email — Tier B (Active Researchers)
See outreach-templates.md

### LinkedIn — Connection Request (300 char max)
See outreach-templates.md

### ResearchGate — Message
See outreach-templates.md

---

## Requirements

1. All outreach waits until ArXiv preprint is live (need citable link)
2. GitHub repo must be public with working Lean proofs + VEX demo
3. Wisdom reviews and approves every Tier A email before sending
4. Tier B emails can be batch-approved but Wisdom spot-checks 20%
5. Tier C messages go through one round of Wisdom review on the template
6. No automated sending without human approval
7. Follow-up: one polite follow-up at 14 days, then stop
8. Track all interactions in a single database
9. Log responses and update researcher profiles

---

## Verification

- [ ] Discovery finds at least 100 unique researchers across clusters
- [ ] Enrichment finds email/contact for 60%+ of discovered researchers
- [ ] Tier A drafts pass Wisdom's quality bar (specific, genuine, non-salesy)
- [ ] n8n workflow handles the full pipeline without manual JSON editing
- [ ] Follow-up scheduling works correctly
- [ ] All sent messages are logged with timestamp and channel

---

## Open Questions

1. **Airtable vs. Google Sheets** for researcher database — Airtable has better structure but Sheets is simpler to start. Decision: start with Google Sheets, migrate to Airtable if needed.
2. **Unipile for LinkedIn API** — several templates use it. Worth the cost? Or manual LinkedIn for Tier A/B?
3. **VEX web demo timeline** — should this be live before outreach starts? (Probably yes — it's the most compelling artifact.)
4. **Conference submissions** — any upcoming math conferences accepting contributed talks on algebra/analysis?
