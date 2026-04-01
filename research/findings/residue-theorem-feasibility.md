# Residue Extraction Theorem Feasibility

**Date:** 2026-03-31
**Verdict:** MODIFY — include as application section, not standalone theorem

## Basic Claim: Residue = IVNA Index at Simple Poles

For R(z) = P(z)/Q(z) with simple pole at z = a:
- Q(a) = 0_{Q'(a)} in IVNA
- R(a) = P(a) / 0_{Q'(a)} = ∞_{P(a)/Q'(a)}
- The IVNA index P(a)/Q'(a) IS the residue Res(R, a)

### Verification (all confirmed analytically)

| Function | Poles | IVNA index | Standard residue | Match |
|---|---|---|---|---|
| 1/(z-1) | z=1 | 1 | 1 | YES |
| 1/(z²-1) | z=±1 | ±1/2 | ±1/2 | YES |
| (z+1)/(z²+1) | z=±i | (1∓i)/2 | (1∓i)/2 | YES (complex indices) |
| 1/(z³-1) | z=1,ω,ω² | 1/3, ω/3, ω²/3 | same | YES; residues sum to 0 by D-INDEX-ZERO |
| z/(z-1)² | z=1 (double) | ∞²₁ + ∞₁ | residue = 1 | YES but needs A-VT expansion |

## Assessment

**Is the basic claim trivial?** Yes for simple poles — it IS the standard formula P(a)/Q'(a) restated.

**Where IVNA adds value:**

1. **Partial fractions via one division per pole**: The partial fraction coefficients are IVNA indices, readable by one application of the division rule at each pole. No linear system, no polynomial long division.

2. **Residue sum = D-INDEX-ZERO**: For 1/(z³-1), residues 1/3 + ω/3 + ω²/3 = (1+ω+ω²)/3 = 0/3 → real 0 by D-INDEX-ZERO.

3. **Double poles via A-VT**: IVNA produces the full principal part as a sum of indexed infinities at different orders.

4. **Generating functions**: IVNA index at dominant pole gives Binet-type asymptotic coefficient.

## Proposed Theorem for Paper

> **Proposition (Partial Fraction Algebraic Derivability):** Let R(z) = P(z)/Q(z) be proper with Q having distinct simple roots a₁,...,aₙ. Then R(z) = Σ idx(R(aₖ))/(z − aₖ), where idx(R(aₖ)) is the IVNA index of R(aₖ). These indices are computed by one application of the IVNA division rule at each pole, with no limit computation or equation-solving.

## Recommendation

Include as application section framed as: "The same division rule that computes real derivatives also computes complex residues and partial fraction coefficients, because the index domain is C\{0}." This is the UNIFICATION argument — the strongest case for IVNA's value.
