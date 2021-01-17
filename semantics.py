"""
The goal in this module is to define functions associated with the semantics of formulas
in propositional logic.
"""


from formula import Atom, Implies, Not, And, Or
from functions import atoms, valuations


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        try:
            return interpretation[formula.name]
        except KeyError:
            return None

    if isinstance(formula, Not):
        inner = truth_value(formula.inner, interpretation)
        if inner is None:
            return None
        return not inner

    if isinstance(formula, And):
        left = truth_value(formula.left, interpretation)
        right = truth_value(formula.right, interpretation)

        if (right is None and left is False) or (left is None and right is False):
            return False
        return left and right

    if isinstance(formula, Or):
        left = truth_value(formula.left, interpretation)
        right = truth_value(formula.right, interpretation)

        if left is None or right is None:
            return None

        return left or right

    if isinstance(formula, Implies):
        left = truth_value(formula.left, interpretation)
        right = truth_value(formula.right, interpretation)
        if (right is None and left is False) or (left is None and right is True):
            return True

        if left is None:
            return None

        return not (truth_value(formula.left, interpretation) is True and
                    truth_value(formula.right, interpretation) is False)


def is_logical_consequence(premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise,
    it returns False.
    """
    return is_satisfiable(And(premises, Not(conclusion))) is False


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    v = valuations(atoms(formula1).union(atoms(formula2)))

    for k in v:
        if truth_value(formula1, k) != truth_value(formula2, k):
            return False
    return True


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    return is_satisfiable(Not(formula)) is False


def sat(formula, _atoms, interpretation):
    if len(_atoms) == 0:
        if truth_value(formula, interpretation):
            return interpretation
        return False

    _atom = _atoms.pop()
    interpretation1 = interpretation.copy()
    interpretation2 = interpretation.copy()

    interpretation1.update({_atom: True})
    interpretation2.update({_atom: False})
    result = sat(formula, _atoms.copy(), interpretation1)
    if result is not False:
        return result
    return sat(formula, _atoms.copy(), interpretation2)


def preprocess_formula(formula):
    if isinstance(formula, Atom):
        return {formula.name: True}

    if isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            return {formula.inner.name: False}

    if isinstance(formula, And):
        left = preprocess_formula(formula.left)
        right = preprocess_formula(formula.right)
        left.update(right)

        return left

    return {}


def is_satisfiable(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns
    true to the formula. Otherwise, it returns False."""
    interpretation = preprocess_formula(formula)
    atoms_names = {a.name for a in atoms(formula)}
    list_atoms = atoms_names - set(interpretation.keys())
    return sat(formula, list_atoms, interpretation)
