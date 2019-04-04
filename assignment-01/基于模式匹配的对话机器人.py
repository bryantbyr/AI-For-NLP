# -*- coding: utf-8 -*-
# @Time    : 2019/4/1
# @Author  : qirui



def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])


def is_pattern_segment(pattern):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])


def segment_match(pattern, saying):
    seg_pat, i = pattern[0], 1
    if seg_pat == '?':
        while i < len(pattern) and (pattern[i] == '*' or 'a' <= pattern[i] <= 'z' or 'A' <= pattern[i] <= 'Z'):
            seg_pat += pattern[i]
            i += 1

    rest = pattern[i:]
    seg_pat = seg_pat.replace('?*', '?')

    if not rest: return (seg_pat, saying), len(saying)

    # for i, token in enumerate(saying):
    #     if rest[0] == token:
    #         return (seg_pat, saying[:i]), i
    for i in reversed(range(len(saying))):  # 最长匹配原则
        if rest[0] == saying[i]:
            return (seg_pat, saying[:i]), i

    return (seg_pat, saying), len(saying)


def pat_match_with_seg(pattern, saying, tmp):
    if not pattern and not saying:
        return True
    elif not pattern or not saying:
        return False

    pat, i = pattern[0], 1
    if pattern[0] == '?':
        while i < len(pattern) and (pattern[i] == '*' or 'a' <= pattern[i] <= 'z' or 'A' <= pattern[i] <= 'Z'):
            pat += pattern[i]
            i += 1

    if is_variable(pat):
        tmp.append((pat, saying[0]))
        return pat_match_with_seg(pattern[i:], saying[1:], tmp)
    elif is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        tmp.append(match)
        return pat_match_with_seg(pattern[i:], saying[index:], tmp)
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:], tmp)
    else:
        return False


def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns}


def pat_to_dict_cn(patterns):
    return {k: ''.join(v) if isinstance(v, list) else v for k, v in patterns}


def subsitite(rule, parsed_rules):
    if not rule: return []
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)


def subsitite_cn(rule, parsed_rules):
    if not rule: return []
    r = rule[0]
    i = 1
    while i < len(rule) and ('a' <= rule[i] <= 'z' or 'A' <= rule[i] <= 'Z'):
        r += rule[i]
        i += 1
    return [parsed_rules.get(r, r)] + subsitite_cn(rule[i:], parsed_rules)


import random
import jieba


def get_response(saying, response_rules):
    for k, v in response_rules.items():
        res = []
        pattern = pat_match_with_seg(k.split(), saying.split(), res)
        if pattern:
            return ' '.join(subsitite(random.choice(v).split(), pat_to_dict(res)))
        else:
            res = []
            pattern = pat_match_with_seg(list(jieba.cut(k, cut_all=False)),
                                         list(jieba.cut(saying, cut_all=False)), res)
            if pattern:
                return ''.join(subsitite_cn(list(jieba.cut(random.choice(v), cut_all=False)), pat_to_dict_cn(res)))

    return "No response..."


rules = {
    "?*X hello ?*Y": ["Hi, how do you do?"],
    "I was ?*X": ["Were you really ?X ?", "I already knew you were ?X ."],
    '?*x no ?*y': ['why not?', 'You are being a negative', 'Are you saying \'No\' just to be negative?'],
    '?*x if ?*y': ['Do you really think its likely that ?y', 'Do you wish that ?y', 'What do you think about ?y',
                   'Really-- if ?y'],
    '?*x你好?*y': ['你好呀', '请告诉我你的问题'],
    '?*x我想?*y': ['你觉得?y有什么意义呢？', '为什么你想?y', '你可以想想你很快就可以?y了'],
    '?*x我想要?*y': ['?x想问你，你觉得?y有什么意义呢?', '为什么你想?y', '?x觉得... 你可以想想你很快就可以有?y了', '你看?x像?y不', '我看你就像?y']
}



print(get_response("老师我想放假", rules))
print(get_response("老哥我想要买书", rules))
print(get_response("Qi hello hello Rui", rules))
print(get_response("no zuo no die", rules))
print(get_response("I will be crashed down if you hurt me", rules))




# 思考题
"""
1. 这样的程序有什么优点？有什么缺点？你有什么改进的方法吗？
优点: 处理逻辑简洁明了，通过模式匹配可对某些话进行特定地回复，结果相对准确
缺点: 我们的处理模板是有限的，而日常生活中我们对话语句是多样且无限的，对于某些对话，我们的程序可能无法做出恰当的回复
改进方法： 增加模板类型和数量 / 对数据语句进行预处理，变换到我们定义好的模板库中 [目的是使其得到正确的模式匹配]

2. 什么是数据驱动？数据驱动在这个程序里如何体现？
(1). 以数据为主导, 我们只关注输入数据, 处理数据的代码可适应不同类型数据的输入或因外界输入数据的不同而自动改变, 最终仍能正确地输出我们想要的结果。
(2). 在这个程序中, 输入的语句是多样的, 它们对应的模板也同时在变化, 我们的代码处理逻辑会自动根据输入的语句查找相应的模板, 从而使其得到正确的回复, 即我们的代码可以适应输入数据的变化, 数据驱动这个处理过程。

3. 数据驱动与AI的关系是什么？
AI的本质就是数据驱动, AI可智能化地处理不同种类的数据, 对于没见过的数据, AI模型也能自适应地进行数据处理, 并有正确的输出结果。

"""
