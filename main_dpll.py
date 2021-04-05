import time

from alocacao import (multiline_input, parse_input,
                      period_restriction_for_all_semesters_formula,
                      professor_restriction_formula)
from cnf_dimacs import CNFDimacsParser
from semantics import cnf, cnf_clausal, dpll


def main():
    try:
        qtd_periods = int(input("Digite a quantidade de horários: "))
    except ValueError:
        print("ERROR: Precisa ser um número inteiro positivo.")
        exit(1)

    courses_list = parse_input(multiline_input("INPUT: "))

    parser = CNFDimacsParser()

    period_restriction = period_restriction_for_all_semesters_formula(courses_list, qtd_periods)
    professor_restriction = professor_restriction_formula(courses_list, qtd_periods)
    literal_lookup = {}

    cnf_clauses = []
    for formula in period_restriction:
        cnf_clauses.extend(cnf_clausal(cnf(formula)))

    period_restriction_cnf = parser.to_cnf_dimacs(cnf_clauses, literal_lookup)

    for formula in professor_restriction.values():
        period_restriction_cnf.extend(parser.to_cnf_dimacs(cnf_clausal(cnf(formula)), literal_lookup))

    start = time.time()
    period_valuation = dpll(period_restriction_cnf)

    end = time.time()

    print("\nDPLL OUTPUT:")

    if not period_valuation:
        print(("Não foi possivel alocar horários para os cursos com os dados fornercidos! "
               "Tente aumentar o número de horários."))
    else:
        literal_lookup = dict(zip(literal_lookup.values(), literal_lookup.keys()))
        for atomic, value in period_valuation.items():
            if value:
                print(literal_lookup[atomic])
    print(f"\nDPLL TOTAL TIME: {end - start}")


if __name__ == "__main__":
    main()
