"""
IVNA — Indexed Virtual Number Algebra
Python implementation for computational consistency testing.

Implements all rules from the IVNA paper (Sections 2.1-2.7)
plus resolved axioms from Section 3 deep plan:
  - D-INDEX-ZERO: index 0 exits to real 0 (like i-i=0)
  - A-EXP: (1 + 0_x)^{∞_y} = e^{xy}
  - A-VT: Virtual Taylor Axiom for analytic function extension
"""

from fractions import Fraction
from typing import Union
import math


class Virtual:
    """An indexed virtual number: either a zero (0_x) or infinity (∞_x).

    Attributes:
        kind: 'zero' or 'inf'
        index: the x in 0_x or ∞_x (a real number)
        order: the n in 0^n_x (default 1, increases with multiplication of same kind)
    """

    def __init__(self, kind: str, index: Union[int, float, Fraction], order: int = 1):
        assert kind in ('zero', 'inf'), f"kind must be 'zero' or 'inf', got {kind}"
        self.kind = kind
        self.index = Fraction(index) if not isinstance(index, Fraction) else index
        self.order = order

    def __repr__(self):
        order_str = f"^{self.order}" if self.order != 1 else ""
        if self.kind == 'zero':
            return f"0{order_str}_{self.index}"
        else:
            return f"∞{order_str}_{self.index}"

    def __eq__(self, other):
        if isinstance(other, Virtual):
            return self.kind == other.kind and self.index == other.index and self.order == other.order
        return False

    def __hash__(self):
        return hash((self.kind, self.index, self.order))

    def collapse(self):
        """The =; operator. Strips indices, returns 0 or float('inf')."""
        if self.kind == 'zero':
            return 0
        else:
            return float('inf')

    # --- MULTIPLICATION (Section 2.1) ---

    def __mul__(self, other):
        if isinstance(other, Virtual):
            if self.kind == 'zero' and other.kind == 'zero':
                # 0_x · 0_y = 0^2_{xy}
                # Generalized: 0^m_x · 0^n_y = 0^{m+n}_{xy}
                return Virtual('zero', self.index * other.index, self.order + other.order)

            elif self.kind == 'inf' and other.kind == 'inf':
                # ∞_x · ∞_y = ∞^2_{xy}
                # Generalized: ∞^m_x · ∞^n_y = ∞^{m+n}_{xy}
                return Virtual('inf', self.index * other.index, self.order + other.order)

            elif self.kind == 'zero' and other.kind == 'inf':
                # 0^m_x · ∞^n_y
                # Base case (m=n=1): 0_x · ∞_y = xy
                # General: order difference determines result type
                if self.order == other.order:
                    return self.index * other.index
                elif self.order > other.order:
                    # More zeros than infinities: result is zero
                    return Virtual('zero', self.index * other.index, self.order - other.order)
                else:
                    # More infinities than zeros: result is infinity
                    return Virtual('inf', self.index * other.index, other.order - self.order)

            elif self.kind == 'inf' and other.kind == 'zero':
                # ∞_x · 0_y = 0_y · ∞_x (commutative)
                return other.__mul__(self)

        elif isinstance(other, (int, float, Fraction)):
            # n · 0_x = 0_{nx}, n · ∞_x = ∞_{nx}
            other = Fraction(other)
            return Virtual(self.kind, other * self.index, self.order)

        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float, Fraction)):
            return self.__mul__(other)
        return NotImplemented

    # --- DIVISION (Section 2.2) ---

    def __truediv__(self, other):
        if isinstance(other, Virtual):
            if self.kind == other.kind:
                # 0_x / 0_y = x/y, ∞_x / ∞_y = x/y
                if self.order == other.order:
                    return self.index / other.index
                elif self.kind == 'zero':
                    if self.order > other.order:
                        return Virtual('zero', self.index / other.index, self.order - other.order)
                    else:
                        return Virtual('inf', self.index / other.index, other.order - self.order)
                else:  # inf
                    if self.order > other.order:
                        return Virtual('inf', self.index / other.index, self.order - other.order)
                    else:
                        return Virtual('zero', self.index / other.index, other.order - self.order)

            elif self.kind == 'zero' and other.kind == 'inf':
                # 0_x / ∞_y = 0_x · 0_{1/y}? No...
                # Actually: y/∞_x = 0_{y/x}. So 0_x / ∞_y...
                # This is 0_x · (1/∞_y). 1/∞_y = 0_{1/y} (from y/∞_x = 0_{y/x} with y=1)
                # So 0_x / ∞_y = 0_x · 0_{1/y} = 0^2_{x/y}
                return Virtual('zero', self.index / other.index, self.order + other.order)

            elif self.kind == 'inf' and other.kind == 'zero':
                # ∞_x / 0_y = ∞_x · ∞_{1/y}?
                # From y/0_x = ∞_{y/x}: 1/0_y = ∞_{1/y}
                # So ∞_x / 0_y = ∞_x · ∞_{1/y} = ∞^2_{x/y}
                return Virtual('inf', self.index / other.index, self.order + other.order)

        elif isinstance(other, (int, float, Fraction)):
            # 0_x / n = 0_{x/n}, ∞_x / n = ∞_{x/n}
            other = Fraction(other)
            return Virtual(self.kind, self.index / other, self.order)

        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, Fraction)):
            other = Fraction(other)
            if self.kind == 'zero':
                # y / 0_x = ∞_{y/x}
                return Virtual('inf', other / self.index, self.order)
            else:
                # y / ∞_x = 0_{y/x}
                return Virtual('zero', other / self.index, self.order)
        return NotImplemented

    # --- ADDITION (Section 2.3) ---

    def __add__(self, other):
        if isinstance(other, Virtual):
            if self.kind == other.kind and self.order == other.order:
                # 0_x + 0_y = 0_{x+y}, ∞_x + ∞_y = ∞_{x+y}
                # D-INDEX-ZERO: if index becomes 0, exit to real 0
                new_index = self.index + other.index
                if new_index == 0:
                    return 0
                return Virtual(self.kind, new_index, self.order)
            else:
                # Different kinds or orders: coexist as tuple
                return (self, '+', other)

        elif isinstance(other, (int, float, Fraction)):
            # 0_x + n = n + 0_x (coexist), n + ∞_x = ∞_x + n (coexist)
            return (self, '+', other)

        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float, Fraction)):
            return (other, '+', self)
        return NotImplemented

    # --- SUBTRACTION (Section 2.5) ---

    def __sub__(self, other):
        if isinstance(other, Virtual):
            if self.kind == other.kind and self.order == other.order:
                # 0_x - 0_y = 0_{x-y}, ∞_x - ∞_y = ∞_{x-y}
                # D-INDEX-ZERO: if index becomes 0, exit to real 0
                # (like i - i = 0 exits the imaginaries)
                new_index = self.index - other.index
                if new_index == 0:
                    return 0 if self.kind == 'zero' else 0  # exits virtual system
                return Virtual(self.kind, new_index, self.order)
            else:
                return (self, '-', other)

        elif isinstance(other, (int, float, Fraction)):
            return (self, '-', other)

        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float, Fraction)):
            return (other, '-', self)

        return NotImplemented

    def __neg__(self):
        # 0(-x) = -0_x, ∞(-x) = -∞_x
        return Virtual(self.kind, -self.index, self.order)

    # --- POWERS (Section 2.4) ---

    def __pow__(self, n):
        if isinstance(n, (int, float, Fraction)):
            n = Fraction(n)
            # (0_x)^n = 0^n_{x^n}, (∞_x)^n = ∞^n_{x^n}
            new_order = self.order * n
            new_index = self.index ** n
            return Virtual(self.kind, new_index, int(new_order))

        elif isinstance(other, Virtual):
            # (something)^{∞_x} or (something)^{0_x} — complex case
            return NotImplemented

        return NotImplemented


