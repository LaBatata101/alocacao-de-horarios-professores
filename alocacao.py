from functions import atoms, valuations
from typing import Any, Dict, List, Union

from semantics import truth_value
from formula import And, Atom, Not, Or
from typing import List, Dict, Union, Any


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
    Take a list of Course objects and create a logic formula that doesn't allow
    different Course's to be at the same period on the same semester. In the
    case of this code there will be two periods, the 1º period is from 8 to 10,
    and the 2º period is from 10 to 12.

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
