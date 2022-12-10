#!/usr/bin/env python3

import json
import random
import os
from card import Card
from convert_from_quizlet import get_quizlet_cards

class Learn:
    cards = []
    finished = False
    multiple_choice_enabled = False
    max_points = 5

    answered_correctly = 0
    total_answers = 0

    # I know i could've used more simple files than JSON but i was courious about JSON.
    def __init__(self, resource_list, max_points, is_multiple_choice_enabled):
        for resource in resource_list:
            if resource.startswith("http"):
                new_cards = get_quizlet_cards(resource)
                self.cards.extend(new_cards)
            else:
                self.load_cards_from_json(resource)
        self.max_points = max_points
        self.multiple_choice_enabled = is_multiple_choice_enabled

        print("WELCOME to the learn section!")
        print("The selected cards are:")
        for i in self.cards:
            print(i)
        input("\n(Press ENTER to continue)")
        self.quiz()

    def clear_terminal(self):
        os.system("cls")

    def load_cards_from_json(self, file):
        f = open(file,)
        data = json.load(f)
        cards_data = data["cards"]
        for card in cards_data:
            #print(card["id"])
            newCard = Card(str(card["name"]), str(card["answer"]))
            self.cards.append(newCard)

    # The next 2 staticmethods are copied from geekforgeeks and are implemented bad.
    @staticmethod
    def add_card_to_json_from_dict(card_obj, filename):
        number = random.randint(0, 100000000000000)
        new_data = {
            "id": card_obj.number,
            "name": card_obj.name,
            "answer": card_obj.answer
        }

        with open(filename, "r+") as file:
            try:
                file_data = json.load(file)
                file_data["cards"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent = 4)
                print("Card added to "+filename)
            except Exception as e:
                print("Error adding the card " + str(e))

    @staticmethod
    def add_card_to_json_from_card(card, filename):
        number = random.randint(0, 100000000000000)
        new_data = {
            "id": number,
            "name": card.name,
            "answer": card.answer
        }

        with open(filename, "r+") as file:
            try:
                file_data = json.load(file)
                file_data["cards"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent = 4)
                print("Card added to "+filename)
            except Exception as e:
                print("Error adding the card " + str(e))
            

    def multiple_choice_mode(self, card):
        self.clear_terminal()
        answers_shown = self.get_random_answer(card.number)
        answers_shown.insert(random.randint(0,3), card.answer)

        print(f"Question: {card.name}")
        print("Select one of the answers by typing the number:")
        for i in range(len(answers_shown)):
            print(f"{i+1}) {answers_shown[i]}")

        user_answ = input(">  ")

        try:
            user_answ = int(user_answ)
        except ValueError:
            user_answ = -1

        if answers_shown[user_answ-1] == card.answer:
            input("Correct answer!\n\n(Press ENTER to continue)")
            return True
        else: 
            print(f"Oops wrong answer! '{card.answer}' is the correct one")
            input("\n(Press ENTER to continue)")
            return False

    def write_answer_mode(self, card):
        self.clear_terminal()
        print(card.name)
        user_answ = input("> ")
        if user_answ.lower() == card.answer.lower():
            input("Correct answer!\n\n(Press ENTER to continue)")
            return True
        else: 
            print(f"Oops wrong answer! '{card.answer}' is the correct one")
            input("\n(Press ENTER to continue)")
            return False

    def is_the_learning_done(self):
        points = [i.points for i in self.cards]
        good_points = 0
        for i in points:
            if i >= self.max_points:
                good_points += 1
        return True if good_points == len(points) else False

    def get_lowest_cards(self):
        min_points = min(i.points for i in self.cards)
        return [i for i in self.cards if i.points == min_points]

    # used only for multiple choice questions
    def get_random_answer(self, exclude_id):
        random_answers = []
        while len(random_answers) < 2:
            random_one = random.choice(self.cards)
            if random_one.number != exclude_id and random_one.answer not in random_answers:
                random_answers.append(random_one.answer)
        return random_answers
    
    def quiz(self):
        while not self.finished:
            lowest_cards = self.get_lowest_cards()
            random_card = random.choice(lowest_cards)

            if (self.multiple_choice_enabled and random_card.points > 2) or not self.multiple_choice_enabled:
                self.total_answers += 1
                if self.write_answer_mode(random_card):
                    random_card.points += 1
                    self.answered_correctly += 1
            else:
                self.total_answers += 1
                if self.multiple_choice_mode(random_card):
                    random_card.points += 1
                    self.answered_correctly += 1
                
            self.finished = self.is_the_learning_done()
        self.clear_terminal()
        print("Congratulations, you completed the learn section")
        percentual = int(self.answered_correctly/self.total_answers*1000)/10.0
        print(f"You did {percentual}% of answers correctly!")

if __name__ == "__main__":
    one = Learn(["Json/morse_code.json", "https://quizlet.com/ch/481172668/vocaboli-flash-cards/"], 5, True)