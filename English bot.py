import random
import json
import datetime
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
API_TOKEN = "5744317659:AAHTNPHfIM6dlX-VBdusHEu9UvHqj7rGZJI"
questions_and_answers = []
# gpt
class TriviaQuestion:
    def __init__(self, question, correct_answer):
        self.question = question
        self.correct_answer = correct_answer
        self.options = self.generate_options(correct_answer)

    def generate_options(self, correct_answer):
        options = [correct_answer]
        while len(options) < 4:
            random_option = random.choice(
                questions_and_answers[random.randint(0, len(questions_and_answers) - 1)][1:]
            )
            if random_option not in options:
                options.append(random_option)
        random.shuffle(options)
        return options

    def ask_question(self, update):
        options_text = "\n".join([f"{i}. {option}" for i, option in enumerate(self.options, start=1)])
        update.message.reply_text(f"{self.question}\n{options_text}")

    def check_answer(self, user_answer):
        return self.options[user_answer - 1] == self.correct_answer


def play_trivia_game(questions, update):
    score = 0
    for question in questions:
        question.ask_question(update)
        user_answer = int(input("Your answer (enter the corresponding number): "))
        if question.check_answer(user_answer):
            update.message.reply_text("Correct!\n")
            score += 1
        else:
            correct_option = question.options.index(question.correct_answer) + 1
            update.message.reply_text(
                f"Wrong! The correct answer was {correct_option}: {question.correct_answer}\n"
            )
    update.message.reply_text(f"Your final score: {score}/{len(questions)}")


def save_questions(filename):
    with open(filename, 'w') as file:
        json.dump(questions_and_answers, file)


def load_questions(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I am your trivia bot. Type /trivia to start playing.")


def trivia(update: Update, context: CallbackContext) -> None:
    # Load existing questions
    questions_and_answers = load_questions('../questions.json')

    # Creating TriviaQuestion instances
    questions_list = [TriviaQuestion(question, answer) for question, answer in questions_and_answers]

    # Playing the trivia game
    play_trivia_game(questions_list, update)


def main():
    # Replace 'YOUR_TOKEN' with your actual Telegram bot token
    TOKEN = API_TOKEN
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trivia", trivia))

    updater.start_polling()
    updater.idle()
telegram.Message(+972587560522,datetime.datetime,'fytyto8y8')

if __name__ == '_main_':
    main()