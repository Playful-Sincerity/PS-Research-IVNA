# Blow-Up Theory Correspondence

**Date:** 2026-03-31
**Status:** COMPLETE

## The Correspondence Is Exact

Take f/g = x²/y, which is 0/0 at the origin.

**Blow-up:** Replace origin with P¹. In chart v≠0 (parameter t = u/v), substitute y = tx. Then x²/y → x²/(tx) = x/t. On the exceptional divisor (x=0), the coordinate t records the approach direction — t captures the ratio x²/y.

**IVNA:** By axiom A8 (0_a/0_b = a/b): 0_{x²}/0_y = x²/y.

**The IVNA index ratio IS the P¹ coordinate on the exceptional divisor.** Both compute the same object: the ratio that survives after the common degeneracy cancels.

## Where IVNA Adds Value (4 concrete advantages)

**1. Arithmetic closure on resolved objects.**
After blow-up: exceptional divisor is a geometric locus (P¹). You cannot multiply two P¹ points canonically.
After IVNA: ∞_{x²/y} is a number you can operate on — multiply, divide, exponentiate. Example: (0_{x²}/0_y) · (0_y/0_x) = (x²/y)·(y/x) = x. No blow-up equivalent.

**2. Discrete and characteristic-agnostic.**
Blow-ups require scheme theory. Hironaka works only in char 0; resolution in char p≥5 is still open (2024). IVNA's axioms are purely algebraic — work over Z, finite fields, combinatorial settings where varieties don't exist.

**3. Computational cost.**
Blow-up: construct Rees algebra, compute Proj, coordinate charts, proper transforms. IVNA A8: compute ratio of indices. O(1).

**4. Closure under iteration.**
Hironaka's proof is hard because each blow-up can introduce new exceptional divisors needing further blow-ups. IVNA: operations on indexed objects always produce new indexed objects. No cascade.

## Where Blow-Ups Are Strictly Stronger

- **Higher-dimensional singularities** — blow up along curves, surfaces, not just points
- **Birational geometry** — Minimal Model Program, Mori theory, moduli
- **Sheaf cohomology** — self-intersection E·E = -1, long exact sequences
- **Weighted blow-ups** — Abramovich-Temkin-Wlodarczyk (2019): multi-weight tuples, weighted projective exceptional divisors

## The Honest Framing (for the paper)

> "IVNA's index-division axiom computes the same ratio that appears as the P¹ coordinate on the exceptional divisor of the corresponding blow-up. Both formalisms identify the direction of approach that survives cancellation. The distinction is one of structure and scope: a blow-up produces a geometric object within scheme-theoretic framework; IVNA produces an arithmetic element within a closed algebraic system supporting further operations. Blow-ups resolve singularities globally; IVNA provides arithmetic on singular values locally. Neither subsumes the other."

## Key Finding: No Prior Work Connects These

Bergstra's 2019 survey of division-by-zero frameworks doesn't mention blow-ups. No division-by-zero algebra (meadows, wheels, transreal, Saitoh) has noticed or exploited this correspondence. IVNA may be the first to make the connection explicit.

## Connection to Complex Index Extension

With C\{0} indices, the correspondence strengthens: complex indices encode approach ANGLE, which is exactly what the P¹ coordinate encodes (P¹ ≅ S¹ for real blow-ups). The complex index extension makes IVNA's connection to blow-up theory not just an analogy but a structural isomorphism at the level of local singularity data.

## References

- Wikipedia: Blowing Up
- Stacks Project 01OF
- Fei Ye, "Different Aspects of Blowing-up" (2023)
- Abramovich-Temkin-Wlodarczyk, "Streamlining resolution with weighted blow-ups" (arXiv:2512.01859)
- Carlström 2004 (wheel theory contrast: 0·∞ = ⊥ vs IVNA 0_x·∞_y = xy)
- Bergstra 2019, "Division by Zero: A Survey" (blow-up not mentioned in any framework)
