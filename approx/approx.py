#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import json
import sys
from random import choice

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
    'multiply': question_multiply,
    'divide': question_divide,
    'highest': question_highest_wrapper,
}

def random_from_range(*args):
    """
    Return corresponding args, choose one number from given range
    """
    for arg in args:
        if isinstance(arg, range):
            yield choice(arg)
        else: 
            yield arg

def generate_question(recipe, *args):
    """
    The recipe is a key in the RECIPE_MAP,

    """
    question_fucntion = RECIPE_MAP[recipe]
    randomized_args = random_from_range(*args)
    question, answer = question_fucntion(*randomized_args)
    return question, answer

def play_question(question, answer, precision, print_method):
    while True:
        users_response = input(question)
        try:
            users_answer = float(users_response)
        except:
            return False 
        
        if is_correct(users_answer, answer, precision):
            print_method(correct_greet(answer, users_answer))
            return True
        
        elif users_answer > answer:
            print_method(too_high_hint())
        else: #users_answer < answer
            print_method(too_low_hint())

class ApproxGame(object):
    """
    Game for mental mathmatics in approximate numbers
    """
    def __init__(self):
        levels = {
        # id: (next_level, precision, round_count, recipe, *args)
        0: (1, 0, 3, 'guess', range(0, 100), 0, 100),
        1: (2, 0, 10, 'add', range(1, 10), range(0, 10)),
        2: (3, 0, 10, 'sub', range(1, 10), range(0, 10)),
        3: (4, 10, 10, 'add', range(1, 100), range(0, 100)),
        4: (5, 10, 10, 'sub', range(1, 100), range(0, 100)),
        5: (6, 0, 10, 'highest', 'multiply', 
                    range(10, 99), range(1, 10)),
        6: (7, 0, 10, 'multiply', range(1, 9), range(0, 9)),
        7: (8, 10, 10, 'multiply', range(10, 99), range(0, 9)),
        8: (9, 50, 10, 'multiply', range(100, 999), range(1, 9)),
        9: (10, 100, 5, 'multiply', range(10, 99), range(10, 99)),
        10: (11, 0, 10, 'divide', range(1, 9), range(2, 9)),
        11: (3, 10, 2, 'divide', range(10, 99), range(2, 9)),
        }

        self._levels = levels
        
    def play_level(self, level_id, print_method):
        level = self._levels[level_id]
        next_level, precision, round_count = level[0:3]
        recipe_args = level[3:]
        print_method(new_level_greet(level_id, precision))
        counter = 0
        while counter <= round_count:
            question, answer = generate_question(*recipe_args)
            correctness = play_question(question, answer, 
                                        precision, direct_print)
            if correctness:
                counter += 1
            else:
                return None
        else: 
            return next_level
    
    def run(self):
        level_id = 1
        while True:
            level_id = self.play_level(level_id, direct_print)
            if level_id is None:
                direct_print('=======\n遊戲結束\n=======')
                break

if __name__ == '__main__':
    game = ApproxGame()
    game.run()