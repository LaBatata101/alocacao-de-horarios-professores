import time

from itertools import combinations
from functions import atoms, valuations
from typing import Any, Dict, List, Union

from semantics import truth_value
from formula import And, Atom, Not, Or


class Course:
    def __init__(self, name="", semester="", professor=""):
        self.name = name
        self.semester = semester
        self.professor = professor

    def __str__(self):
        return f"{self.name}_{self.semester}_{self.professor}"

    def __repr__(self):
        return f"Course({self.name}, {self.semester}, {self.professor}"


def multiline_input(input_text="") -> List[str]:
    print(input_text)
    lines = []
    while True:
        try:
            line = input()
        except KeyboardInterrupt:
            pass

        if line:
            lines.append(line.strip())
        else:
            break
    return lines


def parse_input(text: List[str]) -> List[Course]:
    """
    Parses the input text and return a list of Course objects
    """
    courses = []
    for i in range(len(text)):
        if len(text[i]) == 2:
            course = None
            semester_str = text[i]
            count = i + 1

            while count < len(text) and len(text[count]) != 2:
                course = Course()
                course.semester = semester_str

                try:
                    course.name, course.professor = text[count].split(',')
                    course.professor = course.professor.strip()
                except ValueError:
                    print(f"Formato da entrada incorreto!\n\033[31mERRO:\033[m \"{text[count]}\", linha {count + 1}")
                    print('''\nFormato da entrada:
                          semestre
                          nome do curso, nome do professor
                                    .
                                    .
                                    .
                          nome do curso, nome do professor
                          ''')
                    exit(1)

                count += 1
                courses.append(course)

    return courses


def and_all(logic_formulas) -> And:
    """
    Receive a list of logic formulas and apply the "and" logic operator on them.
    """
    ands = logic_formulas[0]
    for i in range(1, len(logic_formulas)):
        ands = And(ands, logic_formulas[i])
    return ands


def or_all(logic_formulas) -> Or:
    """
    Receive a list of logic formulas and apply the "or" logic operator on them.
    """
    ors = logic_formulas[0]
    for i in range(1, len(logic_formulas)):
        ors = Or(ors, logic_formulas[i])
    return ors


def dont_allow_on_the_same_period(atomics: List[Atom]) -> Union[And, List[Atom]]:
    """
    Return a logic formula that doesn't allow two different courses to be at the same period.
    """
    if len(atomics) <= 1:
        return atomics

    temp = []
    for c in combinations(atomics, 2):
        temp.append(Not(and_all(c)))
    return and_all(temp)