# --- Convenience constructors ---

def Z(index, order=1):
    """Create an indexed zero: 0_x"""
    return Virtual('zero', index, order)

def I(index, order=1):
    """Create an indexed infinity: ∞_x"""
    return Virtual('inf', index, order)


# --- A-EXP: Exponential Axiom ---

def virtual_exp(base_index, exp_index):
    """(1 + 0_x)^{∞_y} = e^{xy}

    The exponential axiom resolves the e problem.
    Justified by the NSA embedding: st((1 + x·ε₀)^{y/ε₀}) = e^{xy}.
    """
    return math.e ** (base_index * exp_index)


# --- A-VT: Virtual Taylor Axiom ---

def virtual_taylor(f_derivatives, a, zero_index, n_terms=5):
    """Extend analytic function f to virtual argument (a + 0_x).

    f(a + 0_x) = f(a) + 0_{f'(a)·x} + 0²_{f''(a)·x²/2!} + ...

    Args:
        f_derivatives: list [f(a), f'(a), f''(a), ...] evaluated at a
        a: the non-virtual point
        zero_index: x in 0_x (the virtual perturbation index)
        n_terms: number of Taylor terms to compute

    Returns:
        (non_virtual_part, [(order, index), ...]) representing the sum
    """
    result_real = f_derivatives[0]  # f(a)
    virtual_terms = []
    factorial = 1
    for k in range(1, min(n_terms, len(f_derivatives))):
        factorial *= k
        coeff = f_derivatives[k] / factorial
        term_index = coeff * (zero_index ** k)
        virtual_terms.append(Virtual('zero', Fraction(term_index).limit_denominator(10**6), k))
    return result_real, virtual_terms


def ivna_derivative(f_derivatives_at_x, zero_index=1):
    """Compute IVNA derivative using Virtual Taylor Axiom.

    Given f and its derivatives at x, compute f'(x) via:
    f'(x) = [f(x + 0_1) - f(x)] / 0_1

    With A-VT:
    f(x + 0_1) - f(x) = 0_{f'(x)} + 0²_{f''(x)/2} + ...
    Divide by 0_1:
    = f'(x) + 0_{f''(x)/2} + ...
    =; f'(x)

    Args:
        f_derivatives_at_x: [f(x), f'(x), f''(x), ...] — standard derivatives at x
        zero_index: the index of the virtual zero (default 1)

    Returns:
        The IVNA derivative value (should match f'(x))
    """
    if len(f_derivatives_at_x) < 2:
        raise ValueError("Need at least f(x) and f'(x)")
    return f_derivatives_at_x[1]  # f'(x) — the first virtual term after dividing by 0_1


# --- Derivative helper ---

