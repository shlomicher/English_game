import dataclasses
import json
import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional

from dataclasses_json import dataclass_json


class State(Enum):
    WAITING_FOR_MENU_RESPONSE = "waiting_for_menu_response"
    WAITING_FOR_PAIR = "waiting_for_pair"
    WAITING_FOR_ADD_MORE_PAIRS_RESPONSE = "waiting_for_add_more_pairs_response"
    WAITING_FOR_QUESTION_RESPONSE = "waiting_for_question_response"


@dataclass_json
@dataclass
class Pair:
    englishWord: str
    hebrewWord: str


@dataclass_json
@dataclass
class Question:
    pair: Pair
    options: List[str]


@dataclass_json
@dataclass
class User:
    id: str
    state: Optional[State] = None
    last_question: Optional[Question] = None


# utils
def send_msg(user: User, text: str):
    print(f"{user.id}: {text}")


# main class
@dataclass_json
@dataclass
class EnglishGame:
    users: Dict[str, User] = dataclasses.field(default_factory=dict)
    pairs: List[Pair] = dataclasses.field(default_factory=list)

    @staticmethod
    def load():
        try:
            return EnglishGame.from_json(json.load(open('data.json', 'r')))
        except Exception as e:
            print(e)
            return EnglishGame(pairs=[], users={})

    def save_data(self):
        # dump users and pairs to json
        json.dump(self.to_json(), open('data.json', 'w'))

    # actions
    def send_menu(self, user: User):
        send_msg(user, 'hello what do you want to do (add words or play or list words)')
        user.state = State.WAITING_FOR_MENU_RESPONSE

    def ask_for_pair(self, user: User):
        send_msg(user, 'please enter english Hebrew pair in the format: english word, hebrew word')
        user.state = State.WAITING_FOR_PAIR

    def ask_question(self, user: User):
        question_index = random.randint(0, len(self.pairs) - 1)
        # options contains the correct answer and 3 random answers
        options = [self.pairs[question_index].hebrewWord]
        if len(self.pairs) >= 4:
            while len(options) < 4:
                random_option = random.choice(self.pairs).hebrewWord
                if random_option not in options:
                    options.append(random_option)
        else:
            send_msg(user, 'you need at least 4 words to play')
            self.send_menu(user)
            return
        question = Question(self.pairs[question_index], options)
        user.state = State.WAITING_FOR_QUESTION_RESPONSE
        user.last_question = question
        send_msg(user, f'what is the hebrew word for {question.pair.englishWord}?')
        send_msg(user, f'your options are: {question.options}')

    # handle functions
    def handle_menu_response(self, user: User, msg: str):
        if msg == 'add words':
            self.ask_for_pair(user)
        elif msg == 'list words':
            send_msg(user, f'your words are:{[(pair.englishWord, pair.hebrewWord) for pair in self.pairs]}')
            self.send_menu(user)
        elif msg == 'play':
            self.ask_question(user)
        else:
            send_msg(user, 'please choose one of the options')

    def handle_new_pair(self, user: User, msg: str):
        english_word, hebrew_word = msg.split(',')
        pair = Pair(english_word.strip(), hebrew_word.strip())
        send_msg(user, f'you entered {pair.englishWord} {pair.hebrewWord}, would you like to add more words?')
        user.state = State.WAITING_FOR_ADD_MORE_PAIRS_RESPONSE
        self.pairs.append(pair)
        self.save_data()

    def handel_add_more_words_response(self, user: User, msg: str):
        if msg == 'yes':
            self.ask_for_pair(user)
        elif msg == 'no':
            self.send_menu(user)
        else:
            send_msg(user, 'please choose one of the options')

    def handle_question_response(self, user: User, msg: str):
        if msg == user.last_question.pair.hebrewWord:
            send_msg(user, 'correct')
            self.ask_question(user)
        else:
            send_msg(user, 'wrong')
            self.ask_question(user)

    def handle_input(self, user: User, msg: str):
        msg = msg.lower()

        if user.state is None:
            self.send_menu(user)
        elif msg == '/exit':
            self.send_menu(user)
        elif user.state == State.WAITING_FOR_MENU_RESPONSE:
            self.handle_menu_response(user, msg)
        elif user.state == State.WAITING_FOR_PAIR:
            self.handle_new_pair(user, msg)
        elif user.state == State.WAITING_FOR_ADD_MORE_PAIRS_RESPONSE:
            self.handel_add_more_words_response(user, msg)
        elif user.state == State.WAITING_FOR_QUESTION_RESPONSE:
            self.handle_question_response(user, msg)
        else:
            send_msg(user, 'unknown state')

        self.save_data()

    def run(self):
        while True:
            userid = "1"
            msg = input('enter msg: ')

            # create user if not exists
            if userid not in self.users:
                self.users[userid] = User(userid)
            user = self.users[userid]

            self.handle_input(user, msg)


if __name__ == '__main__':
    EnglishGame.load().run()
