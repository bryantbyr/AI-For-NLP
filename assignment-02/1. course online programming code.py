# -*- coding: utf-8 -*-
# @Time    : 2019/4/8
# @Author  : qirui
# @FileName: assignment-02.py


"""
第一部分: 语言模型
"""

import pandas as pd
import re
import jieba


database = './data/sqlResult_1558435.csv'
df = pd.read_csv(database, encoding='gb18030')
all_articles = df['content'].tolist()


def token(string):
    return ' '.join(re.findall('[\w|\d]+', string))

all_articles = [token(str(a)) for a in all_articles]

TEXT = ''
for a in all_articles:
    TEXT += a
print('length of text: {}'.format(len(TEXT)))


def cut(string):
    return list(jieba.cut(string))

ALL_TOKENS = cut(TEXT)
print(len(ALL_TOKENS))

valid_tokens = [t for t in ALL_TOKENS if t.strip() and t != 'n']
print(len(valid_tokens))


# 1-Gram
# Get the frequencies of words
from collections import Counter
from functools import reduce

words_count = Counter(valid_tokens)

# print(words_count.most_common(10))


# frequencies = [f for w, f in words_count.most_common(100)]
# x = [i for i in range(100)]

frequencies_all = [f for w, f in words_count.most_common()]
frequencies_sum = sum(frequencies_all)


def get_prob(word):
    esp = 1 / frequencies_sum
    if word in words_count:
        return words_count[word] / frequencies_sum
    else:
        return esp


def product(numbers):
    return reduce(lambda n1, n2: n1 * n2, numbers)


def language_model_one_gram(string):
    words = cut(string)
    return product([get_prob(w) for w in words])


sentences = """
这是一个比较正常的句子
这个一个比较罕见的句子
小明毕业于清华大学
小明毕业于秦华大学
""".split()

for s in sentences:
    print(s, language_model_one_gram(s))

need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "我去吃火锅，今晚 今晚我去吃火锅"
]

for s in need_compared:
    s1, s2 = s.split()
    p1, p2 = language_model_one_gram(s1), language_model_one_gram(s2)

    better = s1 if p1 > p2 else s2

    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probability {}'.format(s1, p1))
    print('-' * 4 + ' {} with probability {}'.format(s2, p2))

# 2-Gram
all_2_grams_words = [''.join(valid_tokens[i:i + 2]) for i in range(len(valid_tokens[:-2]))]

_2_gram_sum = len(all_2_grams_words)
_2_gram_counter = Counter(all_2_grams_words)


def get_combination_prob(w1, w2):
    if w1 + w2 in _2_gram_counter:
        return _2_gram_counter[w1 + w2] / _2_gram_sum
    else:
        return 1 / _2_gram_sum


def get_prob_2_gram(w1, w2):
    return get_combination_prob(w1, w2) / get_prob(w1)


def language_model_of_2_gram(sentence):
    sentences_probability = 1

    words = cut(sentence)

    for i, word in enumerate(words):
        if i == 0:
            prob = get_prob(word)
        else:
            previous = words[i - 1]
            prob = get_prob_2_gram(previous, word)
        sentences_probability *= prob

    return sentences_probability



need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "今晚我去吃火锅 今晚火锅去吃我",
    "洋葱奶昔来一杯 养乐多绿来一杯"
]

for s in need_compared:
    s1, s2 = s.split()
    p1, p2 = language_model_of_2_gram(s1), language_model_of_2_gram(s2)

    better = s1 if p1 > p2 else s2

    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probability {}'.format(s1, p1))
    print('-' * 4 + ' {} with probability {}'.format(s2, p2))



grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun belong
belong => de property
de => 的
property => 眼睛 | 裙子 | 胳膊 | 尾巴
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的
"""

import random


def parse_grammar(grammar_str, sep='=>'):
    grammar = {}
    for line in grammar_str.split('\n'):
        line = line.strip()
        if not line: continue
        target, rules = line.split(sep)
        grammar[target.strip()] = [r.split() for r in rules.split('|')]

    return grammar


def gene(grammar_parsed, target='sentence'):
    if target not in grammar_parsed: return target
    rule = random.choice(grammar_parsed[target])
    return ''.join(gene(grammar_parsed, target=r) for r in rule if r != 'null')


g = parse_grammar(grammar)
random_generated = [gene(g) for _ in range(100)]
print(sorted(random_generated, key=language_model_of_2_gram, reverse=True))



# """
# 第二部分：正则表达式
# """

pattern = '\w+'
string = '***&& %%## this is a BIGGGGGGGGG thing BI and BIGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg'
print(re.findall(pattern, string))



"""
第三部分：网站爬虫
"""
import requests,re

url = 'https://movie.douban.com/'
response = requests.get(url)
url_pattern = re.compile('https://movie.douban.com/subject/\d+/\?from=showing')
image_pattern = re.compile('https://img3.doubanio.com/view/photo/s_ratio_poster/public/\w\d+.\w+')
html_content = response.text


print(image_pattern.findall(html_content))
print(set(url_pattern.findall(html_content)))

for line in html_content.split():
    match = url_pattern.findall(line)
    if match:
        print(match[0])