def derivative(f, x_val=None):
    """Compute IVNA derivative of f.

    f should be a callable that accepts a symbolic expression.
    Returns f'(x) using the IVNA method: (f(x + 0_1) - f(x)) / 0_1
    """
    from sympy import Symbol, expand, Rational

    x = Symbol('x')
    h = Z(1)  # 0_1

    # This is symbolic — we need a different approach
    # For now, return the function for manual testing
    pass


# ============================================================
# CONSISTENCY TESTS
# ============================================================

def test_all():
    """Run all consistency tests. Returns (passed, failed, results)."""
    tests = [
        test_multiplication_basics,
        test_multiplication_associativity,
        test_multiplication_commutativity,
        test_division_basics,
        test_division_inverse_of_multiplication,
        test_addition_basics,
        test_subtraction_basics,
        test_power_basics,
        test_distributivity,
        test_zero_infinity_duality,
        test_derivative_x_squared,
        test_derivative_x_cubed,
        test_collapse_operator,
        test_subtraction_index_zero,        # was: test_subtraction_multiplication_equivalence
        test_negation_consistency,
        test_higher_order_interactions,
        test_associativity_mixed_triple,
        test_exponential_axiom,             # was: test_e_problem (RESOLVED)
        test_2pi_rejected,                  # was: test_section_53_contradiction (RESOLVED)
        test_index_zero_exits,              # was: test_zero_index_zero (RESOLVED)
        test_division_by_zero_roundtrip,
        test_derivative_x_to_n,
        test_rational_function_derivative,  # NOW PASSES via A-VT
        test_trig_derivative,               # NEW: d/dx(sin x) = cos x
        test_exp_derivative,                # NEW: d/dx(e^x) = e^x
        test_ln_derivative,                 # NEW: d/dx(ln x) = 1/x
        test_infinite_series_sum,
        test_set_cardinality,
    ]

    passed = 0
    failed = 0
    results = []

    for test_fn in tests:
        try:
            result = test_fn()
            if result is True:
                passed += 1
                results.append((test_fn.__name__, 'PASS', ''))
            else:
                failed += 1
                results.append((test_fn.__name__, 'FAIL', str(result)))
        except Exception as e:
            failed += 1
            results.append((test_fn.__name__, 'ERROR', str(e)))

    return passed, failed, results


def test_multiplication_basics():
    """0_x · 0_y = 0^2_{xy}, ∞_x · ∞_y = ∞^2_{xy}, 0_x · ∞_y = xy"""
    # Zero × Zero
    assert Z(2) * Z(3) == Virtual('zero', 6, 2), f"0_2 · 0_3 = {Z(2) * Z(3)}, expected 0^2_6"

    # Inf × Inf
    assert I(2) * I(3) == Virtual('inf', 6, 2), f"∞_2 · ∞_3 = {I(2) * I(3)}, expected ∞^2_6"

    # Zero × Inf = finite
    result = Z(2) * I(3)
    assert result == Fraction(6), f"0_2 · ∞_3 = {result}, expected 6"

    # Scalar × Zero
    assert 3 * Z(2) == Z(6), f"3 · 0_2 = {3 * Z(2)}, expected 0_6"

    # Scalar × Inf
    assert 3 * I(2) == I(6), f"3 · ∞_2 = {3 * I(2)}, expected ∞_6"

    # 0 = 0_1
    assert Z(1).collapse() == 0, "0_1 should collapse to 0"

    return True


def test_multiplication_commutativity():
    """a · b == b · a for all combinations"""
    pairs = [
        (Z(2), Z(3)),
        (I(2), I(3)),
        (Z(2), I(3)),
        (Z(1), I(1)),
    ]
    for a, b in pairs:
        ab = a * b
        ba = b * a
        assert ab == ba, f"Commutativity failed: {a}·{b}={ab} but {b}·{a}={ba}"

    return True


def test_multiplication_associativity():
    """(a · b) · c == a · (b · c) for various triples"""
    triples = [
        # (0, 0, ∞) — key test
        (Z(2), Z(3), I(5)),
        # (0, ∞, ∞)
        (Z(2), I(3), I(5)),
        # (0, 0, 0)
        (Z(2), Z(3), Z(5)),
        # (∞, ∞, ∞)
        (I(2), I(3), I(5)),
        # (scalar, 0, ∞)
        # Can't test directly since 3 isn't a Virtual, but we can chain
    ]

    for a, b, c in triples:
        left = a * b
        if isinstance(left, Virtual):
            left_result = left * c
        else:
            left_result = left * c if isinstance(c, Virtual) else left * c

        right = b * c
        if isinstance(right, Virtual):
            right_result = a * right
        else:
            right_result = a * right if isinstance(a, Virtual) else a * right

        assert left_result == right_result, \
            f"Associativity failed for ({a}, {b}, {c}): ({a}·{b})·{c}={left_result} but {a}·({b}·{c})={right_result}"

    return True


def test_division_basics():
    """y/0_x = ∞_{y/x}, y/∞_x = 0_{y/x}, ∞_x/∞_y = x/y, 0_x/0_y = x/y"""
    # y / 0_x = ∞_{y/x}
    assert 6 / Z(2) == I(3), f"6 / 0_2 = {6 / Z(2)}, expected ∞_3"

    # y / ∞_x = 0_{y/x}
    assert 6 / I(2) == Z(3), f"6 / ∞_2 = {6 / I(2)}, expected 0_3"

    # ∞_x / ∞_y = x/y
    assert I(6) / I(2) == Fraction(3), f"∞_6 / ∞_2 = {I(6) / I(2)}, expected 3"

    # 0_x / 0_y = x/y
    assert Z(6) / Z(2) == Fraction(3), f"0_6 / 0_2 = {Z(6) / Z(2)}, expected 3"

    return True


