# Recursive Indexing Closure Proof

**Date:** 2026-03-31
**Status:** PROVED (Z3 + SymPy)

## The Question

Does IVNA's index arithmetic produce infinite regress? Can indices be complex? Can indices be virtual numbers themselves?

## Answer: Index Domain Is C\{0}

The index domain naturally extends from R\{0} to **C\{0}** (nonzero complex numbers). All 11 axioms hold because C\{0} is closed under multiplication, division, and addition (mod D-INDEX-ZERO).

### Closure Proofs

| Operation | Axioms | Closure in C\{0} | Proof |
|-----------|--------|-------------------|-------|
| Multiplication (z1 * z2) | A1-A5 | Yes | \|z1\*z2\| = \|z1\|\*\|z2\| > 0 |
| Division (z1 / z2) | A6-A7 | Yes | \|z1/z2\| = \|z1\|/\|z2\| > 0 |
| Addition (z1 + z2) | A10-A11 | Yes, mod D-INDEX-ZERO | z1+z2=0 iff z2=-z1; exits to real 0 |

Z3 verification: 5/5 checks passed for real case. Complex case proved by the above norm argument (Z3 doesn't support complex natively).

### Virtual-Valued Indices: Reduce to Existing Objects

If you plug a virtual number in as an index, the NSA embedding resolves it automatically:

| Expression | NSA Expansion | Reduces To |
|-----------|---------------|------------|
| 0_{0_z} | (zε₀) · ε₀ = zε₀² | 0²_z (higher-order zero) |
| 0_{∞_z} | (z/ε₀) · ε₀ = z | Real number z (exits) |
| ∞_{0_z} | (zε₀) / ε₀ = z | Real number z (exits) |
| ∞_{∞_z} | (z/ε₀) / ε₀ = z/ε₀² | ∞²_z (higher-order infinity) |

Virtual indices aren't forbidden — they just collapse to order changes or real exits. No recursion, no new objects needed.

### What Complex Indices Buy You

- **Directional information**: 0_{e^{iθ}} represents "a zero approached from angle θ"
- **Connection to blow-ups**: Complex indices correspond to coordinates on the exceptional divisor (P¹ ≅ S¹ parametrized by angle)
- **Euler's formula in IVNA**: e^{iπ} + 1 = 0 becomes expressible with indexed zeros carrying complex phase
- **No cost**: All axioms, all verification, all Lean proofs work unchanged (Lean uses generic field F; C is a field)

## Paper Changes Needed

1. **Section 2.8 (Index Domain)**: Change "R\{0}" to "C\{0}" throughout. Add remark that virtual indices reduce to order changes.
2. **Section 4 (Consistency)**: NSA embedding extends to *C (hypercomplex numbers). Trivial extension.
3. **Lean formalization**: Already generic over any field F. No changes needed.
4. **Remove "complex indices" from Future Work** — it's now part of the framework, not future.

## Draft Paper Remark

> **Remark (Index domain).** The index domain is $\mathbb{C} \setminus \{0\}$. All axiom-induced index operations (multiplication, division, addition) preserve $\mathbb{C} \setminus \{0\}$, with the boundary case $z + (-z) = 0$ handled by D-INDEX-ZERO. Complex indices encode directional information: $0_{e^{i\theta}}$ represents a zero with approach angle $\theta$, connecting IVNA's index arithmetic to the exceptional divisor coordinates in blow-up resolution.
>
> Virtual-valued indices (e.g., $0_{0_z}$) are permitted but reduce to order changes under the NSA embedding: $0_{0_z} = z\varepsilon_0^2 = 0^2_z$. Similarly, $0_{\infty_z} = z$ exits to a real number. No recursive indexing occurs — virtual indices are syntactic sugar for the existing order hierarchy.
