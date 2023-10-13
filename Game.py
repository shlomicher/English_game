# write classes
import random
class User:
    def __init__(self, userid):
        self.userid = userid
        self.state = None
        self.pairs = [
            Pair('hello', 'שלום'),
            Pair('bye', 'להתראות'),
            Pair('good morning', 'בוקר טוב'),
            Pair('good night', 'לילה טוב'),
        ]


class MainState:
    def __init__(self):
        pass


class WaitingForHebrewEnglishPairState:
    pass


class AskingIfWantToAddMoreWordsState:
    pass


class WaitingForUsersAnswerState:
    def __init__(self, current_question):
        self.currentQuestion = current_question


class Pair:
    def __init__(self, englishWord, hebrewWord):
        self.englishWord = englishWord
        self.hebrewWord = hebrewWord


class Question:
    def __init__(self, pair, options):
        self.pair = pair
        self.options = options


# write state mangment functions


def main_menu(user: User):
    send_msg(user, 'hello what do you want to do (add words or play or list words)')
    user.state = MainState()


def handle_main_state(user: User, msg: str):
    if msg == 'add words':
        add_words(user)
#    elif msg == 'play':
#        play(user)
    elif msg == 'list words':
        send_msg(user, f'your words are:{[(pair.englishWord, pair.hebrewWord) for pair in user.pairs]}')
        main_menu(user)
    elif msg == 'play':
        play(user)
    else:
        send_msg(user, 'please choose one of the options')


def add_words(user: User):
    send_msg(user, 'please enter english Hebrew pair in the format: english word, hebrew word')
    user.state = WaitingForHebrewEnglishPairState()

def handle_waiting_for_hebrew_english_pair_state(user: User, msg: str):
    english_word, hebrew_word = msg.split(',')
    pair = Pair(english_word, hebrew_word)
    send_msg(user, f'you entered {english_word} {hebrew_word}, would you like to add more words?')
    user.state = AskingIfWantToAddMoreWordsState()
    user.pairs.append(pair)


def handle_asking_if_want_to_add_more_words_state(user: User, msg: str):
    if msg == 'yes':
        add_words(user)
    elif msg == 'no':
        main_menu(user)
    else:
        send_msg(user, 'please choose one of the options')


def send_msg(user: User, text: str):
    print(f"msg to  user {user.userid} {text}")



def play(user: User):
    question_index = random.randint(0,len(user.pairs)-1)
#options contains the correct answer and 3 random answers
    options = [user.pairs[question_index].hebrewWord]
    if len(user.pairs) > 4:
        while len(options) < 4:
            random_option = random.choice(user.pairs[random.randint(0,len(user.pairs)-1)].hebrewWord)
            if random_option not in options:
                options.append(random_option)
    else:
        send_msg(user, 'you need at least 4 words to play')
        main_menu(user)
    question = Question(user.pairs[question_index], options)
    user.state = WaitingForUsersAnswerState(question)
    send_msg(user, f'what is the hebrew word for {question.pair.englishWord}?')
    send_msg(user, f'your options are: {question.options}')

def handle_waiting_for_users_answer_state(user: User, msg: str):
    if msg == user.state.currentQuestion.pair.hebrewWord:
        send_msg(user, 'correct')
        play(user)
    else:
        send_msg(user, 'wrong')
        play(user)


def main():
    users = {}
    while True:
        msg = input('enter msg: ')
        userid, msg = msg.split(' ', 1)
        if userid not in users:
            users[userid] = User(userid)
        user = users[userid]
        if user.state is None:
            main_menu(user)
        elif msg == '/exit':
            main_menu(user)
        elif isinstance(user.state, MainState):
            handle_main_state(user, msg)
        elif isinstance(user.state, WaitingForHebrewEnglishPairState):
            handle_waiting_for_hebrew_english_pair_state(user, msg)
        elif isinstance(user.state, AskingIfWantToAddMoreWordsState):
            handle_asking_if_want_to_add_more_words_state(user, msg)
        elif isinstance(user.state, WaitingForUsersAnswerState):
            handle_waiting_for_users_answer_state(user, msg)
        else:
            send_msg(user, 'unknown state')


if __name__ == '__main__':
    main()

# write main updates manager

