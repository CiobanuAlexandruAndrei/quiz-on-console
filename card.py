#!/usr/bin/env python3

import random

class Card:
    number = None
    name = None
    answer = None

    points = 0
    learned = False

    def __init__(self, name, answer):
        self.number = random.randint(0, 100000000000000)
        self.name = name
        self.answer = answer

    def __repr__(self):
        return f"name: {self.name}, answer: {self.answer}"