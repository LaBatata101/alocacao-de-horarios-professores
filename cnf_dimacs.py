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
                    atoms.append(atom * -1)
                else:
                    atoms.append(atom)
            result.append(atoms)
        return result

    def to_cnf_dimacs(self, cnf_formula, literal_lookup):
        # atomic_lookup = {}
        atomics = set()
        result = []

        if not literal_lookup:
            for clause in cnf_formula:
                for literal in clause:
                    atomics.add(literal)

            for i, literal in enumerate(atomics):
                i += 1
                if isinstance(literal, Not):
                    if literal.inner in literal_lookup:
                        literal_lookup[literal] = -literal_lookup[literal.inner]
                    else:
                        literal_lookup[literal] = -i
                else:
                    if Not(literal) in literal_lookup:
                        literal_lookup[literal] = literal_lookup[Not(literal)] * -1
                    else:
                        literal_lookup[literal] = i

        for clause in cnf_formula:
            atomics = []
            for literal in clause:
                atomics.append(literal_lookup[literal])
            result.append(atomics)

        self.total_atoms = len(atomics)
        self.total_clauses = len(clause)

        return result