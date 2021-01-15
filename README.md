# Projeto de Lógica da Computação - Alocação de Horários


### Descrição do Problema:
  Um curso de uma universidade quer alocar os horários dos professores e das disciplinas. Todas as
disciplinas possuem 2 horas de duração que devem ser dadas de forma contínua. As aulas são ministradas de
segunda a sexta apenas pela manhã e são alocadas em exatamente um dos seguintes horários: 8-10, 10-12.
Disciplinas do mesmo semestre não podem ocorrer no mesmo hor ́ario e disciplinas ministradas pelo mesmo
professor também não podem ser alocadas no mesmo horário. Os professores do curso querem saber se  ́e
possível alocar os horários das disciplinas sem violar as restrições.


### Executando:
```
$ python alocacao.py
INPUT:
s1
Circuitos Digitais, Carlos
Fundamentos de Programação, Daniel
s2
Laboratório de Programação, Samuel
s3
POO, Marcio
Programação Linear, Ana
s4
Lógica para Computação, João
Comunicação de Dados, José
Estruturas de Dados, Tomás
s5
Análise de Algoritmos, Alice
Grafos, Alice
Sistemas Operacionais, Carlos
Eletrônica, Santos
Engenharia de Software, Marcio
s6
Linguagens de Programação, Fernanda
Teoria da Computação, João
Sistemas Embarcados, Santos
Redes, Tomás
s7
Compiladores, Beatriz
Projeto de Sistemas, Alice
Inteligência Artificial, Amanda
s8
Gestão de Projetos, Daniel
Processamento de Imagens, Beatriz
Inteligência Computacional Aplicada, Amanda


OUTPUT:
s1
8-10 -> Circuitos Digitais :: terça-feira
10-12 -> Circuitos Digitais :: segunda-feira
8-10 -> Fundamentos de Programação :: segunda-feira
10-12 -> Fundamentos de Programação :: terça-feira

s2
8-10 -> Laboratório de Programação :: segunda-feira, terça-feira
10-12 -> Laboratório de Programação :: segunda-feira, quarta-feira

s3
8-10 -> POO :: terça-feira
10-12 -> POO :: segunda-feira
8-10 -> Programação Linear :: segunda-feira
10-12 -> Programação Linear :: terça-feira

s4
8-10 -> Comunicação de Dados :: terça-feira
10-12 -> Comunicação de Dados :: quarta-feira, sexta-feira
8-10 -> Estruturas de Dados :: quinta-feira
10-12 -> Estruturas de Dados :: segunda-feira, terça-feira
8-10 -> Lógica para Computação :: segunda-feira, sexta-feira
10-12 -> Lógica para Computação :: quinta-feira

s5
8-10 -> Análise de Algoritmos :: segunda-feira, quarta-feira, quinta-feira
8-10 -> Eletrônica :: sexta-feira
10-12 -> Eletrônica :: terça-feira
10-12 -> Engenharia de Software :: quinta-feira
10-12 -> Grafos :: segunda-feira, sexta-feira
10-12 -> Sistemas Operacionais :: quarta-feira

s6
8-10 -> Linguagens de Programação :: segunda-feira, sexta-feira
8-10 -> Redes :: quarta-feira
8-10 -> Sistemas Embarcados :: quinta-feira
10-12 -> Sistemas Embarcados :: segunda-feira, quarta-feira
8-10 -> Teoria da Computação :: terça-feira
10-12 -> Teoria da Computação :: sexta-feira

s7
8-10 -> Compiladores :: segunda-feira
10-12 -> Compiladores :: sexta-feira
8-10 -> Inteligência Artificial :: quinta-feira, sexta-feira
10-12 -> Inteligência Artificial :: segunda-feira, terça-feira
8-10 -> Projeto de Sistemas :: terça-feira
10-12 -> Projeto de Sistemas :: quarta-feira, quinta-feira

s8
8-10 -> Gestão de Projetos :: sexta-feira
10-12 -> Gestão de Projetos :: quinta-feira
8-10 -> Inteligência Computacional Aplicada :: segunda-feira, terça-feira
10-12 -> Inteligência Computacional Aplicada :: quarta-feira, sexta-feira
8-10 -> Processamento de Imagens :: quarta-feira, quinta-feira
10-12 -> Processamento de Imagens :: segunda-feira
```
