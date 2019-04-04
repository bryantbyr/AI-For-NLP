# -*- coding: utf-8 -*-
# @Time    : 2019/4/1
# @Author  : qirui


# AI based research [Map research with BFS]

BEIJING, CHANGCHUN, MULUMUQI, WUHAN, GUNAGHZOU, SHENZHEN, BANGKOK, SHANGHAI, NEWYORK = """
BEIJING CHANGCHUN MULUMUQI WUHAN GUANGZHOU SHENZHEN BANGKOK SHANGHAI NEWYORK
""".split()

connection = {
    CHANGCHUN: [BEIJING],
    MULUMUQI: [BEIJING],
    BEIJING: [MULUMUQI, CHANGCHUN, WUHAN, SHENZHEN, NEWYORK],
    NEWYORK: [BEIJING, SHANGHAI],
    SHANGHAI: [NEWYORK, WUHAN],
    WUHAN: [SHANGHAI, BEIJING, GUNAGHZOU],
    GUNAGHZOU: [WUHAN, BANGKOK],
    SHENZHEN: [WUHAN, BANGKOK],
    BANGKOK: [SHENZHEN, GUNAGHZOU]
}


def navigator(start, destination, connecton_graph):
    pathes = [[start], ]

    seen = set()

    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]
        print("I am standing at {}".format(frontier))
        neighbors = connecton_graph[frontier]

        if frontier in seen:    continue
        seen.add(frontier)

        for neighbor in neighbors:
            print("\t ------- I am looking forward to {}".format(neighbor))
            if neighbor == destination:
                return path + [neighbor]
            pathes.append(path + [neighbor])

        # pathes = sorted(pathes, key=len)  # 最小换成


print(navigator(WUHAN, SHENZHEN, connection))





# AI based pattern [sentence generation]

grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的
"""

decimal_grammar = """
expression = operator op operator
operator = num op num
num = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | num num
op = + | - | * | /
"""


def parse_grammar(grammar_str, sep='=>'):
    grammar = {}
    for line in grammar_str.split('\n'):
        line = line.strip()
        if not line:    continue
        target, rules = line.split(sep)
        grammar[target.strip()] = [r.split() for r in rules.split('|')]
    return grammar


import random


def gene(grammar_parsed, target="sentence"):
    if target not in grammar_parsed:    return target
    rule = random.choice(grammar_parsed[target])
    return ''.join([gene(grammar_parsed, target=r) for r in rule if r != 'null'])


g1 = parse_grammar(grammar)
for _ in range(10):
    print(gene(g1))

g2 = parse_grammar(decimal_grammar, sep="=")
for _ in range(10):
    print(gene(g2, target="expression"))
