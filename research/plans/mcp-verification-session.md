# MCP Verification Session — Run in CLI

The MCP tools (sympy-mcp, wolfram, wolfram-verify, mcp-solver, arxiv-latex-mcp) are configured in settings.json but only available in CLI sessions, not VS Code.

## Before Paper Finalization

Run this in a CLI session (`claude` from terminal):

### 1. Wolfram Step-by-Step Verification
Use wolfram-verify to check each key derivation chain:
- The derivative computation for x² (step by step)
- The integration of x^n (Faulhaber → order cancellation)
- The FTC proof (both directions)
- The harmonic oscillator solution
- The NSA embedding for each axiom

### 2. ArXiv LaTeX Comparison
Use arxiv-latex-mcp to pull actual equations from:
- Robinson 1966 (NSA original) — compare standard part to =;
- Keisler's Elementary Calculus — compare infinitesimal integration to IVNA
- Sergeyev's grossone papers — compare ① to ∞₁
- Carlström's wheel algebra — compare ⊥ to IVNA's product rule

### 3. SymPy MCP Symbolic Verification
Use sympy-mcp's 40+ tools for:
- Symbolic simplification of all axiom mappings
- Tensor calculations for physics applications
- Series expansion verification for A-VT

### 4. mcp-solver Extended Z3
Use mcp-solver for:
- Full axiom set satisfiability (all 11 axioms simultaneously)
- Independence checking (is each axiom independent of the others?)
- Consistency under extended axioms (A-EXP, A-VT)

## Migration Prompt

```
Here's context from a previous conversation:

**What we concluded:**
- IVNA validated: 145/148 comprehensive checks pass (0 failures, 3 framing warnings)
- Lean4 compiles (11 axioms, 12 theorems, consistency proof)
- All research complete (calculus, ODEs, complex analysis, physics, CS demos)
- Paper LaTeX scaffold ready at ~/Playful Sincerity/PS Research/IVNA/paper/ivna-paper.tex

**What I'd like to do next:**
Run MCP-based verification of all IVNA claims using the tools that weren't available in VS Code:
1. wolfram-verify for step-by-step derivation checking
2. arxiv-latex-mcp for exact equation comparison with published papers
3. sympy-mcp for symbolic verification
4. mcp-solver for extended Z3 checking

Then finalize the paper draft.

**Key files:**
- ~/Playful Sincerity/PS Research/IVNA/CLAUDE.md
- ~/Playful Sincerity/PS Research/IVNA/research/plans/mcp-verification-session.md
- ~/Playful Sincerity/PS Research/IVNA/research/findings/verification-comprehensive.txt
- ~/Playful Sincerity/PS Research/IVNA/code/verify-comprehensive.py
```