def period_restriction(courses_atoms: List[Atom]) -> And:
    """
    Same as period_restriction_for_all_semesters_formula but only returns one formula from a list of Atom's.
    """
    first_period, second_period = [], []
    for i in range(len(courses_atoms) // 2):
        first_period.append(courses_atoms[i * 2])
        second_period.append(courses_atoms[(i * 2) - 1])

    all_possible_periods = []
    for i in range(len(first_period)):
        for j in range(len(first_period)):
            course_first_period = first_period[i].name.split("_")[0]
            course_second_period = second_period[j].name.split("_")[0]

            if not course_second_period.startswith(course_first_period):
                all_possible_periods.append(And(first_period[i], second_period[j]))

    return and_all([dont_allow_on_the_same_period(first_period), dont_allow_on_the_same_period(second_period),
                    or_all(all_possible_periods)])


def period_restriction_for_all_semesters_formula(courses: List[Course]) -> List[Union[And, Or]]:
    """
    Take a list of Course objects and creates a logic formula that only allows
    two different Course objects to be at different period on the same semester.
    In the case of this code there will be two periods, the 1º period is
    from 8 to 10, and the 2º period is from 10 to 12.

    Return a list of logic formulas, each position in the list represents a semester.
    Example of a possible logic formula of any semester:
        ~(Circuitos Digitais_1 ^ Fundamentos de Programação_1) ^ ~(Circuitos Digitais_2 ^ Fundamentos de Programação_2) ^
        (Circuitos Digitais_1 ^ Fundamentos de Programação_2) v (Circuitos Digitais_2 ^ Fundamentos de Programação_1)
    """
    atomics_by_semester: Dict[str, List[Atom]] = {}
    for c in courses:
        atomics = []
        for p in (1, 2):  # create a Atom representing the 1º and 2º period of a Course
            atomics.append(Atom(f"{c.name}_{p}"))

        if c.semester not in atomics_by_semester:
            atomics_by_semester[c.semester] = []
        atomics_by_semester[c.semester].extend(atomics)

    final_formula: List[Union[And, Or]] = []
    for s in atomics_by_semester:
        if len(atomics_by_semester[s]) == 2:  # XXX: for the sake of gambiarra
            final_formula.append(Or(atomics_by_semester[s][0], atomics_by_semester[s][1]))
            continue
        final_formula.append(period_restriction(atomics_by_semester[s]))
    return final_formula



def professor_restriction_formula(courses: List[Course]) -> Dict[str, Union[And, Or]]:
    """
    Take a list of Course's objects and create a logic formula that doesn't allow
    a professor to teach two different Course's at the same period. In the
    case of this code there will be two periods, the 1º period is from 8 to 10,
    and the 2º period is from 10 to 12.

    Return dictionare with the professor name as key and the logic formula as value.
    Example:
        {'Carlos':
        ~(Circuitos Digitais_1 ^ Fundamentos de Programação_1) ^ ~(Circuitos Digitais_2 ^ Fundamentos de Programação_2)
        ^ (Circuitos Digitais_1 ^ Fundamentos de Programação_2) v (Circuitos Digitais_2 ^ Fundamentos de Programação_1)}
    """
    courses_with_same_professor: Dict[str, List[Any]] = {}
    for i in range(len(courses)):
        if courses[i].professor not in courses_with_same_professor:
            courses_with_same_professor[courses[i].professor] = []
        courses_with_same_professor[courses[i].professor].append(courses[i].name)

    for professor in courses_with_same_professor:
        periods = []
        for course in courses_with_same_professor[professor]:
            for p in (1, 2):
                periods.append(Atom(f"{course}_{p}"))
        courses_with_same_professor[professor] = periods

    formulas: Dict[str, Union[And, Or]] = {}
    for professor in courses_with_same_professor:
        if len(courses_with_same_professor[professor]) == 2:  # XXX: for the sake of gambiarra
            formulas[professor] = Or(courses_with_same_professor[professor][0],
                                     courses_with_same_professor[professor][1])
            continue
        formulas[professor] = period_restriction(courses_with_same_professor[professor])
    return formulas



def satisfiable_valuations(logic_formula: Union[And, Or]) -> List[Dict[str, bool]]:
    "Returns a list of valuations that satisfies the formula."
    solution = []
    for v in valuations(atoms(logic_formula)):
        if truth_value(logic_formula, v):
            solution.append(v)
    return solution



def get_prof_courses(professor_name: str, professor_possibles_schedules: Dict[str, List[Dict[str, bool]]],
                     schedules_by_semester: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[str]]:
    """
    Return a dictionare with the professor name as key and a list of courses that he/she teaches as value.
    """
    courses_names = [course_name for course_name in professor_possibles_schedules[professor_name][0]]
    courses_schedules_of_professor = {}

    for course_name in courses_names:
        for courses_schedules in schedules_by_semester.values():
            if course_name in courses_schedules:
                courses_schedules_of_professor[course_name] = courses_schedules[course_name]

    return courses_schedules_of_professor



def remove_professors_collisions(professor_possibles_schedules: Dict[str, List[Dict[str, bool]]],
                                 schedules_by_semester: Dict[str, Dict[str, List[str]]]) -> None:
    """
    If in schedules_by_semester there is a schedule for a professor to teach two different courses in the same period
    and in the same day of week for different semesters, remove this schedule collision.
    """
    for prof_name in professor_possibles_schedules:
        professor_courses_schedules = get_prof_courses(prof_name, professor_possibles_schedules, schedules_by_semester)
        courses_names = list(professor_courses_schedules.keys())

        # search for professor schedules collisions in schedules_by_semester
        for i in range(len(courses_names) - 1):
            period_course_i = courses_names[i].split("_")[1]

            for day in professor_courses_schedules[courses_names[i]]:
                for j in range(i + 1, len(courses_names)):
                    period_course_j = courses_names[j].split("_")[1]
                    if period_course_i == period_course_j and day in professor_courses_schedules[courses_names[j]]:
                        # print(f"{prof_name = } {courses_names[i]} -> {courses_names[j] = } {day = }")
                        solve_collision(courses_names[j], courses_names[i], day, schedules_by_semester)


def solve_collision(course_name: str, conflicting_course_name: str, day: str,
                    schedules_by_semester: Dict[str, Dict[str, List[str]]]) -> None:
    """
    Solve the schedule collision of course_name and conflicting_course_name.
    """
    conflicting_semester_index = ''
    semester_index = ''

    for semester, courses_schedules in schedules_by_semester.items():
        if course_name in courses_schedules:
            semester_index = semester
            course_schedules = courses_schedules[course_name]

        if conflicting_course_name in courses_schedules:
            conflicting_semester_index = semester
            conflicting_course_schedules = courses_schedules[conflicting_course_name]

    # remove the conflicting day from the course with more days booked
    if len(conflicting_course_schedules) > len(course_schedules):
        schedules_by_semester[conflicting_semester_index][conflicting_course_name].remove(day)
    else:
        schedules_by_semester[semester_index][course_name].remove(day)


def is_day_picked(day: str, courses_schedules: Dict[str, Dict[str, List[str]]], semester: str):
    """
    The day is picked if it appears two times in course_schedules for a specific semester.
    """
    all_booked_days = [day for days_booked in courses_schedules[semester].values() for day in days_booked]
    return all_booked_days.count(day) == 2


def create_courses_schedules(all_possible_valuations: List[List[Dict[str, bool]]]) -> Dict[str, Dict[str, List[str]]]:
    """
    Take a list of valuations and returns a dictionare with the semester as key and another dictionare
    as value containing the name of the course as a key and a list of days schedule for that course.
    Example:
    >>> create_courses_schedules([[{'Fundamentos de Programação_1': True, 'Fundamentos de Programação_2': False,
    ...                             'Circuitos Digitais_2': True, 'Circuitos Digitais_1': False},
    ...                            {'Fundamentos de Programação_1': False, 'Fundamentos de Programação_2': True,
    ...                             'Circuitos Digitais_2': False, 'Circuitos Digitais_1': True}]])
    {'1': {'Circuitos Digitais_1': ['segunda-feira'],
           'Circuitos Digitais_2': ['terça-feira'],
           'Fundamentos de Programação_1': ['terça-feira'],
           'Fundamentos de Programação_2': ['segunda-feira']}}
    """
    days_taken: Dict[str, Dict[str, List[str]]] = {}
    days = ("segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira")
    for semester, possible_valuations_for_semester in enumerate(all_possible_valuations):
        semester_str = f"{semester + 1}"
        if semester_str not in days_taken:
            days_taken[semester_str] = {}

        for i, schedule in enumerate(possible_valuations_for_semester):
            for course_name, value in schedule.items():
                if value:
                    if course_name not in days_taken[semester_str]:
                        days_taken[semester_str][course_name] = []

                    day = days[i % len(days)]
                    if not is_day_picked(day, days_taken, semester_str):
                        days_taken[semester_str][course_name].append(day)
    return days_taken


def get_course_period(course_name: str) -> str:
    periods = {"1": "8-10", "2": "10-12"}
    name, period = course_name.split("_")
    return f"{periods[period]} -> {name}"


def print_solution(all_courses_schedules: Dict[str, Dict[str, List[str]]]) -> None:
    for semester, courses_schedules in all_courses_schedules.items():
        print(f"s{semester}")
        for course_name in sorted(courses_schedules.keys()):
            days = courses_schedules[course_name]
            if days:  # list of days is not empty
                print(f"{get_course_period(course_name)} :: {', '.join(days)}")
        print()


def main():
    courses_list = parse_input(multiline_input("INPUT: "))

    start = time.time()

    valuations_for_period_restriction = [satisfiable_valuations(formula)
                                         for formula in period_restriction_for_all_semesters_formula(courses_list)]
    valuations_for_professor_restriction = {name: satisfiable_valuations(formula)
                                            for name, formula in professor_restriction_formula(courses_list).items()}

    courses_schedules = create_courses_schedules(valuations_for_period_restriction)
    remove_professors_collisions(valuations_for_professor_restriction, courses_schedules)

    print("\nOUTPUT:")
    print_solution(courses_schedules)

    end = time.time()

    print(f"\nTOTAL TIME: {end - start}")


if __name__ == "__main__":
    main()