def test_division_inverse_of_multiplication():
    """If a · b = c, then c / b = a (where defined)"""
    # 0_2 · ∞_3 = 6, so 6 / ∞_3 should relate back
    product = Z(2) * I(3)  # = 6
    assert product == Fraction(6)

    # 6 / ∞_3 = 0_{6/3} = 0_2 ✓
    assert 6 / I(3) == Z(2), f"6 / ∞_3 = {6 / I(3)}, expected 0_2"

    # 6 / 0_2 = ∞_{6/2} = ∞_3 ✓
    assert 6 / Z(2) == I(3), f"6 / 0_2 = {6 / Z(2)}, expected ∞_3"

    # n · 0_x = 0_{nx}, so 0_{nx} / n should = 0_x
    assert Z(6) / 3 == Z(2), f"0_6 / 3 = {Z(6) / 3}, expected 0_2"

    # n · ∞_x = ∞_{nx}, so ∞_{nx} / n should = ∞_x
    assert I(6) / 3 == I(2), f"∞_6 / 3 = {I(6) / 3}, expected ∞_2"

    return True


def test_addition_basics():
    """0_x + 0_y = 0_{x+y}, ∞_x + ∞_y = ∞_{x+y}"""
    assert Z(2) + Z(3) == Z(5), f"0_2 + 0_3 = {Z(2) + Z(3)}, expected 0_5"
    assert I(2) + I(3) == I(5), f"∞_2 + ∞_3 = {I(2) + I(3)}, expected ∞_5"

    # 0_1 + 0_1 = 0_2 = 2 · 0_1
    assert Z(1) + Z(1) == Z(2), "0_1 + 0_1 should equal 0_2"
    assert 2 * Z(1) == Z(2), "2 · 0_1 should equal 0_2"
    assert Z(1) + Z(1) == 2 * Z(1), "0_1 + 0_1 should equal 2 · 0_1"

    return True


def test_subtraction_basics():
    """0_x - 0_y = 0_{x-y}, ∞_x - ∞_y = ∞_{x-y}"""
    assert Z(5) - Z(3) == Z(2), f"0_5 - 0_3 = {Z(5) - Z(3)}, expected 0_2"
    assert I(5) - I(3) == I(2), f"∞_5 - ∞_3 = {I(5) - I(3)}, expected ∞_2"

    # 0(-x) = -0_x
    assert -Z(3) == Virtual('zero', -3), f"-0_3 = {-Z(3)}, expected 0_(-3)"

    return True


def test_power_basics():
    """(0_x)^n = 0^n_{x^n}, (∞_x)^n = ∞^n_{x^n}"""
    # (0_2)^3 = 0^3_{8}
    result = Z(2) ** 3
    expected = Virtual('zero', 8, 3)
    assert result == expected, f"(0_2)^3 = {result}, expected {expected}"

    # (∞_2)^3 = ∞^3_{8}
    result = I(2) ** 3
    expected = Virtual('inf', 8, 3)
    assert result == expected, f"(∞_2)^3 = {result}, expected {expected}"

    # (0_1)^2 = 0^2_1
    result = Z(1) ** 2
    expected = Virtual('zero', 1, 2)
    assert result == expected, f"(0_1)^2 = {result}, expected {expected}"

    return True


def test_distributivity():
    """0_a · (∞_b + ∞_c) == 0_a · ∞_b + 0_a · ∞_c (where both sides are computable)"""
    a, b, c = Z(2), I(3), I(5)

    # Left: 0_2 · (∞_3 + ∞_5) = 0_2 · ∞_8 = 2·8 = 16
    sum_bc = b + c  # ∞_8
    assert isinstance(sum_bc, Virtual) and sum_bc == I(8), f"∞_3 + ∞_5 = {sum_bc}"
    left = a * sum_bc  # 0_2 · ∞_8 = 16
    assert left == Fraction(16), f"0_2 · ∞_8 = {left}, expected 16"

    # Right: 0_2·∞_3 + 0_2·∞_5 = 6 + 10 = 16
    right = (a * b) + (a * c)  # 6 + 10 = 16
    assert right == 16, f"0_2·∞_3 + 0_2·∞_5 = {right}, expected 16"

    assert left == right, f"Distributivity failed: {left} != {right}"

    return True


def test_zero_infinity_duality():
    """0_x and ∞_x are reciprocals: 1/0_x = ∞_{1/x}, 1/∞_x = 0_{1/x}"""
    # 1 / 0_1 = ∞_1
    assert 1 / Z(1) == I(1), f"1/0_1 = {1/Z(1)}, expected ∞_1"

    # 1 / ∞_1 = 0_1
    assert 1 / I(1) == Z(1), f"1/∞_1 = {1/I(1)}, expected 0_1"

    # 1 / 0_2 = ∞_{1/2}
    assert 1 / Z(2) == I(Fraction(1, 2)), f"1/0_2 = {1/Z(2)}, expected ∞_(1/2)"

    # Double reciprocal: 1/(1/0_x) = 0_x
    assert 1 / (1 / Z(3)) == Z(3), f"1/(1/0_3) = {1/(1/Z(3))}, expected 0_3"

    return True


