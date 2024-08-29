import telebot # импортируем модуль для настройки бота
import random # импортируем модуль рандомайзера

bot = telebot.TeleBot('7242519489:AAFl-QQAUBadSvrQjWmFFfyHfiBs_XQdXco') # создаем объект класса TeleBot и передаем токен Telegram-бота

@bot.message_handler(commands = ['start'])
def say_hi(message):
    bot.send_message(message.chat.id, f'Hi, {message.from_user.first_name}!')

class HangmanList: # создаем класс игры

    def __init__(self): # создаем метод-конструктор

        self.word_catalog = ['python', 'programmer', 'coding', 'bug', 'command'] # список слов
        self.word = random.choice(self.word_catalog) # слово, которое будет отгадывать игрок
        self.word_copy = self.word # копия загаданного слова, с которой будем проверять оставшиеся буквы
        self.word_length = len(self.word) # длина загаданного слова
        self.display = '_' * self.word_length # скрытое загаданное слово
        self.mistakes = 0 # счетчик ошибок
        self.already_guessed = [] # ранее введенные буквы
        self.staps = [
            ' _____ \n  |      \n  |      \n  |      \n  |      \n  |      \n  |      \n__|__\n',
            ' _____ \n  |     | \n  |     |\n  |      \n  |      \n  |      \n  |      \n__|__\n',
            ' _____ \n  |     | \n  |     |\n  |     | \n  |      \n  |      \n  |      \n__|__\n',
            ' _____ \n  |     | \n  |     |\n  |     | \n  |     O \n  |      \n  |      \n__|__\n',
            ' _____ \n  |     | \n  |     |\n  |     | \n  |     O \n  |    /|\ \n  |    / \ \n__|__\n'
        ]
        self.stop_game = False # конец игры

    def check(self, user_letter): # создаем метод проверки вводимых букв

        feedback = { # словарь результата проверки
            'bot_answer': False, # ответ бота о продолжении или окончании игры
            'hang': False # ответ об ошибке или правильном ответе
        }

        if user_letter in self.word_copy: # проверяем, находится ли буква в загаданном слове
            self.already_guessed.append(user_letter) # добавляем букву в список ранее введенных букв
            char_index = self.word_copy.find(user_letter) # определяем индекс буквы в слове
            self.word_copy = self.word_copy[:char_index] + '_' + self.word_copy[char_index + 1:] # в копии слова заменяем отгаданную букву на нижнее подчеркивание
            self.display = self.display[:char_index] + user_letter + self.display[char_index + 1:] # в скрытом слове заменяем нижнее подчеркивание на отгаданную букву
            feedback['hang'] = f'You are guessing letter!\n{self.display}' # в ответе говорим, что буква отгадана
        elif user_letter in self.already_guessed: # проверяем, находится ли буква в списке ранее введенных
            feedback['hang'] = 'Try another letter!' # в ответе говорим, что буква уже была введена
        else: # проверяем все остальные случаи, то есть, если буквы нет в слове
            self.already_guessed.append(user_letter) # добавляем букву в список ранее введенных букв
            self.mistakes += 1 # увеличиваем количество ошибок на 1
            feedback['hang'] = f'You are guessing letter!\n{self.mistakes}' # в ответе говорим, что пользователь допустил ошибку
            match self.mistakes:
                case 1:
                    feedback['hang'] = f'You are guessing letter!\n{self.staps[0]}'
                case 2:
                    feedback['hang'] = f'You are guessing letter!\n{self.staps[1]}'
                case 3:
                    feedback['hang'] = f'You are guessing letter!\n{self.staps[2]}'
                case 4:
                    feedback['hang'] = f'You are guessing letter!\n{self.staps[3]}'
                case 5:
                    feedback['hang'] = f'You are guessing letter!\n{self.staps[4]}'

        if self.mistakes >= 5: # проверяем, превышает ли количество ошибок значения 5
            self.stop_game = True # присваиваем атрибуту конца игры значение истины
            feedback['bot_answer'] = f'You lose...\nHidden word was {self.word}!' # в ответе говорим, что пользователь проиграл
        elif self.word_copy == '_' * self.word_length: # проверяем, остались в копии загаданного слова неотгаданные буквы
            self.stop_game = True # присваиваем атрибуту конца игры значение истины
            feedback['bot_answer'] = f'You WIN:)\nHidden word was {self.word}!' # в ответе говорим, что пользователь выиграл
        else: # проверяем все остальные случаи, то есть, если игра продолжается
            feedback['bot_answer'] = 'Enter your guess ->' # в ответе говорим, чтобы пользователь вводил следующую букву

        return feedback # возвращаем результат проверки

def hangman(game_message): # создаем функцию игры

    welcome_phrase = 'Welcome to Hangman'
    bot.send_message(game_message.chat.id, f'{welcome_phrase:-^{20 + len(welcome_phrase)}}')

    hangman_base = HangmanList() # создаем объект класса игры
    bot.send_message(game_message.chat.id, f'Hidden word: {hangman_base.display}\nEnter your guess ->') # отправляем сообщение, что слово загадано и пользователь должен ввести букву

    @bot.message_handler() # вызываем декоратор для проверки содержимого сообщения
    def char_check(user_guess): # создаем функцию для передачи введенной буквы объекту класса и проверки остановки бота
        if user_guess.text == 'stop': # проверяем, не хочет ли пользователь остановить программу
            bot.stop_polling() # останавливаем работу бота
        else: # проверяем все остальные случаи, то есть, если пользователь ввел букву
            guess = user_guess.text # сохраняем содержимое сообщения в переменную guess
            result = hangman_base.check(guess) # сохраняем результат проверки буквы (feedback) в переменную result
            bot.send_message(user_guess.chat.id, result['hang']) # отправляем сообщение с ответом об ошибке или правильном ответе
            bot.send_message(user_guess.chat.id, result['bot_answer']) # отправляем сообщение с ответом об окончании или продолжении игры

        if hangman_base.stop_game == True: # проверяем, равен ли атрибут конца игры истине
            bot.stop_polling() # останавливаем работу бота


@bot.message_handler(commands = ['game']) # вызываем декоратор для проверки команды /game
def start_game(message): # создаем функцию запуска игры
    bot.send_message(message.chat.id, 'Ow, you want to play! Ok)') # отправляем сообщение о начале игры
    hangman(message) # вызываем функцию игры

bot.polling(none_stop = True) # запускаем постоянную работу бота