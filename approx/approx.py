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

def is_correct(users_answer, answer, precision):
    delta = abs(users_answer - answer)
    
    return delta <= precision

def new_level_greet(level_id):
    return '=======\n第 {} 關\n======='.format(level_id)

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
    'division': question_divide,
}

QUESTION_RANGE_MAP = {
    'd1': range(0, 10),
    'd2': range(1, 100),
    'd3': range(10, 1000),
}

ANSWER_FILTER_MAP = {
    'all_pass': lambda n: True,
}

def generate_range(range_key):
    real_range = QUESTION_RANGE_MAP.get(range_key, None)
    if real_range is None:
        return [int(range_key)]
    else:
        return real_range

def generate_question(question_recipe, r_args, a_range, *args):
    """
    The question_recipe are function names in the RECIPE_MAP,

    """
    question_fucntion = RECIPE_MAP[question_recipe]
    is_valid = ANSWER_FILTER_MAP[a_range]
    function_args = [choice(generate_range(arg)) for arg in r_args]
    for i in range(10):
        question, answer = question_fucntion(*function_args)
        if is_valid(answer):
            break
    else:
        raise ValueError('The recipe setting may be wrong.')

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
        # id, recipe, r_args, answer_range, precision, next level
        1: ('guess', ('d2', 0, 99), 'all_pass', 0, 2), 
        2: ('add', ('d1', 'd1'), 'all_pass', 0, 3),
        3: ('sub', ('d1', 'd1'), 'all_pass', 0, 4),
        4: ('add', ('d2', 'd1'), 'all_pass', 1, 5),
        5: ('sub', ('d2', 'd2'), 'all_pass', 1, 6),
        6: ('multiply', ('d1', 'd1'), 'all_pass', 0, 7),
        7: ('multiply', ('d2', 'd1'), 'all_pass', 10, 8),
        8: ('multiply', ('d3', 'd1'), 'all_pass', 20, 9),
        9: ('multiply', ('d2', 'd2'), 'all_pass', 100, 1),
        }

        self._levels = levels
        
    def play_level(self, level_id, print_method):
        level = self._levels[level_id]
        precision = level[3]
        next_level = level[4]
        print_method(new_level_greet(level_id))
        counter = 0
        while counter < 2:
            question, answer = generate_question(*level)
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