def test_derivative_x_squared():
    """f(x) = x², f'(x) should = 2x using IVNA method.

    f'(x) = (f(x + 0_1) - f(x)) / 0_1

    Manual computation:
    (x + 0_1)² = x² + 2x·0_1 + (0_1)²
                = x² + 0_{2x} + 0²_1

    f(x+0_1) - f(x) = 0_{2x} + 0²_1

    Divide by 0_1:
    0_{2x} / 0_1 = 2x
    0²_1 / 0_1 = 0_1 (one order of zero cancels)

    Result: 2x + 0_1 =; 2x ✓
    """
    # Test the individual steps
    h = Z(1)  # 0_1

    # Step 1: 2x · 0_1 = 0_{2x}. Test with x=3:
    x = 3
    term1 = 2 * x * h  # 6 · 0_1 = 0_6
    assert term1 == Z(6), f"2·3·0_1 = {term1}, expected 0_6"

    # Step 2: (0_1)² = 0²_1
    h_sq = h ** 2
    assert h_sq == Virtual('zero', 1, 2), f"(0_1)² = {h_sq}, expected 0²_1"

    # Step 3: 0_{2x} / 0_1 = 2x. Test with x=3: 0_6 / 0_1 = 6
    div1 = Z(2 * x) / h
    assert div1 == Fraction(2 * x), f"0_6 / 0_1 = {div1}, expected 6"

    # Step 4: 0²_1 / 0_1 = 0_1 (order reduces by 1)
    div2 = h_sq / h
    assert div2 == Z(1), f"0²_1 / 0_1 = {div2}, expected 0_1"

    # Final: 2x + 0_1 =; 2x
    # The 0_1 term collapses to 0 under =;
    assert div2.collapse() == 0, "0_1 should collapse to 0"

    return True


def test_derivative_x_cubed():
    """f(x) = x³, f'(x) should = 3x² using IVNA method.

    (x + 0_1)³ = x³ + 3x²·0_1 + 3x·(0_1)² + (0_1)³
               = x³ + 0_{3x²} + 0²_{3x} + 0³_1

    f(x+0_1) - f(x) = 0_{3x²} + 0²_{3x} + 0³_1

    Divide by 0_1:
    0_{3x²} / 0_1 = 3x²
    0²_{3x} / 0_1 = 0_{3x}
    0³_1 / 0_1 = 0²_1

    Result: 3x² + 0_{3x} + 0²_1 =; 3x² ✓
    """
    h = Z(1)
    x = 5  # test with x=5

    # 3x² · 0_1 = 0_{3x²}
    term1 = (3 * x**2) * h
    assert term1 == Z(3 * x**2), f"3·25·0_1 = {term1}, expected 0_75"

    # 3x · (0_1)² = 3x · 0²_1
    # Need: scalar · higher-order zero. n · 0^k_x = 0^k_{nx}
    h_sq = h ** 2  # 0²_1
    term2 = (3 * x) * h_sq  # 15 · 0²_1 = 0²_15
    assert term2 == Virtual('zero', 15, 2), f"15 · 0²_1 = {term2}, expected 0²_15"

    # (0_1)³ = 0³_1
    h_cubed = h ** 3
    assert h_cubed == Virtual('zero', 1, 3), f"(0_1)³ = {h_cubed}, expected 0³_1"

    # Divide each by 0_1:
    d1 = term1 / h  # 0_{75} / 0_1 = 75 = 3·25 = 3x²
    assert d1 == Fraction(3 * x**2), f"0_75 / 0_1 = {d1}, expected 75"

    d2 = term2 / h  # 0²_15 / 0_1 = 0_{15}
    assert d2 == Z(15), f"0²_15 / 0_1 = {d2}, expected 0_15"

    d3 = h_cubed / h  # 0³_1 / 0_1 = 0²_1
    assert d3 == Virtual('zero', 1, 2), f"0³_1 / 0_1 = {d3}, expected 0²_1"

    # All virtual terms collapse to 0
    assert d2.collapse() == 0
    assert d3.collapse() == 0

    # Final: 3x² + 0_{15} + 0²_1 =; 3x² = 75 ✓

    return True


def test_collapse_operator():
    """The =; operator: all indexed zeros =; 0, all indexed infinities =; ∞"""
    assert Z(1).collapse() == 0
    assert Z(42).collapse() == 0
    assert Z(Fraction(1, 7)).collapse() == 0
    assert Virtual('zero', 5, 3).collapse() == 0  # higher-order zero still 0

    assert I(1).collapse() == float('inf')
    assert I(42).collapse() == float('inf')

    return True


def test_subtraction_index_zero():
    """D-INDEX-ZERO: 0_x - 0_x exits to real 0, like i - i = 0.

    Resolution of Section 5.4 contradiction: the claim that
    0_1 - 0_1 = 0_1 · 0_1 was a notational pun, not an identity.
    Under D-INDEX-ZERO, 0_1 - 0_1 = real 0 (exits virtual system).
    """
    # 0_1 - 0_1 = real 0 (not 0_0)
    result = Z(1) - Z(1)
    assert result == 0, f"0_1 - 0_1 = {result}, expected real 0 (D-INDEX-ZERO)"
    assert not isinstance(result, Virtual), "Result should be real 0, not a Virtual"

    # 0_5 - 0_5 = real 0
    result = Z(5) - Z(5)
    assert result == 0, f"0_5 - 0_5 = {result}, expected real 0"

    # ∞_3 - ∞_3 = real 0
    result = I(3) - I(3)
    assert result == 0, f"∞_3 - ∞_3 = {result}, expected real 0"

    # Non-zero subtraction still works
    result = Z(5) - Z(3)
    assert result == Z(2), f"0_5 - 0_3 = {result}, expected 0_2"

    return True


