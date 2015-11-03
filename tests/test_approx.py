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

    def test_is_correct(self):
        correctness = approx.is_correct(800, 1000, 100)
        self.assertEqual(correctness, False)

        correctness = approx.is_correct(1055, 1000, 100)
        self.assertEqual(correctness, True)

        correctness = approx.is_correct(1055, 1000, 50)
        self.assertEqual(correctness, False)

    def test_new_level_greet(self):
        result = approx.new_level_greet(11)
        wanted = '=======\n第 11 關\n======='
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

    def test_generate_range(self):
        result = approx.generate_range('d1')
        wanted = range(0, 10)
        self.assertEqual(result, wanted)
        result = approx.generate_range(10)
        wanted = [10]
        self.assertEqual(result, wanted)

    def test_generate_question(self):
        result = approx.generate_question('add', (1, 3), 'all_pass')
        wanted = ('1 + 3 = ', 4)
        self.assertEqual(result, wanted)

class TestApproxGame(unittest.TestCase):

    def setUp(self):
        self.game = approx.ApproxGame()

    def tearDown(self):
        pass
