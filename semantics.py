"""
The goal in this module is to define functions associated with the semantics of formulas
in propositional logic.
"""


from formula import Atom, Implies, Not, And, Or
from functions import atoms, valuations
from collections import defaultdict
from statistics import mode


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


def remove_implication(formula):
    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Not):
        return Not(remove_implication(formula.inner))

    if isinstance(formula, Implies):
        left = remove_implication(formula.left)
        right = remove_implication(formula.right)
        return Or(Not(left), right)

    if isinstance(formula, (And, Or)):
        formula.left = remove_implication(formula.left)
        formula.right = remove_implication(formula.right)
        return formula


def is_literal(formula):
    return (isinstance(formula, Not) and isinstance(formula.inner, Atom)) or isinstance(formula, Atom)


def negation_normal_form(formula):
    if is_literal(formula):
        return formula

    if isinstance(formula, (And, Or)):
        formula.left = negation_normal_form(formula.left)
        formula.right = negation_normal_form(formula.right)
        return formula

    if isinstance(formula, Not):
        inner = formula.inner
        if isinstance(inner, Not):
            return negation_normal_form(inner.inner)
        elif isinstance(inner, And):
            return Or(negation_normal_form(Not(inner.left)), negation_normal_form(Not(inner.right)))
        elif isinstance(inner, Or):
            return And(negation_normal_form(Not(inner.left)), negation_normal_form(Not(inner.right)))


def distributive(formula):
    if is_literal(formula):
        return formula

    if isinstance(formula, And):
        formula.left = distributive(formula.left)
        formula.right = distributive(formula.right)
        return formula

    if isinstance(formula, Or):
        left_subformula = distributive(formula.left)
        right_subformula = distributive(formula.right)
        if isinstance(left_subformula, And):
            return And(distributive(Or(left_subformula.left, left_subformula)),
                       distributive(Or(left_subformula.right, right_subformula)))
        if isinstance(right_subformula, And):
            return And(distributive(Or(left_subformula, right_subformula.left)),
                       distributive(Or(left_subformula, right_subformula.right)))
        return Or(left_subformula, right_subformula)


def cnf(formula):
    return distributive(negation_normal_form(remove_implication(formula)))


def cnf_clausal(formula):
    if is_literal(formula):
        return [[formula]]

    if isinstance(formula, Or):
        return [list(atoms(formula))]

    if isinstance(formula, And):
        left = cnf_clausal(formula.left)
        right = cnf_clausal(formula.right)
        return left + right


def has_one_literals_pair(c1, c2):
    count_pairs = defaultdict(lambda: 0)
    for c in c1:
        if isinstance(c, Atom) and Not(c) in c2:
            count_pairs[c] += 1
        elif isinstance(c, Not) and c.inner in c2:
            count_pairs[c] += 1
    return sum(count_pairs.values()) == 1


def res(clause1, clause2):
    c1 = clause1.copy()
    c2 = clause2.copy()
    for c in c1:
        if isinstance(c, Atom) and Not(c) in c2:
            c1.remove(c)
            c2.remove(Not(c))
        elif isinstance(c, Not) and c.inner in c2:
            c1.remove(c)
            c2.remove(c.inner)
    return list(set(c1 + c2))  # temporary?


def find_interpretation(clauses):
    valuation = {}
    for clause in clauses:
        for literal in clause:
            if isinstance(literal, Atom):
                valuation.update({literal.name: True})
            elif isinstance(literal, Not):
                valuation.update({literal.inner.name: False})
    return valuation


def resolution(clauses):  # clauses -> [[p, s, r], [~s, r], [~p], [~r]]
    new_clauses = []
    index = 0
    while True:
        for i in range(index, len(clauses)):
            for j in range(len(clauses)):
                if has_one_literals_pair(clauses[i], clauses[j]):
                    resolvent = res(clauses[i], clauses[j])
                    if not resolvent:
                        return False
                    if resolvent not in new_clauses:
                        new_clauses.append(resolvent)
        if not new_clauses:
            return find_interpretation(clauses)
        index = len(clauses)
        for clause in new_clauses:
            if clause not in clauses:
                clauses.append(clause)
        new_clauses.clear()


def dpll(clauses):
    return dpll_check(clauses, {})


def has_unit_clause(clauses):
    for clause in clauses:
        if len(clause) == 1:
            return True
    return False


def set_valuation(literal, valuation):
    if isinstance(literal, Atom):
        valuation[literal.name] = True
    elif isinstance(literal, Not):
        valuation[literal.inner.name] = False


def remove_clauses_with_literal(clauses, literal, valuation):
    for clause in clauses[:]:
        if literal in clause:
            for l in clause:
                set_valuation(l, valuation)
            clauses.remove(clause)
    return clauses


def remove_complement_literal(clauses, literal):
    for clause in clauses:
        if isinstance(literal, Atom) and Not(literal) in clause:
            clause.remove(Not(literal))
        elif isinstance(literal, Not) and literal.inner in clause:
            clause.remove(literal.inner)
    return clauses


def unit_propagation(clauses, valuation):
    while has_unit_clause(clauses):
        literal = get_atomic(clauses)

        if isinstance(literal, Atom):
            valuation[literal.name] = True
        elif isinstance(literal, Not):
            valuation[literal.inner.name] = False

        clauses = remove_clauses_with_literal(clauses, literal)
        clauses = remove_complement_literal(clauses, literal)
    return clauses, valuation


def get_atomic(clauses):
    # return clauses[0][0]
    smallest_clause_list = []
    no_empty_clauses = [clause for clause in clauses if clause]
    if len(no_empty_clauses) == 1:
        return no_empty_clauses[0][0]

    for i in range(len(no_empty_clauses) - 1):
        if len(no_empty_clauses[i]) < len(no_empty_clauses[i + 1]):
            smallest_clause_list.extend(no_empty_clauses[i])
        else:
            smallest_clause_list.extend(no_empty_clauses[i + 1])

    return mode(smallest_clause_list)  # get the most common literal


def has_only_empty_clauses(clauses):
    for clause in clauses:
        if clause != []:
            return False
    return True


def dpll_check(clauses, valuation):
    clauses, valuation = unit_propagation(clauses, valuation)
    if not clauses:
        return valuation

    if has_only_empty_clauses(clauses):
        return False

    atomic = get_atomic(clauses)
    clauses1 = clauses + [[atomic]]
    if isinstance(atomic, Not):
        clauses2 = clauses + [[atomic.inner]]
    else:
        clauses2 = clauses + [[Not(atomic)]]
    result = dpll_check(clauses1, valuation)

    if result:
        return result

    return dpll_check(clauses2, valuation)
