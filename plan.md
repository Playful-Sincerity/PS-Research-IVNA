# IVNA Phase 3: From Framework to Contribution

## Environment Health
**CLEAN** — Git repo synced, all verification passes (489/489), Lean builds, paper compiles.

## Assumptions
- Open-ended timeline — quality over speed
- Actively seeking mathematician collaborator
- Hold ArXiv submission until external theorem + blow-up engagement are in the paper
- No endorser yet — use development time to find one (collaborator may solve both problems)

## Goal
Transform IVNA from "interesting framework with verified computations" into "significant mathematical contribution worthy of academic adoption." The debate identified three gaps: (1) no external theorem, (2) no blow-up engagement, (3) axiom system not characterized as a named algebraic object. Closing these gaps — plus finding a collaborator — makes the paper defensible at a serious venue.

## Cross-Cutting Concerns

- **Verification standard**: Every new mathematical claim gets GVR treatment (generate, verify with SymPy/Z3/Lean, revise)
- **Lean formalization**: New theorems should be formalized in Lean 4 where feasible — this is IVNA's credibility differentiator
- **Paper integration**: Each section's output must be writable as a paper section or subsection
- **Collaborator compatibility**: All work should be documented clearly enough that a mathematician joining mid-stream can understand the full state
- **Notation**: IVNA notation throughout (0_x, ∞_x, =;), VEA for computer arithmetic mode

## Meta-Plan

### Sections

1. **Algebraic Characterization** — Determine exactly what algebraic object IVNA is
   - Complexity: L
   - Risk: Medium — the answer might reveal IVNA is trivially isomorphic to something known
   - Acceptance criteria:
     - IVNA is characterized as a named or novel algebraic structure (e.g., graded ring, Laurent monoid, colored extension)
     - The characterization is proven in Lean 4 or SymPy
     - The paper's Section 4 (Consistency) is updated with the characterization
     - The "isomorphism question" in Section 9.2 has a definitive answer

2. **Blow-Up Engagement** — Establish the precise relationship between IVNA and blow-up resolution
   - Complexity: M
   - Risk: High — if IVNA is literally a subset of blow-up theory, the contribution claim weakens
   - Acceptance criteria:
     - A formal statement of what IVNA shares with blow-ups and what it doesn't
     - At least one concrete example where IVNA's arithmetic closure provides something blow-ups don't (e.g., discrete/computational setting)
     - Paper literature section updated with blow-up comparison (1-2 paragraphs)

