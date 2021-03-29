from formula import Atom, Not


class CNFDimacsParser:
    def __init__(self):
        self.total_atoms = 0
        self.total_clauses = 0

    def parse(self, path_to_file):
        with open(path_to_file) as f:
            self.__contents = f.readlines()

        cnf_clauses = []
        result = []
        for i, line in enumerate(self.__contents):
            if line.startswith("c"):
                continue

            if line.startswith("p"):
                total_atoms_n_clauses = line.strip().split(" ")[2:]
                self.total_atoms = int(total_atoms_n_clauses[0])
                self.total_clauses = int(total_atoms_n_clauses[2])

                cnf_clauses = self.__contents[i + 1: self.total_clauses]
                break

        for clause in cnf_clauses:
            clause = clause.strip()
            atoms = []
            for atom in clause.split(' '):
                atom = int(atom)
                if atom == 0:
                    break
                elif atom < 0:
                    atoms.append(Not(Atom(str(atom * -1))))
                else:
                    atoms.append(Atom(str(atom)))
            result.append(atoms)
        return result

    def to_cnf_dimacs(self, cnf_formula):
        atomic_lookup = {}
        atomics = set()
        result = []

        for clause in cnf_formula:
            for atomic in clause:
                atomics.add(atomic)

        for i, atomic in enumerate(atomics):
            i += 1
            if isinstance(atomic, Not):
                atomic_lookup[atomic] = -i
            else:
                atomic_lookup[atomic] = i 

        for clause in cnf_formula:
            atomics = []
            for atomic in clause:
                atomics.append(atomic_lookup[atomic])
            result.append(atomics)

        return result