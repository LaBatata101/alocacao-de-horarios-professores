from typing import Any, Dict, List, Union

from formula import And, Atom, Not, Or


class Course:
    def __init__(self, name="", semester="", professor=""):
        self.name = name
        self.semester = semester
        self.professor = professor

    def __str__(self):
        return f"{self.name}_{self.semester}_{self.professor}"

    def __repr__(self):
        return f"Course({self.name}, {self.semester}, {self.professor})"


def multiline_input(input_text="") -> List[str]:
    print(input_text)
    lines = []
    while True:
        try:
            line = input()
        except KeyboardInterrupt:
            exit(0)

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


def period_restriction(courses_atoms: List[Atom]) -> And:
    """
    Same as period_restriction_for_all_semesters_formula but only returns one formula from a list of Atom's.
    """
    all_possible_periods = []

    for i in range(len(courses_atoms) - 1):
        course_name_i, course_period_i = courses_atoms[i].name.split("_")
        for j in range(i + 1, len(courses_atoms)):
            course_name_j, course_period_j = courses_atoms[j].name.split("_")
            if course_name_i != course_name_j and course_period_i == course_period_j:
                all_possible_periods.append(Not(And(courses_atoms[i], courses_atoms[j])))

    return and_all(all_possible_periods)


def formula_allow_course_in_one_period(atomics_list):
    result = []
    for i in range(len(atomics_list) - 1):
        course_name_i, course_period_i = atomics_list[i].name.split("_")
        for j in range(i + 1, len(atomics_list)):
            course_name_j, course_period_j = atomics_list[j].name.split("_")

            if course_name_i == course_name_j and course_period_i != course_period_j:
                result.append(Not(And(atomics_list[i], atomics_list[j])))

    return and_all(result)


def period_restriction_for_all_semesters_formula(courses: List[Course], qtd_periods: int) -> List[Union[And, Or]]:
    """
    Take a list of Course objects and creates a logic formula that only allows
    two different Course objects to be at different period on the same semester.
    In the case of this code there will be two periods, the 1º period is
    from 8 to 10, and the 2º period is from 10 to 12.

    Return a list of logic formulas, each position in the list represents a semester.
    Example of a possible logic formula of any semester:
        ¬(Circuitos Digitais_1 ∧ Fundamentos de Programação_1) ∧ ¬(Circuitos Digitais_2 ∧ Fundamentos de Programação_2)
        ∧ (Circuitos Digitais_1 ∨ Circuitos Digitais_2) ∧ (Fundamentos de Programação_1 ∨ Fundamentos de Programação_2)
         ∧ ¬(Circuitos Digitais_1 ∧ Circuitos Digitais_2) ∧ ¬(Fundamentos de Programação_1 ∧ Fundamentos de Programação_2)
    """
    atomics_by_semester: Dict[str, List[Atom]] = {}
    possible_periods = {}
    allow_course_in_one_period = {}
    for c in courses:
        atomics = []
        # create a Atom representing the 1º and 2º period that the Course can be taught
        for p in range(1, qtd_periods + 1):
            atomics.append(Atom(f"{c.name}_{p}"))

        if c.semester not in allow_course_in_one_period:
            allow_course_in_one_period[c.semester] = []
        allow_course_in_one_period[c.semester].append(formula_allow_course_in_one_period(atomics))

        if c.semester not in possible_periods:
            possible_periods[c.semester] = []
        possible_periods[c.semester].append(or_all(atomics))

        if c.semester not in atomics_by_semester:
            atomics_by_semester[c.semester] = []
        atomics_by_semester[c.semester].extend(atomics)

    final_formula: List[Union[And, Or]] = []
    for s in atomics_by_semester:
        if len(atomics_by_semester[s]) == qtd_periods:  # if there's only one course in the semester
            final_formula.append(And(or_all(atomics_by_semester[s]), Not(and_all(atomics_by_semester[s]))))
            continue
        final_formula.append(and_all([period_restriction(atomics_by_semester[s]), and_all(possible_periods[s]),
                                      and_all(allow_course_in_one_period[s])]))
    return final_formula


def professor_restriction_formula(courses: List[Course], qtd_periods: int) -> Dict[str, Union[And, Or]]:
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
    allow_course_in_one_period = {}
    for i in range(len(courses)):
        if courses[i].professor not in courses_with_same_professor:
            courses_with_same_professor[courses[i].professor] = []
        courses_with_same_professor[courses[i].professor].append(courses[i].name)

    possible_periods = {}
    for professor in courses_with_same_professor:
        periods = []
        for course in courses_with_same_professor[professor]:
            # create a Atom representing the 1º and 2º period that the Course can be taught
            atomics = []
            for p in range(1, qtd_periods + 1):
                atomics.append(Atom(f"{course}_{p}"))

            periods.extend(atomics)
            if professor not in possible_periods:
                possible_periods[professor] = []
            possible_periods[professor].append(or_all(atomics))

        courses_with_same_professor[professor] = periods

        if professor not in allow_course_in_one_period:
            allow_course_in_one_period[professor] = []
        allow_course_in_one_period[professor].append(formula_allow_course_in_one_period(periods))

    formulas: Dict[str, Union[And, Or]] = {}
    for professor in courses_with_same_professor:
        if len(courses_with_same_professor[professor]) == qtd_periods:  # if the professor only teaches one course
            formulas[professor] = And(or_all(courses_with_same_professor[professor]),
                                      Not(and_all(courses_with_same_professor[professor])))
            continue
        formulas[professor] = and_all([period_restriction(courses_with_same_professor[professor]),
                                       and_all(possible_periods[professor]),
                                       and_all(allow_course_in_one_period[professor])])
    return formulas