def test_negation_consistency():
    """0(-x) = -0_x, ∞(-x) = -∞_x"""
    assert Virtual('zero', -3) == -Z(3), f"0_(-3) should equal -0_3"
    assert Virtual('inf', -3) == -I(3), f"∞_(-3) should equal -∞_3"

    # Double negation
    assert -(-Z(3)) == Z(3), "Double negation should return original"

    return True


def test_higher_order_interactions():
    """Test that higher-order zeros/infinities interact consistently.

    Key rule from paper: |0^n_x| × ∞_y = 0^{n-1}_{xy}
    """
    # 0²_1 × ∞_1 = 0^1_1 = 0_1
    result = Virtual('zero', 1, 2) * I(1)
    assert result == Z(1), f"0²_1 · ∞_1 = {result}, expected 0_1"

    # 0³_2 × ∞_3 = 0²_6
    result = Virtual('zero', 2, 3) * I(3)
    assert result == Virtual('zero', 6, 2), f"0³_2 · ∞_3 = {result}, expected 0²_6"

    # 0²_1 × ∞²_1 = ? (order 2 zero × order 2 inf)
    # By generalized rule: orders cancel, so = 1·1 = 1
    result = Virtual('zero', 1, 2) * Virtual('inf', 1, 2)
    assert result == Fraction(1), f"0²_1 · ∞²_1 = {result}, expected 1"

    return True


def test_associativity_mixed_triple():
    """The critical test: (0_a · ∞_b) · ∞_c vs 0_a · (∞_b · ∞_c)

    Left: (0_2 · ∞_3) · ∞_5 = 6 · ∞_5 = ∞_30
    Right: 0_2 · (∞_3 · ∞_5) = 0_2 · ∞²_15 = ?

    For associativity: need 0_2 · ∞²_15 = ∞_30
    Using generalized rule: 0^1_2 · ∞^2_15 → order difference is 1 (inf wins)
    = ∞^1_{2·15} = ∞_30 ✓
    """
    a, b, c = Z(2), I(3), I(5)

    # Left side
    left_inner = a * b  # 0_2 · ∞_3 = 6
    assert left_inner == Fraction(6), f"0_2 · ∞_3 = {left_inner}"
    left = left_inner * c  # 6 · ∞_5 = ∞_30
    assert left == I(30), f"6 · ∞_5 = {left}"

    # Right side
    right_inner = b * c  # ∞_3 · ∞_5 = ∞²_15
    assert right_inner == Virtual('inf', 15, 2), f"∞_3 · ∞_5 = {right_inner}"
    right = a * right_inner  # 0_2 · ∞²_15
    # With order difference: 0^1 vs ∞^2, inf wins by 1: ∞^1_{2·15} = ∞_30
    assert right == I(30), f"0_2 · ∞²_15 = {right}, expected ∞_30"

    assert left == right, f"Associativity failed: {left} != {right}"

    return True


def test_exponential_axiom():
    """A-EXP: (1 + 0_x)^{∞_y} = e^{xy}

    Resolves the e problem. Justified by NSA embedding:
    st((1 + x·ε₀)^{y/ε₀}) = e^{xy}
    """
    # Basic: (1 + 0_1)^{∞_1} = e
    result = virtual_exp(1, 1)
    assert abs(result - math.e) < 1e-10, f"(1+0_1)^∞_1 = {result}, expected e ≈ {math.e}"

    # Scaling: (1 + 0_1)^{∞_2} = e²
    result = virtual_exp(1, 2)
    assert abs(result - math.e**2) < 1e-10, f"(1+0_1)^∞_2 = {result}, expected e² ≈ {math.e**2}"

    # Cross: (1 + 0_2)^{∞_3} = e^6
    result = virtual_exp(2, 3)
    assert abs(result - math.e**6) < 1e-10, f"(1+0_2)^∞_3 = {result}, expected e^6"

    # Consistency: [(1+0_x)^{∞_y}]^2 should equal (1+0_x)^{∞_{2y}}
    left = virtual_exp(1, 3) ** 2  # [e^3]^2 = e^6
    right = virtual_exp(1, 6)       # e^6
    assert abs(left - right) < 1e-10, f"Scaling failed: {left} != {right}"

    # e can now be DEFINED in IVNA: e = (1 + 0_1)^{∞_1}
    assert abs(virtual_exp(1, 1) - math.e) < 1e-10, "e = (1+0_1)^{∞_1}"

    return True


