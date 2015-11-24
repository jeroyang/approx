#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from random import choice, sample
from itertools import product


def direct_print(text):
    print(text, flush=True)
    
def question_guess(number, lower_bound, upper_bound):
    template = '從 {} 到 {} 猜一個數字：'
    question = template.format(lower_bound, upper_bound)
    answer = number
    return (question, answer)

def question_add(arg1, arg2):
    template = '{0} + {1} = '
    question = template.format(arg1, arg2)
    answer = arg1 + arg2
    return (question, answer)

def question_sub(arg1, wanted_answer):
    template = '{0} - {1} = '
    question = template.format(arg1 + wanted_answer, arg1)
    answer = wanted_answer
    return (question, answer)

def question_sub_fixed(arg1, arg2):
    """
    Given arg1 and arg2 return the question of "arg1 - arg2 = "
    """
    template = '{0} - {1} = '
    question = template.format(arg1, arg2)
    answer = arg1 - arg2
    return (question, answer)

def question_multiply(arg1, arg2):
    template = '{0} × {1} = '
    question = template.format(arg1, arg2)
    answer = arg1 * arg2
    return (question, answer)

def question_divide(arg1, wanted_answer):
    template = '{0} ÷ {1} = '
    question = template.format(arg1*wanted_answer, arg1)
    answer = wanted_answer
    return (question, answer)

def question_highest_digit(original_question, original_answer):
    blocked_answer = '▢' + str(original_answer)[1:]
    question = ''.join([
        original_question,
        blocked_answer,
        '，其中▢應填入什麼數字？',
        ])
    answer = int(str(original_answer)[0])
    return (question, answer)

def question_highest_wrapper(recipe, *args):
    original = generate_question(recipe, *args)
    question, answer = question_highest_digit(*original)
    return (question, answer)

def is_correct(users_answer, answer, precision):
    delta = abs(users_answer - answer)
    
    return delta <= precision

def new_level_greet(level_id, precision):
    template = '第 {} 關 (容許誤差：{})'
    greet = template.format(level_id, precision)
    bar = '=' * 20
    return '\n'.join([bar, greet, bar])

def correct_greet(answer, users_answer):
    if answer == users_answer:
        greet = '太棒了，答案就是 {}！'.format(answer)
    else:
        greet = '算你答對，正確答案是 {}！'.format(answer)
    return greet

def too_high_hint():
    return '太多了，再少一點！'

def too_low_hint():
    return '太少了，再多一點！'
    
RECIPE_MAP = {
    'guess': question_guess,
    'add': question_add,
    'sub': question_sub,
    'subf': question_sub_fixed,
    'multiply': question_multiply,
    'divide': question_divide,
    'highest': question_highest_wrapper,
}

def generate_question_list(recipe, *args):
    
    question_function = RECIPE_MAP[recipe]

    new_args = []
    for arg in args:
        if not isinstance(arg, range):
            new_args.append([arg])
        else:
            new_args.append(arg)
    
    question_list = []
    for arg_tuple in product(*new_args):
        question, answer = question_function(*arg_tuple)
        question_list.append((question, answer))
    return question_list

def play_question(question, answer, precision, print_method, input_func):
    while True:
        users_response = input_func(question)
        try:
            users_answer = float(users_response)
        except:
            confirmed = confirm_exit(input_func)
            if confirmed:
                return False
            else:
                continue
        
        if is_correct(users_answer, answer, precision):
            print_method(correct_greet(answer, users_answer))
            return True
        
        elif users_answer > answer:
            print_method(too_high_hint())
        else: #users_answer < answer
            print_method(too_low_hint())

def confirm_exit(input_func):
    answer = input_func("確認結束遊戲？(是請按1；其他鍵表示否)")
    if answer == '1':
        return True
    else:
        return False

class ApproxGame(object):
    """
    Game for mental mathmatics in approximate numbers
    """
    def __init__(self):
        levels = {
        # id: (next_level, precision, round_count, recipe, *args)
        1: (2, 0, 1, 'guess', range(0, 100), 0, 100),
        2: (3, 0, 10, 'add', range(1, 10), range(0, 10)),
        3: (4, 0, 5, 'subf', 9, range(1, 10)),
        4: (5, 0, 5, 'add', 10, range(1, 10)),
        6: (7, 0, 10, 'add', range(10, 100, 10), range(1, 10)),
        5: (6, 0, 10, 'sub', range(1, 10), range(0, 10)),
        7: (8, 5, 10, 'subf', 99, range(11, 100)),
        8: (9, 0, 10, 'add', range(100, 1000, 100), range(10, 100, 10)),
        9: (10, 0, 10, 'add', range(100, 1000, 100), range(10, 100)),
        10: (11, 10, 10, 'subf', 999, range(100, 1000)),
        11: (12, 10, 10, 'add', range(10, 100), range(10, 100)),
        12: (13, 10, 10, 'sub', range(10, 100), range(0, 100)),
        13: (14, 0, 10, 'highest', 'multiply', 
                    range(10, 99), range(1, 10)),
        14: (15, 0, 10, 'multiply', range(1, 9), range(0, 9)),
        15: (16, 10, 10, 'multiply', range(10, 99), range(0, 9)),
        16: (17, 50, 10, 'multiply', range(100, 999), range(1, 9)),
        17: (18, 100, 5, 'multiply', range(10, 99), range(10, 99)),
        18: (19, 0, 10, 'divide', range(1, 9), range(2, 9)),
        19: (1, 10, 2, 'divide', range(10, 99), range(2, 9)),
        }

        self._levels = levels
        
    def play_level(self, level_id, print_method, input_func):
        level = self._levels[level_id]
        next_level, precision, round_count = level[0:3]
        recipe_args = level[3:]
        print_method(new_level_greet(level_id, precision))
        question_list = generate_question_list(*recipe_args)

        for question, answer in sample(question_list, round_count):
            correctness = play_question(question, answer, 
                        precision, direct_print, input_func)
            if not correctness: # stop game
                return None    
        return next_level

    def run(self, level_id=1):
        while True:
            level_id = self.play_level(level_id, direct_print, input)
            if level_id is None:
                direct_print("=======\n遊戲結束\n=======\n")
                break

if __name__ == '__main__':
    game = ApproxGame()
    game.run()