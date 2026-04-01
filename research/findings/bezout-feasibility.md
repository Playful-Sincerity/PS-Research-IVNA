# Bezout Index Conservation — Feasibility Check

**Date:** 2026-03-31
**Verdict:** ABANDON — definitionally equivalent to Bezout, no new mathematical content

## The Problem

The candidate theorem: represent intersection multiplicities as indexed zeros, then Bezout's theorem becomes an IVNA identity.

## Critical Issue: Sum vs Product

Bezout says **Sigma m_i = d1*d2** (sum), not product. The additive IVNA encoding via A10 gives: Sigma 0_{m_i} = 0_{Sigma m_i} = 0_{d1*d2}. This is Bezout with a subscript wrapper. A referee would write: "The author has relabeled m_i as the index of an indexed zero. No new mathematical content is present."

## Concrete Examples (all hold trivially)

| Curves | Degrees | Intersections | Bezout | IVNA |
|--------|---------|--------------|--------|------|
| Line y=x, circle x^2+y^2=1 | 1,2 | 2 pts, m=1 each | 1+1=2 | 0_1+0_1=0_2 |
| Parabola y=x^2, line y=1 | 2,1 | 2 pts, m=1 each | 1+1=2 | 0_1+0_1=0_2 |
| Two conics | 2,2 | 4 pts, m=1 each | 4=4 | 0_1+0_1+0_1+0_1=0_4 |
| Parabola y=x^2, tangent y=0 | 2,1 | 1 pt, m=2 | 2=2 | 0_2=0_2 |

## Key Discovery: McKean (2021)

Stephen McKean, "An arithmetic enrichment of Bezout's Theorem," *Mathematische Annalen* 379 (2021), pp. 633-660. arXiv:2003.07413.

McKean assigns each intersection point an element of the Grothendieck-Witt group GW(k) — a quadratic form over the base field — rather than an integer multiplicity. This works over non-algebraically closed fields. IVNA's approach (index = integer multiplicity) is structurally weaker.

## Assessment

| Question | Answer |
|----------|--------|
| Is the IVNA Bezout statement true? | Yes |
| Is it non-trivial? | No — definitionally equivalent |
| Does it require IVNA? | No |
| Referee risk | Fatal: "just Bezout restated in notation" |

## Recommendation

Abandon. Bezout's multiplicities are well-defined integers, not indeterminate forms. There is no "0/0 problem" in Bezout for IVNA to solve. IVNA's strength is resolving INDETERMINATE forms — look for theorems where 0/0 or infinity-infinity actually arises and standard math struggles.
