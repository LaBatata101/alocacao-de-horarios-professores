import time

from pysat.solvers import Glucose3

from semantics import cnf, cnf_clausal
from cnf_dimacs import CNFDimacsParser
from alocacao import (multiline_input, parse_input,
                      period_restriction_for_all_semesters_formula,
                      professor_restriction_formula)


def main():
    try:
        qtd_periods = int(input("Digite a quantidade de horários: "))
    except ValueError:
        print("ERROR: Precisa ser um número inteiro positivo.")
        exit(1)

    courses_list = parse_input(multiline_input("INPUT: "))

    parser = CNFDimacsParser()
    literal_lookup = {}

    period_restriction = period_restriction_for_all_semesters_formula(courses_list, qtd_periods)
    professor_restriction = professor_restriction_formula(courses_list, qtd_periods)

    cnf_clauses = []
    for formula in period_restriction:
        cnf_clauses.extend(cnf_clausal(cnf(formula)))

    period_restriction_cnf = parser.to_cnf_dimacs(cnf_clauses, literal_lookup)

    for formula in professor_restriction.values():
        period_restriction_cnf.extend( parser.to_cnf_dimacs(cnf_clausal(cnf(formula)), literal_lookup))

    glucose = Glucose3()
    glucose.append_formula(period_restriction_cnf)

    start = time.time()
    print("PySat OUTPUT:")
    if glucose.solve():
        print(glucose.get_model())
    else:
        print(("Não foi possivel alocar horários para os cursos com os dados fornercidos!"
               " Tente aumentar o número de horários."))

    end = time.time()

    print(f"PySat GLUCOSE3 TOTAL TIME: {end - start}")


if __name__ == "__main__":
    main()
