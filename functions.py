"""The goal in this module is to define functions that take a formula as input and
do some computation on its syntactic structure. """


from formula import Not, Atom, Implies, And, Or
from itertools import product


def length(formula):
    """Determines the length of a formula in propositional logic."""
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return length(formula.inner) + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return length(formula.left) + length(formula.right) + 1


def subformulas(formula):
    """Returns the set of all subformulas of a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for subformula in subformulas(my_formula):
        print(subformula)

    This piece of code prints p, s, (p v s), (p → (p v s))
    (Note that there is no repetition of p)
    """

    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, Not):
        return {formula}.union(subformulas(formula.inner))
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        sub1 = subformulas(formula.left)
        sub2 = subformulas(formula.right)
        return {formula}.union(sub1).union(sub2)

#  we have shown in class that, for all formula A, len(subformulas(A)) <= length(A).


def atoms(formula):
    """Returns the set of all atoms occurring in a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for atom in atoms(my_formula):
        print(atom)

    This piece of code above prints: p, s
    (Note that there is no repetition of p)
    """
    if isinstance(formula, Atom):
        return {formula}

    if isinstance(formula, Not):
        return atoms(formula.inner)

    if isinstance(formula, (Implies, And, Or)):
        return atoms(formula.left).union(atoms(formula.right))


def number_of_atoms(formula):
    """Returns the number of distinct atoms occurring in a formula."""
    if isinstance(formula, Atom):
        return 1

    if isinstance(formula, Not):
        return number_of_atoms(formula.inner)

    if isinstance(formula, (Implies, And, Or)):
        return number_of_atoms(formula.right) + number_of_atoms(formula.left)


def number_of_connectives(formula):
    """Returns the number of connectives occurring in a formula."""
    if isinstance(formula, Atom):
        return 0

    if isinstance(formula, Not):
        return 1 + number_of_connectives(formula.inner)

    if isinstance(formula, (Implies, And, Or)):
        return 1 + number_of_connectives(formula.right) + number_of_connectives(formula.left)


def substitution(formula, old_subformula, new_subformula):
    """Returns a new formula obtained by replacing all occurrences
    of old_subformula in the input formula by new_subformula."""
    if formula == old_subformula:
        return new_subformula

    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Not):
        formula.inner = substitution(formula.inner, old_subformula, new_subformula)
        return formula

    if isinstance(formula, (Implies, And, Or)):
        formula.left = substitution(formula.left, old_subformula, new_subformula)
        formula.right = substitution(formula.right, old_subformula, new_subformula)
        return formula


def valuations(atoms):
    d = {a.name: [True, False] for a in atoms}
    return [dict(zip(d, v)) for v in product(*d.values())]
