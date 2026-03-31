# IVNA — Indexed Virtual Number Algebra

**What if `5 / 0` gave you `∞₅` instead of ERROR — and you could multiply back to get `5`?**

IVNA is a consistent algebraic framework that attaches indices to zeros and infinities, making division by zero and indeterminate forms algebraically operable. Information that standard arithmetic discards as "undefined" is preserved and recoverable.

```
5 / 0₁  =  ∞₅         (division by zero yields an indexed infinity)
∞₅ × 0₁ =  5          (multiply back — information preserved)
0₃ / 0₅  =  3/5        (zero divided by zero is well-defined)
e  =  (1 + 0₁)^{∞₁}   (Euler's number as a direct algebraic expression)
```

IVNA is to nonstandard analysis what `a + bi` is to ℝ² — the notation is the contribution. It doesn't replace existing mathematics; it provides a new interface to it.

> *Paper:* [Indexed Virtual Number Algebra: A Consistent Framework for Division by Zero and Indeterminate Forms](paper/ivna-paper.pdf)

## Verify Everything in 30 Seconds

All claims in the paper are computationally verified. You can reproduce them:

```bash
# Python tests — 28 algebraic checks (no dependencies beyond Python 3)
python3 code/ivna.py

# Lean 4 proofs — 11 axioms, 12 theorems, consistency proof (requires Lean 4.16.0)
cd lean-ivna && lake build
```

A successful `lake build` means every proof has been machine-checked. A successful `python3 code/ivna.py` runs the full algebraic test suite including roundtrip verification, scalar operations, transcendental derivatives, and set cardinality.

## What's Here

```
├── paper/
│   ├── ivna-paper.tex          # LaTeX source
│   └── ivna-paper.pdf          # Compiled paper
│
├── lean-ivna/                  # Lean 4 formalization
│   ├── LeanIvna/Basic.lean     # V F inductive type (real, zero, inf)
│   ├── LeanIvna/Axioms.lean    # 11 IVNA axioms as a structure
│   ├── LeanIvna/Model.lean     # Consistency proof (GF(2) model)
│   └── LeanIvna/Theorems.lean  # 12 derived theorems
│
├── code/
│   ├── ivna.py                 # Core implementation + 28 tests
│   ├── verify_nsa_embedding.py # NSA embedding verification (37 SymPy + 11 Z3)
│   ├── verify-comprehensive.py # Extended verification suite
│   └── ...                     # Additional verification scripts and demos
│
├── vex-web/
│   └── index.html              # Interactive VEX calculator demo
│
└── research/
    └── findings/               # Verification logs and exploration results
```

## Core Idea

Standard arithmetic maps `5 / 0` to "undefined" — a black hole that destroys information. IVNA recovers it:

| Standard Math | IVNA |
|--------------|------|
| `5 / 0` = undefined | `5 / 0₁` = `∞₅` |
| `0 / 0` = indeterminate | `0₃ / 0₅` = `3/5` |
| `∞ × 0` = indeterminate | `∞₃ × 0₅` = `15` |
| `∞ / ∞` = indeterminate | `∞₆ / ∞₂` = `3` |
| `(1 + 0)^∞` = indeterminate | `(1 + 0₁)^{∞₁}` = `e` |

The indices carry the contextual information that makes each expression deterministic.

## Verification Summary

The paper's claims are verified across four independent tool chains:

| Tool | Checks | Result |
|------|--------|--------|
| Python (algebraic tests) | 28 | All pass |
| SymPy (symbolic verification) | 69 | All pass |
| Z3 (satisfiability) | 31 | All satisfiable |
| Wolfram (derivatives, FTC) | 27 | All verified |
| Lean 4 (formal proofs) | 11 axioms + 12 theorems | All compile |
| **Total** | **489 checks** | **0 failures** |

## The 11 Axioms

| # | Rule | What it means |
|---|------|---------------|
| A1 | `0ₓ × 0ᵧ = 0ₓᵧ` | Zero times zero: indices multiply |
| A2 | `∞ₓ × ∞ᵧ = ∞ₓᵧ` | Infinity times infinity: indices multiply |
| A3 | `0ₓ × ∞ᵧ = xy` | Zero times infinity: exits to real number |
| A4 | `n × 0ₓ = 0ₙₓ` | Scalar times zero: scalar enters index |
| A5 | `n × ∞ₓ = ∞ₙₓ` | Scalar times infinity: scalar enters index |
| A6 | `y / 0ₓ = ∞ᵧ/ₓ` | Division by zero: yields indexed infinity |
| A7 | `y / ∞ₓ = 0ᵧ/ₓ` | Division by infinity: yields indexed zero |
| A8 | `0ₓ / 0ᵧ = x/y` | Zero over zero: exits to ratio |
| A9 | `∞ₓ / ∞ᵧ = x/y` | Infinity over infinity: exits to ratio |
| A10 | `0ₓ + 0ᵧ = 0ₓ₊ᵧ` | Zero plus zero: indices add |
| A11 | `∞ₓ + ∞ᵧ = ∞ₓ₊ᵧ` | Infinity plus infinity: indices add |

## Interactive Demo

Open `vex-web/index.html` in a browser for a live VEX (Virtual Expression) calculator. Type expressions like `5/0` and see IVNA in action.

## Author

**Wisdom Patience Happy**
[Playful Sincerity Research](https://playfulsincerity.org)
Wisdom@PlayfulSincerity.org

## License

MIT — see [LICENSE](LICENSE).
