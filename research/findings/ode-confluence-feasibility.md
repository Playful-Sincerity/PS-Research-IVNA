# ODE Confluence Feasibility Study

**Date:** 2026-03-31
**Verdict:** ABANDON strong claim — numbers match but trivially (just counting multiplications)

## Classical Results

Merging N regular singular points produces Poincaré rank N/2 (Ince 1926):

| Equation | N merged | Poincaré rank |
|----------|----------|---------------|
| Kummer/Bessel | 2 | 1 |
| Airy | 3 | 3/2 |
| Hermite | 4 | 2 |

## IVNA Encoding

Multiplying N indexed zeros: 0_{r1} · 0_{r2} · ... · 0_{rN} = 0^N_{r1·r2·...·rN}

IVNA order = N. Classical rank = N/2. Matches — but trivially.

## Why It Fails

1. **The index does no work.** Rank depends only on order (count of multiplications), not on the index. IVNA's distinctive feature is irrelevant.
2. **The encoding is non-canonical.** Each singular point has two indicial exponents. Which becomes the subscript?
3. **Half-integer ranks require post-hoc division by 2.** Not derived from IVNA axioms.
4. **Stokes phenomena invisible.** The real depth in confluence theory (monodromy, connection matrices) is discarded.
5. **Any order-additive system would do this.** Not specific to IVNA.

## Recommendation

Abandon as external theorem. At most, a one-paragraph bookkeeping observation citing Ince.
