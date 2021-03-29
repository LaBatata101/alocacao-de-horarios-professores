from formula import And, Or, Not, Implies, Atom
from semantics import truth_value, is_literal
from collections import OrderedDict


class Tableaux:
    def __init__(self, *formula_list):
        self.formula_list = self.sort_formulas(formula_list)
        self.__was_formula_processed_lookup = {formula: is_literal(formula) for formula in self.formula_list}
        self.__track_branch = []

    def get_unprocessed_formula(self):
        for formula in self.formula_list:
            if not self.__was_formula_processed_lookup[formula]:
                return formula
        return False

    def solve(self):
        """
        Solves the formulas in 'self.formula_list' using Tableaux method.
        Return False if the set of formulas is insatisfiable. Otherwise,
        Return a valuation that makes the set of formulas true.
        """
        valuation = {}
        # i = 0
        for i, formula in enumerate(self.formula_list):
            formula = self.formula_list[i]
            # formula = self.get_unprocessed_formula()
            # print(formula)
            # if formula is False:
                # break
            if not self.__was_formula_processed_lookup[formula] and not self.proccess_formula(formula):
                return False
        # for i, formula in enumerate(self.formula_list):
            # formula = self.formula_list[i]

            # if not self.__was_formula_processed_lookup[formula]:
                # if not self.proccess_formula(formula):
                    # return False

            # i = (i + 1) % len(self.formula_list)

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
                if Not(formula_list[i]) in formula_list[i + 1:]:
                    return True
            elif isinstance(formula_list[i], Not) and isinstance(formula_list[i].inner, Atom):
                if formula_list[i].inner in formula_list[i + 1:]:
                    return True
        return False

    def proccess_formula(self, formula):
        """ Applies the Tableaux rules to the 'formula'.
        Return False if there's a complement in 'self.formula_list' and 'self.track_branch' is empty.
        Return True otherwise.
        """
        # index = self.formula_list.index(formula)
        # del self.formula_list[index]
        self.__was_formula_processed_lookup[formula] = True
        # del self.__was_formula_processed_lookup[formula]

        if isinstance(formula, And):
            if formula.left not in self.formula_list:
                self.formula_list.append(formula.left)
                self.__was_formula_processed_lookup[formula.left] = is_literal(formula.left)
            if formula.right not in self.formula_list:
                self.formula_list.append(formula.right)
                self.__was_formula_processed_lookup[formula.right] = is_literal(formula.right)

        elif isinstance(formula, Not) and isinstance(formula.inner, Or):
            inner = formula.inner
            left_formula = Not(inner.left)
            right_formula = Not(inner.right)

            if left_formula not in self.formula_list:
                self.formula_list.append(left_formula)
                self.__was_formula_processed_lookup[left_formula] = is_literal(left_formula)

            if right_formula not in self.formula_list:
                self.formula_list.append(right_formula)
                self.__was_formula_processed_lookup[right_formula] = is_literal(right_formula)

        elif isinstance(formula, Not) and isinstance(formula.inner, Implies):
            inner = formula.inner
            left_formula = inner.left
            right_formula = Not(inner.right)

            if left_formula not in self.formula_list:
                self.formula_list.append(left_formula)
                self.__was_formula_processed_lookup[left_formula] = is_literal(left_formula)

            if right_formula not in self.formula_list:
                self.formula_list.append(right_formula)
                self.__was_formula_processed_lookup[right_formula] = is_literal(right_formula)

        elif isinstance(formula, Not) and isinstance(formula.inner, Not):
            if formula.inner.inner not in self.formula_list:
                self.formula_list.append(formula.inner.inner)
                self.__was_formula_processed_lookup[formula.inner.inner] = is_literal(formula.inner.inner)

        elif isinstance(formula, Or):
            self.__track_branch.append((self.__was_formula_processed_lookup.copy(), formula.left))

            if formula.right not in self.formula_list:
                self.formula_list.append(formula.right)
                self.__was_formula_processed_lookup[formula.right] = is_literal(formula.right)

        elif isinstance(formula, Not) and isinstance(formula.inner, And):
            self.__track_branch.append((self.__was_formula_processed_lookup.copy(), Not(formula.inner.left)))

            if Not(formula.inner.right) not in self.formula_list:
                self.formula_list.append(Not(formula.inner.right))
                self.__was_formula_processed_lookup[Not(formula.inner.right)] = is_literal(Not(formula.inner.right))

        elif isinstance(formula, Implies):
            self.__track_branch.append((self.__was_formula_processed_lookup.copy(), Not(formula.left)))

            if formula.right not in self.formula_list:
                self.formula_list.append(formula.right)
                self.__was_formula_processed_lookup[formula.right] = is_literal(formula.right)

        while self.__has_complement(list(self.__was_formula_processed_lookup)):
            if not self.__track_branch:
                return False

            was_processed_list_old, formula = self.__track_branch.pop(-1)

            self.formula_list = list(was_processed_list_old.keys())
            self.formula_list.append(formula)

            self.__was_formula_processed_lookup = was_processed_list_old
            self.__was_formula_processed_lookup[formula] = is_literal(formula)

        # self.formula_list = self.sort_formulas(self.formula_list)

        return True