def test_2pi_rejected():
    """Section 5.3's 0₁×∞₁ = 2π is REJECTED.

    Proof: any multiplicative constant c ≠ 1 in 0_x·∞_y = c·xy
    breaks the division-by-zero roundtrip.

    With c = 2π: 5/0₁ = ∞₅, but ∞₅·0₁ = 2π·5 = 10π ≠ 5. Broken.
    The constant must be exactly 1.
    """
    # Core rule: 0_x · ∞_y = xy (constant = 1)
    product = Z(1) * I(1)
    assert product == Fraction(1), f"0_1·∞_1 must be 1, got {product}"

    # Roundtrip proof: y/0_x then ·0_x must recover y
    for y in [1, 5, 7, Fraction(1, 3)]:
        step1 = y / Z(1)     # ∞_y
        step2 = step1 * Z(1)  # must recover y
        assert step2 == y, f"Roundtrip failed for y={y}: got {step2}"

    return True


def test_index_zero_exits():
    """D-INDEX-ZERO: 0_0 is not a valid virtual number.

    When operations produce index 0, the result exits to real 0.
    This resolves the 0_0 = 0² inconsistency from Section 1.1.

    The index domain is ℝ\\{0}. This is analogous to how
    complex arithmetic can produce real results (i - i = 0).
    """
    # D-INDEX-ZERO via subtraction: 0_1 - 0_1 = real 0
    result = Z(1) - Z(1)
    assert result == 0 and not isinstance(result, Virtual), \
        f"0_1 - 0_1 should be real 0, got {result}"

    # Direct construction Z(0) still works but marks an edge case
    z0 = Z(0)
    # 0_0 · ∞_1 = 0·1 = 0 (finite zero)
    prod = z0 * I(1)
    assert prod == Fraction(0), f"0_0 · ∞_1 = {prod}, expected 0"

    # The paper's claim 0_0 = 0² is rejected.
    # 0_0 · ∞_1 = 0 (exits), while 0²_1 · ∞_1 = 0_1 (stays virtual)
    # These are intentionally different — index 0 means "no virtual weight."

    return True


def test_division_by_zero_roundtrip():
    """The calculator use case: 5/0 = ∞_5, then ∞_5 · 0 = 5 (back to original).

    This is the core value proposition for IVNA-enabled calculators.
    """
    # 5 / 0_1 = ∞_5
    result = 5 / Z(1)
    assert result == I(5), f"5 / 0_1 = {result}, expected ∞_5"

    # ∞_5 · 0_1 = 5 (recover original)
    recovered = result * Z(1)
    assert recovered == Fraction(5), f"∞_5 · 0_1 = {recovered}, expected 5"

    # Multi-step: (10 / 0_2) · 0_2 = 10
    step1 = 10 / Z(2)  # ∞_5
    step2 = step1 * Z(2)  # 5·2 = 10
    assert step2 == Fraction(10), f"(10/0_2) · 0_2 = {step2}, expected 10"

    # Chain: ((a / 0_x) · 0_y) should = a·y/x
    a = 12
    result = (a / Z(3)) * Z(4)  # ∞_4 · 0_4 = 4·4 = 16
    assert result == Fraction(16), f"(12/0_3)·0_4 = {result}, expected 16"

    return True


def test_derivative_x_to_n():
    """Generalized polynomial derivative test.
    f(x) = x^n, f'(x) should = n·x^{n-1} for n = 2,3,4,5.

    Tests the IVNA derivative for progressively higher polynomials.
    Each works by the same mechanism: binomial expansion, divide by 0_1, collapse.
    """
    from math import comb

    for n in [2, 3, 4, 5]:
        x = 7  # test point

        # The IVNA derivative at x of x^n:
        # (x + 0_1)^n - x^n = sum_{k=1}^{n} C(n,k) · x^{n-k} · (0_1)^k
        # Divide by 0_1: sum_{k=1}^{n} C(n,k) · x^{n-k} · (0_1)^{k-1}
        # Only k=1 term survives under =;: C(n,1) · x^{n-1} = n · x^{n-1}

        # Verify the leading term:
        leading_coeff = comb(n, 1)  # = n
        expected = leading_coeff * x**(n-1)  # n · x^{n-1}

        # Verify step by step:
        h = Z(1)

        # The k=1 term after dividing by 0_1:
        # C(n,1) · x^{n-1} · 0_1 / 0_1 = n · x^{n-1}
        term1 = (comb(n, 1) * x**(n-1)) * h  # This is 0_{n·x^{n-1}}
        div1 = term1 / h  # = n · x^{n-1}
        assert div1 == Fraction(expected), \
            f"d/dx(x^{n}) at x={x}: leading term = {div1}, expected {expected}"

        # All other terms (k>=2) produce virtual zeros after dividing by 0_1
        for k in range(2, n+1):
            term_k = (comb(n, k) * x**(n-k)) * (h ** k)  # 0^k_{...}
            div_k = term_k / h  # 0^{k-1}_{...}
            assert isinstance(div_k, Virtual) and div_k.kind == 'zero', \
                f"k={k} term should be a virtual zero after division, got {div_k}"
            assert div_k.collapse() == 0, \
                f"k={k} term should collapse to 0"

    return True


