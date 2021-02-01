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
8-10 -> Circuitos Digitais :: segunda-feira
10-12 -> Circuitos Digitais :: terça-feira
8-10 -> Fundamentos de Programação :: terça-feira
10-12 -> Fundamentos de Programação :: segunda-feira

s2
10-12 -> Laboratório de Programação :: segunda-feira, terça-feira

s3
8-10 -> POO :: segunda-feira
10-12 -> POO :: terça-feira
8-10 -> Programação Linear :: terça-feira
10-12 -> Programação Linear :: segunda-feira

s4
8-10 -> Comunicação de Dados :: quarta-feira
10-12 -> Comunicação de Dados :: quinta-feira
10-12 -> Estruturas de Dados :: segunda-feira, terça-feira
8-10 -> Lógica para Computação :: segunda-feira, terça-feira

s5
8-10 -> Análise de Algoritmos :: sexta-feira
10-12 -> Análise de Algoritmos :: quinta-feira
8-10 -> Eletrônica :: segunda-feira
10-12 -> Eletrônica :: sexta-feira
8-10 -> Engenharia de Software :: quarta-feira, quinta-feira
10-12 -> Grafos :: quarta-feira, terça-feira
8-10 -> Sistemas Operacionais :: terça-feira
10-12 -> Sistemas Operacionais :: segunda-feira

s6
8-10 -> Linguagens de Programação :: quarta-feira
10-12 -> Linguagens de Programação :: quinta-feira
8-10 -> Redes :: segunda-feira, terça-feira
8-10 -> Sistemas Embarcados :: sexta-feira
10-12 -> Sistemas Embarcados :: quarta-feira
10-12 -> Teoria da Computação :: segunda-feira, terça-feira

s7
8-10 -> Compiladores :: quarta-feira
10-12 -> Compiladores :: quarta-feira
10-12 -> Inteligência Artificial :: segunda-feira, terça-feira
8-10 -> Projeto de Sistemas :: segunda-feira, terça-feira

s8
10-12 -> Gestão de Projetos :: quinta-feira, sexta-feira
8-10 -> Inteligência Computacional Aplicada :: quarta-feira, segunda-feira
10-12 -> Processamento de Imagens :: segunda-feira, terça-feira
```
