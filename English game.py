#original

import random
questions_and_answers = []
class TriviaQuestion:
    def __init__(self, question, correct_answer):
        self.question = question
        self.correct_answer = correct_answer
        self.options = self.generate_options(correct_answer)

    def generate_options(self, correct_answer):
        options = [correct_answer]
        while len(options) < 4:
            random_option = random.choice(questions_and_answers[random.randint(0,len(questions_and_answers)-1)][1:]) # Random placeholder for incorrect answers
            if random_option not in options:
                options.append(random_option)
        random.shuffle(options)
        return options

    def ask_question(self):
        print(self.question)
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option}")

    def check_answer(self, user_answer):
        return self.options[user_answer - 1] == self.correct_answer


def play_trivia_game(questions):
    score = 0
    for question in questions:
        question.ask_question()
        user_answer = int(input("Your answer (enter the corresponding number): "))
        if question.check_answer(user_answer):
            print("Correct!\n")
            score += 1
        else:
            correct_option = question.options.index(question.correct_answer) + 1
            print(f"Wrong! The correct answer was {correct_option}: {question.correct_answer}\n")
    print(f"Your final score: {score}/{len(questions)}")


# User inputs for questions and correct answers

while True:
    question_text = input("Enter a trivia question (or type 'done' to finish): ")
    if question_text.lower() == 'done':
        break
    correct_answer = input("Enter the correct answer: ")
    questions_and_answers.append([question_text, correct_answer])

# Creating TriviaQuestion instances
questions_list = [TriviaQuestion(question, answer) for question, answer in questions_and_answers]

# Playing the trivia game
play_trivia_game(questions_list)