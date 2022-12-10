import telebot
from telebot import types
import random


API_TOKEN = '#'
bot = telebot.TeleBot(API_TOKEN)


token1 = ''
board = list(range(1,10))

def show_board(message):
    bot.send_message(message.chat.id,"-------------")
    for i in range(3):
        table = f"| {board[0+i*3]} | {board[1+i*3]} | {board[2+i*3]}|"
        bot.send_message(message.chat.id,table)
        bot.send_message(message.chat.id,"-------------")
    

def check_win(board):
    win_coord = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False

def take_input_bot(token2):
    valid = False
    while not valid:
        answer_bot = random.randint(1,9)
        print(answer_bot)
        if (str(board[answer_bot-1]) not in "XO"):
            board[answer_bot-1] = token2
            valid = True

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name} {message.from_user.last_name} чтобы начать играть в крестики-нолики набери команду /new_game'
    bot.send_message(message.chat.id,mess)




@bot.message_handler(commands=['new_game'])
def choose_avatar(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn_1 = types.InlineKeyboardButton(text="X",callback_data='btn1')
    btn_2 = types.InlineKeyboardButton(text="O",callback_data='btn2')
    kb.add(btn_1,btn_2)
    bot.send_message(message.chat.id,"Выберите аватар",reply_markup=kb)
    global board
    board = list(range(1,10))

     

@bot.callback_query_handler(func=lambda callback:callback.data)
def check_calback_data(callback):
    if callback.data == 'btn1':
        bot.send_message(callback.message.chat.id,"Вы выбрали X")
        global token1
        token1 = "X"
                
    else:
        bot.send_message(callback.message.chat.id,"Вы выбрали O")
        token1= "O"
  
    qw = f"Куда поставим  {token1} ?"
    player_answer = bot.send_message(callback.message.chat.id, qw)
    bot.register_next_step_handler(player_answer,func)
def func(message):
    try:
        answer = int(message.text)
    except:
        bot.send_message(message.chat.id,"Некорректный ввод. Вы уверены, что ввели число?")
    if answer >= 1 and answer <= 9:
        if (str(board[answer-1]) not in "XO"):
            board[answer-1] = token1
            show_board(message)
            tmp = check_win(board)
            if tmp:
                bot.send_message(message.chat.id, f"выиграл {token1}! наберите /new_game чтобы начать новую игру")
            else:
                bot.send_message(message.chat.id,"ХОДИТ БОТ")
                if token1 == "X":
                    token2 = "O"
                else:
                    token2 = "X"
                take_input_bot(token2)
                show_board(message)
                counter = 1
                counter += 1
                if counter == 9:
                    bot.send_message(message.chat.id,"Ничья!")
                tmp = check_win(board)
                if tmp:
                    bot.send_message(message.chat.id, "выиграл БОТ!")
                else:
                    qw = f"Куда поставим  {token1} ?"
                    player_answer = bot.send_message(message.chat.id, qw)
                    bot.register_next_step_handler(player_answer,func)


        else:
            buzy = bot.send_message(message.chat.id,"Эта клеточка уже занята. Выберите другую")
            bot.register_next_step_handler(buzy,func)
    else:
        bot.send_message(message.chat.id,"Некорректный ввод числа должны быть от 1-9")
        qw = f"Куда поставим  {token1} ?"
        player_answer = bot.send_message(message.chat.id, qw)
        bot.register_next_step_handler(player_answer,func)

bot.polling()