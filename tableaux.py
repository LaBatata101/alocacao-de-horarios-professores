from formula import And, Or, Not, Implies, Atom
from semantics import truth_value, is_literal
from collections import OrderedDict


class Tableaux:
    def __init__(self, *formula_list):
        self.formula_list = self.sort_formulas(formula_list)
        self.__was_formula_processed_lookup = [is_literal(formula) for formula in self.formula_list]
        self.__track_branch = []

    def solve(self):
        """
        Solves the formulas in 'self.formula_list' using Tableaux method.
        Return False if the set of formulas is insatisfiable. Otherwise,
        Return a valuation that makes the set of formulas true.
        """
        valuation = {}
        i = 0
        while False in self.__was_formula_processed_lookup:
            formula = self.formula_list[i]

            if not self.__was_formula_processed_lookup[i]:
                if not self.proccess_formula(formula):
                    return False

            i = (i + 1) % len(self.formula_list)

        for formula in self.formula_list:
            if is_literal(formula):
                if isinstance(formula, Atom):
                    valuation[formula.name] = True
                elif isinstance(formula, Not):
                    valuation[formula.inner.name] = False
        return valuation

    def __does_formula_branch(self, formula):
        """
        Check if the 'formula' applied in the Tableaux creates a branch.
        """
        return isinstance(formula, Or) or isinstance(formula, Implies) or (isinstance(formula, Not) and
                                                                           isinstance(formula.inner, And))

    def sort_formulas(self, formula_list):
        """
        Sort the formulas in 'formula_list', so the formulas that doesn't create branches be in the start of the list.
        """
        result = []
        for formula in formula_list:
            if self.__does_formula_branch(formula):
                result.append(formula)
            else:
                result.insert(0, formula)
        return result

    def __has_complement(self, formula_list):
        """
        Verify if there's a literal and it's negation in 'formula_list'.
        Return False if there's no literal in 'formula_list'.
        """
        for i in range(len(formula_list) - 1):
            if isinstance(formula_list[i], Atom):
                return Not(formula_list[i]) in formula_list[i + 1:]
            elif isinstance(formula_list[i], Not) and isinstance(formula_list[i].inner, Atom):
                return formula_list[i].inner in formula_list[i + 1:]
        return False

    def proccess_formula(self, formula):
        """ Applies the Tableaux rules to the 'formula'.
        Return False if there's a complement in 'self.formula_list' and 'self.track_branch' is empty.
        Return True otherwise.
        """
        index = self.formula_list.index(formula)
        self.__was_formula_processed_lookup[index] = True

        if isinstance(formula, And):
            if formula.left not in self.formula_list:
                self.formula_list.append(formula.left)
                self.__was_formula_processed_lookup.append(is_literal(formula.left))
            if formula.right not in self.formula_list:
                self.formula_list.append(formula.right)
                self.__was_formula_processed_lookup.append(is_literal(formula.right))

        elif isinstance(formula, Not) and isinstance(formula.inner, Or):
            inner = formula.inner
            if Not(inner.left) not in self.formula_list:
                self.formula_list.append(Not(inner.left))
                self.__was_formula_processed_lookup.append(is_literal(Not(inner.left)))
            if Not(inner.right) not in self.formula_list:
                self.formula_list.append(Not(inner.right))
                self.__was_formula_processed_lookup.append(is_literal(Not(inner.right)))

        elif isinstance(formula, Not) and isinstance(formula.inner, Implies):
            inner = formula.inner
            if inner.left not in self.formula_list:
                self.formula_list.append(inner.left)
                self.__was_formula_processed_lookup.append(is_literal(inner.left))
            if Not(inner.right) not in self.formula_list:
                self.formula_list.append(Not(inner.right))
                self.__was_formula_processed_lookup.append(is_literal(Not(inner.right)))

        elif isinstance(formula, Not) and isinstance(formula.inner, Not):
            if formula.inner.inner not in self.formula_list:
                self.formula_list.append(formula.inner.inner)
                self.__was_formula_processed_lookup.append(is_literal(formula.inner.inner))

        elif isinstance(formula, Or):
            self.__track_branch.append((self.__was_formula_processed_lookup.copy(), formula.left))
            if formula.right not in self.formula_list:
                self.formula_list.append(formula.right)
                self.__was_formula_processed_lookup.append(is_literal(formula.right))

        elif isinstance(formula, Not) and isinstance(formula.inner, And):
            self.__track_branch.append((self.__was_formula_processed_lookup.copy(), Not(formula.left)))
            if formula.right not in self.formula_list:
                self.formula_list.append(formula.right)
                self.__was_formula_processed_lookup.append(is_literal(formula.right))

        elif isinstance(formula, Implies):
            self.__track_branch.append((self.__was_formula_processed_lookup.copy(), Not(formula.left)))
            if formula.right not in self.formula_list:
                self.formula_list.append(formula.right)
                self.__was_formula_processed_lookup.append(is_literal(formula.right))

        while self.__has_complement(self.formula_list):
            if not self.__track_branch:
                return False

            was_processed_list_old, formula = self.__track_branch.pop(-1)

            del self.formula_list[len(was_processed_list_old):]

            self.formula_list.append(formula)
            self.__was_formula_processed_lookup = was_processed_list_old
            self.__was_formula_processed_lookup.append(is_literal(formula))

        return True