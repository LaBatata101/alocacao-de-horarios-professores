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
