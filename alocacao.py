class Curso:
    def __init__(self, nome, semestre, professor, horario):
        self.nome = nome
        self.semestre = semestre
        self.professor = professor
        self.horario = horario

    def __str__(self):
        return f"{self.nome}_{self.semestre}_{self.professor}_{self.horario}"