3. **External Theorem** — Prove at least one theorem about an established mathematical domain using IVNA
   - Complexity: L
   - Risk: High — this is the hardest and most important section
   - Acceptance criteria:
     - One theorem stated precisely, proved rigorously, and verified computationally
     - The theorem is about something outside IVNA (not just "IVNA is consistent")
     - The theorem cannot be trivially restated without IVNA's index structure
     - Lean 4 formalization of the theorem (or clear explanation of why it's out of Lean scope)

4. **Recursive Indexing Closure** — Prove that IVNA's index arithmetic doesn't produce infinite regress
   - Complexity: S
   - Risk: Low — the paper already restricts indices to R\{0}, just needs explicit statement
   - Acceptance criteria:
     - Explicit proof that all IVNA operations on virtual numbers produce real-valued indices
     - The index domain R\{0} is closed under all axiom-induced index operations
     - One paragraph added to paper Section 2.8 (Index Domain)

5. **Collaborator Search** — Find and engage a mathematician willing to review/co-author
   - Complexity: M
   - Risk: Medium — dependent on external people
   - Acceptance criteria:
     - At least 5 targeted outreach emails sent to researchers in relevant fields
     - At least 1 substantive technical exchange with a mathematician
     - Clear decision on whether collaboration or acknowledgment is the path

6. **Paper Revision** — Integrate all findings into the paper
   - Complexity: M
   - Risk: Low — straightforward once content exists
   - Acceptance criteria:
     - Blow-up comparison in literature section
     - External theorem as new section or expanded application
     - Algebraic characterization in consistency section
     - Recursive indexing closure in index domain section
     - All new claims verified (target: 550+ total checks)
     - Paper compiles clean, no undefined references

### Dependency Graph
```
Section 1 (Algebraic Characterization) → Section 3 (External Theorem)
  The characterization determines which theorem candidates are viable.

Section 2 (Blow-Up Engagement) → Section 6 (Paper Revision)
  Literature positioning needs blow-up comparison before paper update.

Section 4 (Recursive Indexing) can run in parallel with everything.

Section 5 (Collaborator Search) can run in parallel with everything.
  Ideally starts early — a collaborator's input shapes Sections 1-3.

Section 6 (Paper Revision) depends on Sections 1, 2, 3, 4.

Execution order:
  Phase A (parallel): Sections 1, 2, 4, 5
  Phase B (sequential): Section 3 (needs Section 1)
  Phase C: Section 6 (needs all others)
```

### External Theorem Candidates — Round 1 Results

**Bezout Index Conservation: ABANDONED.** Trivially definitional — just Bezout with subscripts. McKean (2021) already did the real enrichment via Grothendieck-Witt groups.

**ODE Confluence: ABANDONED.** Numbers match but trivially — IVNA just counts multiplications. The index (IVNA's distinctive feature) does no work. Poincaré rank = N/2 is Ince (1926).

**Key lesson:** The index must be load-bearing. Both failures occurred because only the ORDER mattered, not the INDEX. The external theorem must exploit IVNA's continuous parameterization.

### External Theorem Candidates — Round 2 (In Progress)

**Primary: Blow-Up Correspondence Theorem (Algebraic Geometry)**
"IVNA's index-division axiom computes the same local data as the exceptional divisor coordinate of a blow-up at a singular point." This is genuinely new — no prior framework has made this connection. The INDEX is the exceptional divisor coordinate, so it's load-bearing. Complex indices (C\{0}) strengthen the connection. Agent developing rigorous proof.

**Secondary: Residue Extraction (Complex Analysis)**
For simple poles, IVNA index = residue. Question: can this extend to partial fractions, double poles, generating function asymptotics? Agent testing.

**Tertiary: IEEE 754 Cancellation Tracking (Numerical Analysis)**
IVNA tracks WHICH value was lost, not just THAT cancellation occurred. Compare with interval arithmetic, Higham bounds. Agent testing.

### Other Developments

**Index domain extended to C\{0}** — complex indices encode directional information, connecting to blow-up exceptional divisor coordinates. Virtual indices reduce to order changes (no recursion). This is a genuine upgrade to the framework.

**Algebraic characterization complete** — IVNA ≅ K* × Z (unit group of Laurent polynomial ring). Known structure, novel interpretation + product rule. No prior framework combines wheel-like division-by-zero with continuous parameterization.

## Execution Plan

### Session 1: Algebraic Characterization + Recursive Indexing (can start now)

**Section 1 — What algebraic object is IVNA?**

The NSA embedding already tells us: 0_x = xε₀, ∞_x = x/ε₀. So IVNA lives inside the Laurent polynomial ring R[ε₀, ε₀⁻¹], restricted to monomials. The question is: what structure does that restriction inherit?

Tasks:
1. **Literature deep-dive** — Research agent: search for "graded monoid," "Laurent monoid," "filtered ring," "colored algebra" in the context of infinitesimal arithmetic. Is IVNA isomorphic to a known named structure? Check Bourbaki's algebra volumes, nLab.
2. **Characterize the index algebra** — The indices form a structure under the axiom-induced operations. Map out: what binary operations exist on indices? (Multiplication from A1-A5, addition from A10-A11, division from A6-A9.) What are the closure properties? Is the index algebra just (R\{0}, ×, +)?
3. **Formal statement** — Write the characterization as a precise mathematical definition. "IVNA is isomorphic to the Z-graded monoid of Laurent monomials over R\{0}, with grading by ε₀-order."
4. **Verify in SymPy** — Prove the isomorphism computationally: every IVNA axiom corresponds to a Laurent monomial identity.
5. **Lean formalization** — If feasible, encode the isomorphism in Lean 4 (new file: LeanIvna/Characterization.lean).
6. **Answer the isomorphism question** — Is IVNA "just" Laurent monomials with new notation? If yes, the paper must own this honestly (like a+bi is "just" R² with a multiplication rule). If no, document what's genuinely new.

Deliverables: research/findings/algebraic-characterization.md, updated Lean files, draft paper paragraph.

**Section 4 — Recursive Indexing Closure (quick task, same session)**

Tasks:
1. Enumerate all 11 axioms and list the index operation each induces
2. Prove each operation maps R\{0} → R\{0} (or R\{0} → R, in the case of A3/A8/A9 which exit to reals)
3. Prove no axiom produces a virtual-valued index
4. Write one paragraph + one lemma for the paper
5. Verify in Z3: "for all x,y in R\{0}, [each index operation] produces a value in R\{0}"

Deliverables: paper paragraph, Z3 verification script, plan update.

---

### Session 2: Blow-Up Engagement

**Section 2 — Map the blow-up relationship**

Tasks:
1. **Read primary sources** — Research agent: fetch Hironaka's resolution theorem overview, Atiyah's blow-up construction, a modern algebraic geometry textbook treatment. Focus on: how does the exceptional divisor parametrize approach directions?
2. **Construct the formal correspondence** — For a 2-variable rational function f(x,y)/g(x,y) with a mutual zero at origin:
   - Blow-up: replace (0,0) with P¹, each point on P¹ = a ratio y/x = slope
   - IVNA: 0_{f(x,y)} / 0_{g(x,y)} = f-index / g-index, which encodes the ratio
   - State precisely: IVNA indices at a point = coordinates on the exceptional divisor of the blow-up at that point
3. **Find the separation** — Where does IVNA do something blow-ups don't?
   - Blow-ups are geometric (need scheme theory, coordinate charts)
   - IVNA is arithmetic (closed-form computation, works in discrete settings)
   - Test case: compute something in IVNA that would require a full blow-up construction in algebraic geometry. Candidate: classify singularity type of a rational function at a pole using only index arithmetic.
4. **Write the comparison** — 1-2 paragraphs for the literature section. Honest framing: "IVNA's indexed infinities are an arithmetic analog of blow-up resolution. The exceptional divisor parametrizes approach directions geometrically; IVNA indices encode the same information arithmetically. IVNA adds computational closure: arithmetic on resolved objects without ambient geometric machinery."
5. **Verify the correspondence** — SymPy: for 3-4 concrete rational functions, show IVNA indices match blow-up exceptional divisor coordinates.

Deliverables: research/findings/blow-up-comparison.md, paper paragraphs, verification script.

---

### Session 3: External Theorem — Exploration

**Section 3, Part 1 — Test the candidates**

Don't commit to one theorem yet. Instead, run parallel feasibility checks:

Tasks:
1. **Bezout feasibility** — SymPy: For specific curve pairs (line+conic, two conics, cubic+line), compute intersection multiplicities, encode as indexed zeros, verify Π 0_{mᵢ} = 0^n_{d₁d₂}. Does the identity hold for all configuration types? Where does it break (if anywhere)?
2. **ODE confluence feasibility** — SymPy/Wolfram: Take the hypergeometric equation, merge two regular singular points, compute the Poincaré rank of the result. Does the IVNA index product of the colliding indicial exponents equal the rank? Test 3-4 specific confluences (Bessel, Airy, Hermite arise from specific confluences).
3. **Evaluate results** — Which candidate produced a clean, verifiable result? Which felt like "mere rephrasing" vs. genuine mathematical content?
4. **Select the winner** — Pick the candidate that (a) is true, (b) is non-trivial, (c) can't be trivially stated without IVNA.

Deliverables: feasibility results in research/findings/, candidate selection documented in plan.md.

---

### Session 4: External Theorem — Proof

**Section 3, Part 2 — Rigorous proof of the selected theorem**

Tasks:
1. **State the theorem precisely** — LaTeX-ready statement with all quantifiers, hypotheses, and notation defined
2. **Write the proof** — Full rigorous proof, step by step
3. **Verify computationally** — SymPy + Z3: verify the theorem for a large class of instances (target: 50+ new checks)
4. **Lean formalization** — If the theorem is about finite algebraic structures, encode in Lean 4. If it involves analysis (limits, convergence), document why Lean formalization is out of scope and rely on computational verification.
5. **Write the "why IVNA is needed" argument** — Explicitly show what the theorem looks like without IVNA (clumsy, requires external bookkeeping) vs. with IVNA (clean algebraic statement). This is what makes it an "external theorem" rather than a "rephrasing."
6. **Draft paper section** — Write the theorem + proof as a self-contained paper section (2-3 pages)

Deliverables: theorem statement, proof, verification scripts, Lean files (if feasible), draft paper section.

---

### Session 5: Collaborator Outreach

**Section 5 — Find a mathematician**

This is partly Wisdom's task (sending emails, building relationships) but we can prepare everything:

Tasks:
1. **Refine target list** — From the existing outreach/researcher-targets.md, identify 5 researchers whose work most closely touches IVNA:
   - Someone in wheels/meadows/division algebras (Bergstra?)
   - Someone in blow-ups/singularity resolution
   - Someone in numerical analysis / IEEE 754
   - Someone in Lean 4 formalization community
   - Someone in math education (AMM audience)
2. **Draft personalized emails** — Each email:
   - Opens with genuine engagement with their specific work
   - States IVNA's core idea in 2 sentences
   - Links to the GitHub repo (all verification is public)
   - Asks a specific technical question about their area (not "what do you think of IVNA?")
   - Explicitly offers co-authorship if they want to engage deeply
3. **Prepare a 2-page technical summary** — Not the full paper, but a concise document a busy mathematician could evaluate in 15 minutes: core axioms, NSA embedding, one application, the external theorem result, the open question.
4. **Bluesky/Mathstodon presence** — Draft 3-5 posts about IVNA for academic social media. Focus on the puzzle ("what if 0/0 gave you a ratio instead of undefined?") not the framework. Build visibility before cold-emailing.

Deliverables: outreach/emails-v2/, research/2-page-summary.pdf, social media drafts.

---

### Session 6: Paper Revision & Final Verification

**Section 6 — Integrate everything**

Tasks:
1. **Add blow-up comparison** to Section 7 (Literature Positioning) — 1-2 paragraphs
2. **Add external theorem** as new Section 5.7 or expanded Section 5/6
3. **Update algebraic characterization** in Section 4 (Consistency) — state what IVNA is
4. **Add recursive indexing closure** to Section 2.8 (Index Domain) — 1 paragraph
5. **Update verification table** — add new checks, update total count
6. **Update abstract** — mention external theorem
7. **Update Future Work** — remove items now completed, add new items discovered
8. **Full re-verification** — run all scripts, rebuild Lean, recompile paper
9. **Final debate test** — re-run the adversarial debate with the updated paper. Does CON still win?

Deliverables: updated ivna-paper.tex, recompiled PDF, verification logs, debate re-run.

---

## Timeline Estimate (not a commitment)

| Session | Content | Can do in one sitting? |
|---------|---------|----------------------|
| 1 | Algebraic characterization + recursive indexing | Yes |
| 2 | Blow-up engagement | Yes |
| 3 | External theorem exploration | Yes |
| 4 | External theorem proof | Maybe (depends on difficulty) |
| 5 | Collaborator outreach prep | Yes |
| 6 | Paper revision + final verification | Yes, if inputs are ready |

Sessions 1-2 can happen in any order. Session 3 should follow Session 1 (characterization informs theorem choice). Session 5 can happen anytime. Session 6 is last.

---

### Overall Success Criteria

The paper is ready for submission when:
1. At least one external theorem is proved, verified, and Lean-formalized
2. The blow-up relationship is stated precisely
3. IVNA is characterized as a named algebraic structure
4. A mathematician has reviewed the paper (collaborator or independent reviewer)
5. Total verification checks ≥ 550 with 0 failures
6. The paper can survive the debate's CON arguments point-by-point
