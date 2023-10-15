import dataclasses
import json
import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional

from dataclasses_json import dataclass_json


class States(Enum):
    MAIN = "main"
    WAITING_FOR_HEBREW_ENGLISH_PAIR = "waiting_for_hebrew_english_pair"
    ASKING_IF_WANT_TO_ADD_MORE_WORDS = "asking_if_want_to_add_more_words"
    WAITING_FOR_USERS_ANSWER = "waiting_for_users_answer"


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
    state: Optional[States] = None
    last_question: Optional[Question] = None


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


# write state mangment functions


def send_msg(user: User, text: str):
    print(f"msg to  user {user.id} {text}")


def custom_asdict_factory(data):
    def convert_value(obj):
        if isinstance(obj, Enum):
            return obj.value
        return obj

    return dict((k, convert_value(v)) for k, v in data)


# game class
@dataclass_json
@dataclass
class EnglishGame:
    users: Dict[str, User] = dataclasses.field(default_factory=dict)
    pairs: List[Pair] = dataclasses.field(default_factory=list)

    # = [
    #             Pair('hello', 'שלום'),
    #             Pair('bye', 'להתראות'),
    #             Pair('good morning', 'בוקר טוב'),
    #

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
    def play(self, user: User):
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
            self.main_menu(user)
            return
        question = Question(self.pairs[question_index], options)
        user.state = States.WAITING_FOR_USERS_ANSWER
        user.last_question = question
        send_msg(user, f'what is the hebrew word for {question.pair.englishWord}?')
        send_msg(user, f'your options are: {question.options}')

    def main_menu(self, user: User):
        send_msg(user, 'hello what do you want to do (add words or play or list words)')
        user.state = States.MAIN


    def add_words(self, user: User):
        send_msg(user, 'please enter english Hebrew pair in the format: english word, hebrew word')
        user.state = States.WAITING_FOR_HEBREW_ENGLISH_PAIR

    # handle functions
    def handle_main_state(self, user: User, msg: str):
        if msg == 'add words':
            self.add_words(user)
        elif msg == 'list words':
            send_msg(user, f'your words are:{[(pair.englishWord, pair.hebrewWord) for pair in self.pairs]}')
            self.main_menu(user)
        elif msg == 'play':
            self.play(user)
        else:
            send_msg(user, 'please choose one of the options')

    def handle_waiting_for_hebrew_english_pair_state(self, user: User, msg: str):
        english_word, hebrew_word  = msg.split(',')
        pair = Pair(english_word.strip(), hebrew_word.strip())
        send_msg(user, f'you entered {pair.englishWord} {pair.hebrewWord}, would you like to add more words?')
        user.state = States.ASKING_IF_WANT_TO_ADD_MORE_WORDS
        self.pairs.append(pair)
        self.save_data()

    def handle_asking_if_want_to_add_more_words_state(self, user: User, msg: str):
        if msg == 'yes':
            self.add_words(user)
        elif msg == 'no':
            self.main_menu(user)
        else:
            send_msg(user, 'please choose one of the options')

    def handle_waiting_for_users_answer_state(self, user: User, msg: str):
        if msg == user.last_question.pair.hebrewWord:
            send_msg(user, 'correct')
            self.play(user)
        else:
            send_msg(user, 'wrong')
            self.play(user)

    def run(self):
        while True:
            msg = input('enter msg: ')
            userid = "1"
            msg = msg.lower()
            if userid not in self.users:
                self.users[userid] = User(userid)
            user = self.users[userid]
            if user.state is None:
                self.main_menu(user)
            elif msg == '/exit':
                self.main_menu(user)
            elif user.state == States.MAIN:
                self.handle_main_state(user, msg)
            elif user.state == States.WAITING_FOR_HEBREW_ENGLISH_PAIR:
                self.handle_waiting_for_hebrew_english_pair_state(user, msg)
            elif user.state == States.ASKING_IF_WANT_TO_ADD_MORE_WORDS:
                self.handle_asking_if_want_to_add_more_words_state(user, msg)
            elif user.state == States.WAITING_FOR_USERS_ANSWER:
                self.handle_waiting_for_users_answer_state(user, msg)
            else:
                send_msg(user, 'unknown state')

            self.save_data()


if __name__ == '__main__':
    game = (EnglishGame.load())
    game.run()
