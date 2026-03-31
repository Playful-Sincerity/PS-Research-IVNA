# IVNA — Indexed Virtual Number Algebra

## What This Is
A consistent algebraic framework that attaches indices to zeros and infinities, making division by zero and indeterminate forms algebraically operable. Proven consistent via NSA embedding (37/37 SymPy + 11/11 Z3 checks). Lean4 formalization complete (11 axioms, 12 theorems, consistency proof).

## Status
**Phase 2: Paper drafting.** Validation complete (272 total checks: 145 comprehensive + 127 MCP verification, 0 failures). Lean4 proofs compile. e exploration done. LaTeX scaffold ready. Impact/adoption/community document written. Next: fill in paper sections, then ArXiv submission.

## Key Results
- **28/28 Python tests pass** — core algebra + resolved contradictions + transcendental derivatives
- **IVNA is consistent** — NSA embedding provides concrete model
- **e = (1 + 0₁)^{∞₁}** — direct algebraic definition, not a limit
- **All standard calculus derivatives work** — polynomial, rational, trig, exponential, logarithmic
- **Division-by-zero roundtrip** — 5/0₁ = ∞₅, ∞₅ · 0₁ = 5 (information preserved)
- **IVNA is to NSA what a+bi is to R²** — the notation is the contribution

## Project Structure

```
IVNA/
├── CLAUDE.md                    # This file
├── .gitignore
│
├── paper/                       # The academic paper
│   ├── ivna-paper.tex           # LaTeX source (10-section structure)
│   └── ivna-paper.pdf           # Compiled PDF
│
├── lean-ivna/                   # Lean 4 formalization
│   ├── LeanIvna/
│   │   ├── Basic.lean           # V F inductive type
│   │   ├── Axioms.lean          # 11 IVNA axioms as structure
│   │   ├── Model.lean           # Consistency proof (GF(2) model)
│   │   └── Theorems.lean        # 12 derived theorems
│   ├── lakefile.lean
│   ├── lean-toolchain
│   └── README.md
│
├── code/                        # Python implementation & tools
│   ├── ivna.py                  # Core IVNA implementation (28 tests)
│   ├── verify_nsa_embedding.py  # NSA embedding verification (37+11 checks)
│   └── vex_calculator.py        # VEX calculator prototype/demo
│
├── research/                    # Research documents
│   ├── Indexed_Virtual_Number_Algebra.pdf  # Original paper (source)
│   ├── findings/
│   │   ├── e-exploration.md         # Deep e consequences (5 HIGH-rated)
│   │   ├── applications-physics.md  # Physics apps + L'Hôpital elimination
│   │   ├── value-assessment.md      # Final verdict + revised paper outline
│   │   ├── writing-style-guide.md   # Wisdom's voice for paper drafting
│   │   ├── impact-and-adoption.md   # Real-world impact trajectory + community vision
│   │   ├── verification-mcp-sympy.txt    # 69/69 SymPy symbolic checks
│   │   ├── verification-mcp-z3.txt       # 31/31 Z3 satisfiability checks
│   │   ├── verification-mcp-wolfram.txt  # 27/27 step-by-step derivative/FTC checks
│   │   └── verification-mcp-literature.txt # 20-source literature comparison
│   └── plans/
│       ├── plan.md                        # Phase 1 master plan (complete)
│       ├── plan-phase2.md                 # Phase 2 plan (paper + publication)
│       ├── next-steps.md                  # Development + publication roadmap
│       ├── plan-section-consistency.md    # Audit results
│       ├── plan-section-literature.md     # Literature positioning
│       ├── plan-section-contradiction-resolution.md
│       ├── plan-section-model-construction.md
│       ├── plan-section-model-verification.md
│       └── plan-section-applications.md
│
└── sessions/                    # Session logs
    └── 2026-03-31-session-validation-and-deep-plan.md
```

## Core Axioms (resolved)
- **A1-A5**: Multiplication rules (zero×zero, inf×inf, zero×inf, scalar×zero, scalar×inf)
- **A6-A9**: Division rules (by zero, by inf, zero/zero, inf/inf)
- **A10-A11**: Addition rules
- **A-EXP**: (1 + 0_x)^{∞_y} = e^{xy} — resolves the e problem
- **A-VT**: Virtual Taylor Axiom — extends analytic functions to virtual arguments
- **D-INDEX-ZERO**: Index 0 exits to real 0 (like i-i=0 exits imaginaries)

## Research Tools (available)
- **sympy-mcp** — symbolic math verification
- **mcp-solver** — Z3 satisfiability checking
- **wolfram / wolfram-verify** — computation + step-by-step verification
- **jupyter-mcp-server** — persistent computation
- **arxiv-latex-mcp** — raw LaTeX from arXiv papers
- **Lean 4** — formal proof verification (`lake build` in lean-ivna/)
- **Python venv** — `/tmp/ivna-env` (SymPy 1.14.0, Z3 4.16.0, NumPy, SciPy)
- Run tests: `source /tmp/ivna-env/bin/activate && python3 code/ivna.py`
- Compile paper: `cd paper && tectonic ivna-paper.tex`
- Build Lean: `cd lean-ivna && lake build`

## GVR Rule (Auto-Applied)
This project falls under `~/Playful Sincerity/PS Research/**`:
1. Generate reasoning from training knowledge
2. Verify with computation tools (SymPy, Wolfram, Z3) before presenting
3. Revise if verification reveals errors

## Publication Plan
- **ArXiv first** (math.RA or math.GM) — establishes priority
- **Target journal**: American Mathematical Monthly or Mathematical Intelligencer
- **Supplementary**: GitHub repo with code + Lean proofs + VEX calculator
- **Attribution**: Wisdom as sole author, Playful Sincerity Digital Core in acknowledgments

## Connection to Other PS Research
- **Gravitationalism**: IVNA notation for field singularities
- **ULP**: Both seek irreducible formal structures
- **Academic credibility**: First publication → gateway for other PS Research papers