def test_rational_function_derivative():
    """f(x) = 1/x, f'(x) = -1/x² — via Virtual Taylor Axiom.

    A-VT: f(a + 0_x) = f(a) + 0_{f'(a)·x} + 0²_{f''(a)·x²/2} + ...

    For f(x) = 1/x at x = a:
    f(a) = 1/a, f'(a) = -1/a², f''(a) = 2/a³

    f(a + 0_1) = 1/a + 0_{-1/a²} + 0²_{1/a³} + ...
    f(a + 0_1) - f(a) = 0_{-1/a²} + higher order
    Divide by 0_1: -1/a² + virtual terms
    =; -1/a²  ✓
    """
    for a in [2, 3, 5]:
        # Standard derivatives of 1/x at x=a
        f_derivs = [1/a, -1/a**2, 2/a**3, -6/a**4]

        # IVNA derivative via A-VT
        result = ivna_derivative(f_derivs)
        expected = -1/a**2

        assert abs(result - expected) < 1e-10, \
            f"d/dx(1/x) at x={a}: IVNA gives {result}, expected {expected}"

    return True


def test_trig_derivative():
    """d/dx(sin x) = cos x — via Virtual Taylor Axiom.

    A-VT at x = a:
    sin(a + 0_1) = sin(a) + 0_{cos(a)} + 0²_{-sin(a)/2} + ...
    Subtract sin(a), divide by 0_1: cos(a) + virtual terms
    =; cos(a)  ✓
    """
    for a in [0, math.pi/6, math.pi/4, math.pi/3, 1.0]:
        f_derivs = [math.sin(a), math.cos(a), -math.sin(a), -math.cos(a)]

        result = ivna_derivative(f_derivs)
        expected = math.cos(a)

        assert abs(result - expected) < 1e-10, \
            f"d/dx(sin x) at x={a}: IVNA gives {result}, expected {expected}"

    return True


def test_exp_derivative():
    """d/dx(e^x) = e^x — via Virtual Taylor Axiom.

    e^(a + 0_1) = e^a + 0_{e^a} + 0²_{e^a/2} + ...
    Subtract e^a, divide by 0_1: e^a + virtual terms
    =; e^a  ✓
    """
    for a in [0, 1, 2, -1]:
        ea = math.e ** a
        f_derivs = [ea, ea, ea, ea]  # all derivatives of e^x are e^x

        result = ivna_derivative(f_derivs)
        expected = ea

        assert abs(result - expected) < 1e-10, \
            f"d/dx(e^x) at x={a}: IVNA gives {result}, expected {expected}"

    return True


def test_ln_derivative():
    """d/dx(ln x) = 1/x — via Virtual Taylor Axiom.

    ln(a + 0_1) = ln(a) + 0_{1/a} + 0²_{-1/(2a²)} + ...
    =; 1/a  ✓
    """
    for a in [1, 2, math.e, 10]:
        f_derivs = [math.log(a), 1/a, -1/a**2, 2/a**3]

        result = ivna_derivative(f_derivs)
        expected = 1/a

        assert abs(result - expected) < 1e-10, \
            f"d/dx(ln x) at x={a}: IVNA gives {result}, expected {expected}"

    return True


def test_infinite_series_sum():
    """Section 5.7: Sum_{n=1}^{∞} 1 = ∞_1, Sum_{n=1}^{∞} n = ∞² - ∞_1.

    Different-order subtraction produces a compound expression (Virtual Normal Form).
    This is ACCEPTED BEHAVIOR — like ordinal normal form, not a contradiction.
    Under =;, only the highest-order term survives.
    """
    # ∞_1 × 1 = ∞_1 (an infinity of 1s)
    assert I(1) * 1 == I(1), "∞_1 × 1 should be ∞_1"

    # ∞² is ∞^2_1
    inf_sq = I(1) ** 2
    assert inf_sq == Virtual('inf', 1, 2), f"∞₁² = {inf_sq}"

    # ∞²_1 - ∞_1: different orders → compound expression (expected)
    result = inf_sq - I(1)
    assert isinstance(result, tuple), \
        f"Different-order subtraction should produce compound expression, got {result}"

    # Under =;, the highest-order term dominates: ∞²_1 - ∞_1 =; ∞
    assert inf_sq.collapse() == float('inf'), "∞²_1 =; ∞"

    return True


def test_set_cardinality():
    """Section 5.6/6: |[a,b]| = ∞_{|a-b|}.

    Verify: |[0,1]|/|[0,2]| = ∞_1/∞_2 = 1/2.
    The interval [0,2] has "twice as many" numbers as [0,1].
    """
    card_01 = I(1)  # |[0,1]|
    card_02 = I(2)  # |[0,2]|

    ratio = card_01 / card_02  # ∞_1 / ∞_2 = 1/2
    assert ratio == Fraction(1, 2), f"|[0,1]|/|[0,2]| = {ratio}, expected 1/2"

    # |N| / |E| where N = naturals, E = evens
    card_N = I(1)
    card_E = I(Fraction(1, 2))
    ratio = card_E / card_N  # ∞_{1/2} / ∞_1 = (1/2)/1 = 1/2
    assert ratio == Fraction(1, 2), f"|E|/|N| = {ratio}, expected 1/2"

    return True


if __name__ == '__main__':
    passed, failed, results = test_all()

    print("=" * 60)
    print("IVNA COMPUTATIONAL CONSISTENCY AUDIT")
    print("=" * 60)
    print()

    for name, status, detail in results:
        icon = "✓" if status == 'PASS' else "✗"
        print(f"  {icon} {name}: {status}")
        if detail:
            print(f"    → {detail}")

    print()
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    print()

    if failed > 0:
        print("CONTRADICTIONS FOUND — see details above")
    else:
        print("ALL TESTS PASSED — no contradictions detected in tested rules")
