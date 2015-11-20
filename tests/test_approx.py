#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""
test_approx
----------------------------------

Tests for `approx` module.
"""

import unittest

from approx import approx

class TestApprox(unittest.TestCase):
    def test_question_guess(self):
        question, answer = approx.question_guess(5, 1, 100)
        wanted_question = '從 1 到 100 猜一個數字：'
        wanted_answer = 5
        self.assertEqual(question, wanted_question)
        self.assertEqual(answer, wanted_answer)

    def test_question_add(self):
        question, answer = approx.question_add(3, 5)
        wanted_question = '3 + 5 = '
        wanted_answer = 8
        self.assertEqual(question, wanted_question)
        self.assertEqual(answer, wanted_answer)

    def test_question_sub(self):
        question, answer = approx.question_sub(8, 7)
        wanted_question = '15 - 8 = '
        wanted_answer = 7
        self.assertEqual(question, wanted_question)
        self.assertEqual(answer, wanted_answer)

    def test_question_multiply(self):
        question, answer = approx.question_multiply(3, 5)
        wanted_question = '3 × 5 = '
        wanted_answer = 15
        self.assertEqual(question, wanted_question)
        self.assertEqual(answer, wanted_answer)

    def test_question_divide(self):
        question, answer = approx.question_divide(3, 5)
        wanted_question = '15 ÷ 3 = '
        wanted_answer = 5
        self.assertEqual(question, wanted_question)
        self.assertEqual(answer, wanted_answer)

    def test_question_highest_digit(self):
        args = ('15 + 16 = ', 31)
        question, answer = approx.question_highest_digit(*args)
        wanted_question = '15 + 16 = ▢1，其中▢應填入什麼數字？'
        wanted_answer = 3
        self.assertEqual(question, wanted_question)
        self.assertEqual(answer, wanted_answer)
        args = ('300 - 120 = ', 180)
        question, answer = approx.question_highest_digit(*args)
        wanted_question = '300 - 120 = ▢80，其中▢應填入什麼數字？'
        wanted_answer = 1
        self.assertEqual(question, wanted_question)
        self.assertEqual(answer, wanted_answer)

    def test_is_correct(self):
        correctness = approx.is_correct(800, 1000, 100)
        self.assertEqual(correctness, False)

        correctness = approx.is_correct(1055, 1000, 100)
        self.assertEqual(correctness, True)

        correctness = approx.is_correct(1055, 1000, 50)
        self.assertEqual(correctness, False)

    def test_new_level_greet(self):
        result = approx.new_level_greet(11, 0)
        bar = '=' * 20
        wanted = '\n'.join([bar, '第 11 關 (容許誤差：0)', bar])
        self.assertEqual(result, wanted)

    def test_correct_greet(self):
        result = approx.correct_greet(10, 11)
        wanted = '算你答對，正確答案是 10！'
        self.assertEqual(result, wanted)
        result = approx.correct_greet(10, 10)
        wanted = '太棒了，答案就是 10！'
        self.assertEqual(result, wanted)

    def test_too_high_hint(self):
        result = approx.too_high_hint()
        wanted = '太多了，再少一點！'
        self.assertEqual(result, wanted)

    def test_too_low_hint(self):
        result = approx.too_low_hint()
        wanted = '太少了，再多一點！'
        self.assertEqual(result, wanted)

    def test_generate_question(self):
        result = approx.generate_question('add', 1, 3)
        wanted = ('1 + 3 = ', 4)
        self.assertEqual(result, wanted)

    def test_generate_question_list(self):
        result = approx.generate_question_list('add', range(2), range(3))
        wanted = [('0 + 0 = ', 0),
                  ('0 + 1 = ', 1),
                  ('0 + 2 = ', 2),
                  ('1 + 0 = ', 1),
                  ('1 + 1 = ', 2),
                  ('1 + 2 = ', 3)]
        self.assertEqual(result, wanted)

    def test_play_question(self):
        question = 'anything question'
        answer = 15
        precision = 0
        out = []
        def print_method(text):
            out.append(text)

        input_sequence = iter(['13', '15'])
        def input_func(text):
            return next(input_sequence)

        result = approx.play_question(
            question, answer, precision, print_method, input_func)
        wanted = True
        self.assertEqual(result, wanted)
        self.assertEqual(out, ['太少了，再多一點！', '太棒了，答案就是 15！'])

    def test_confirm_exit(self):
        result = approx.confirm_exit(lambda x: '1')
        self.assertTrue(result)
        result = approx.confirm_exit(lambda x: 'd')
        self.assertFalse(result)

class TestApproxGame(unittest.TestCase):

    def setUp(self):
        self.game = approx.ApproxGame()

    def tearDown(self):
        pass
