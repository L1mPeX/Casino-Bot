#!/usr/bin/python3.6
import func, menu, config
import random
def error_message(message, bot):
    bot.send_message(message.chat.id, "Что-то пошло не по плану")
def not_enough_money(message, bot, error_sum):
    chat_id = message.chat.id
    user_balanse = func.get_user_information(chat_id)[1]
    bot.send_message(message.chat.id, f"Ваш баланс равен {user_balanse} RUB\nСумма, которую вы ввели равна {error_sum}\nВведенная сумма не может быть больше, чем баланс")
def main_profile(message, bot):
    chat_id = message.chat.id
    user_information = func.get_user_information(chat_id)
    user_balanse = user_information[1]
    if user_information[2] != 0:
        average_list = user_information[3] / user_information[2]
    else:
        average_list = 0
    bot.send_message(chat_id, f"👤Профиль:\n\n💰Баланс: {user_balanse} RUB \n\n 📈Средний чек {average_list} RUB", reply_markup = menu.gen_refer_kb())
def refer_system(call, bot, user_data):
    chat_id = call.message.chat.id
    user_information = func.get_user_information(chat_id)
    ref_sum = user_information[4]
    count_refs = user_information[5]
    bot.send_message(chat_id, f"👥Реферальная система:\n\nКоличество рефералов {count_refs}\n\nЗаработано с реферальной системы - {ref_sum} RUB\n\nВаша реферальная ссылка - https://t.me/{config.bot_name}?start={chat_id}", reply_markup = menu.gen_ref_system_kb())
def how_work_referal_system(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Получайте процент с продаж и зарабатывайте вместе с нами! Если пользователь зарегисрируется в боте по вашей ссылке, то вами будет получен процент.\n\nСейчас условия такие:\n\nВы будете получать 5% с каждого пополнения приглашенного пользователя.", reply_markup = menu.gen_return_referal_system_how_it_works())
def main_profile_call(call, bot, user_data):
    chat_id = call.message.chat.id
    user_information = func.get_user_information(chat_id)
    user_balanse = user_information[1]
    if user_information[2] != 0:
        average_list = user_information[3] / user_information[2]
    else:
        average_list = 0
    bot.send_message(chat_id, f"👤Профиль:\n\n💰Баланс: {user_balanse} RUB \n\n 📈Средний чек {average_list} RUB", reply_markup = menu.gen_refer_kb())
def main_user_balanse(message, bot):
    chat_id = message.chat.id
    user_balanse = func.get_user_information(chat_id)[1]
    bot.send_message(chat_id, f"💰Баланс:\n\n💷 {user_balanse} RUB", reply_markup = menu.gen_balanse_kb())


def popolnenye(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Выберите платежную систему для пополнения", reply_markup = menu.gen_popoln_plateg_sys_kb())
def withdraw(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Выберите платежную систему для вывода", reply_markup = menu.gen_withdraw_plateg_sys_kb())
def popoln_qiwi(call, bot, user_data):
    chat_id = call.message.chat.id
    try:
        func.delete_last_popoln(chat_id)
    except:
        pass
    bot.register_next_step_handler(bot.send_message(chat_id, "Введите сумму пополнения в рублях"),get_sum_popoln, bot = bot)
def popoln_btc(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.register_next_step_handler(bot.send_message(chat_id, "Введите ваш BTC кошелек, с которого будет выполнено пополнение, в случае ошибки администрация ответственности не несет"), get_btc_num, bot = bot)




def get_sum_popoln(message, bot):
    try:
        chat_id = message.chat.id
        sum_popoln = float(message.text)
        bot.register_next_step_handler(bot.send_message(chat_id, "Введите номер Qiwi кошелька без знака + с которого будет выполнено пополнение"), get_qiwi_num, bot = bot, sum_popoln = sum_popoln)
    except:
        error_message(message, bot)
def get_qiwi_num(message, bot, sum_popoln):
    try:
        chat_id = message.chat.id
        qiwi_num = int(message.text)
        code = random.randint(1000000000, 9999999999)
        code2 = random.randint(1000000000, 9999999999)
        func.create_qiwi_popoln(chat_id, sum_popoln, qiwi_num, code)
        popoln = func.get_last_popoln(chat_id)
        bot.send_message(chat_id, f"Пополнение #{code2}\n\nСумма пополнения: {popoln[1]} RUB\n\nТелефон для перевода: {config.qiwi_num}\n\nКомментарий для пополнения: {popoln[3]}", reply_markup = menu.gen_check_popoln())
    except:
        error_message(message, bot)
def get_btc_num(message, bot):
    chat_id = message.chat.id
    btc_num = message.text
    btc_num = func.create_new_coinbase_plateg()
    bot.send_message(chat_id, f"Для пополнения прешлите на адресс {btc_num}, ту сумму BTC, на которую вы хотите пополнить", reply_markup = menu.gen_check_btc_kb(btc_num))
def main_user_balanse_call(call, bot, user_data):
    chat_id = call.message.chat.id
    user_balanse = func.get_user_information(chat_id)[1]
    bot.send_message(chat_id, f"💰Баланс:\n\n💷 {user_balanse} RUB", reply_markup = menu.gen_balanse_kb())
def check_popoln(call, bot, user_data):
    chat_id = call.message.chat.id
    popoln = func.get_last_popoln(chat_id)
    S = func.check_qiwi_repl(chat_id)
    if S:
        bot.edit_message_text(chat_id = chat_id, message_id = call.message.message_id, text = f"Ваш баланс пополнен на {popoln[1]} RUB")
    else:
        pass
def check_btc(call, bot, user_data):
    chat_id = call.message.chat.id
    sum_pl = func.get_sum_payments_from_adress(user_data)
    c = func.get_course_btc_rub()
    sum_rub = sum_pl * c
    if sum_pl > 0:
       func.repl_bal(chat_id, sum_rub)
       bot.edit_message_text(chat_id = chat_id, message_id = call.message.message_id, text = f"Ваш баланс пополнен\nНа {sum_rub} RUB")




def withdraw_qiwi(call, bot, user_data):
    chat_id = call.message.chat.id
    if func.check_unicless_withdraw(chat_id):
        mes = bot.send_message(chat_id, "Введите сумму вывода в RUB")
        bot.register_next_step_handler(mes, get_qiwi_sum_withdraw, bot = bot)
    else:
        bot.send_message(chat_id, "Ожидайте подтверждения предыдущего вывода, перед созданием новой заявки")
def get_qiwi_sum_withdraw(message, bot):
    try:
        chat_id = message.chat.id
        sum_withdraw = float(message.text)
        user_balanse = func.get_user_information(chat_id)[1]
        if sum_withdraw / 100 * (100 + config.withdraw_comission) <= user_balanse:
            mes = bot.send_message(chat_id, "Введите Qiwi кошелек без знака +")
            bot.register_next_step_handler(mes, get_qiwi_num_withdraw, bot = bot, sum_withdraw = sum_withdraw)
        else:
            not_enough_money(message, bot, sum_withdraw)
    except:
        error_message(message, bot)
def get_qiwi_num_withdraw(message, bot, sum_withdraw):
    try:
        chat_id = message.chat.id
        qiwi_num = int(message.text)
        func.withdraw_sum_from_balanse(chat_id, sum_withdraw / 100 * (100 + config.withdraw_comission))
        func.create_withdraw(chat_id, sum_withdraw, qiwi_num, 1)
        bot.send_message(chat_id, "Выплата принята в обработку ожидайте подтверждения")
    except:
        error_message(message, bot)
def withdraw_btc(call, bot, user_data):
    chat_id = call.message.chat.id
    if func.check_unicless_withdraw(chat_id):
        mes = bot.send_message(chat_id, "Введите сумму вывода в RUB")
        bot.register_next_step_handler(mes, get_btc_sum_withdraw, bot = bot)
    else:
        bot.send_message(chat_id, "Ожидайте подтверждения предыдущего вывода, перед созданием новой заявки")
def get_btc_sum_withdraw(message, bot):
    try:
        chat_id = message.chat.id
        sum_withdraw = float(message.text)
        user_balanse = func.get_user_information(chat_id)[1]
        c = func.get_course_btc_rub()
        if sum_withdraw / 100 * (100 + config.withdraw_comission) <= user_balanse:
            sum_withdraw = sum_withdraw * c
            mes = bot.send_message(chat_id, "Введите BTC кошелек")
            bot.register_next_step_handler(mes, get_btc_num_withdraw, bot = bot, sum_withdraw = sum_withdraw)
        else:
            not_enough_money(message, bot, sum_withdraw)
    except:
        error_message(message, bot)
def get_btc_num_withdraw(message, bot, sum_withdraw):
    chat_id = message.chat.id
    btc_num = message.text
    func.withdraw_sum_from_balanse(chat_id, sum_withdraw / 100 * (100 + config.withdraw_comission))
    func.create_withdraw(chat_id, sum_withdraw, btc_num, 2)







def dice_game(message, bot):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Создайте новую игру или выберите из имеющихся", reply_markup = menu.gen_dice_game_kb()) 
def create_dice_game_step1(call, bot, user_data):
    chat_id = call.message.chat.id
    mes = bot.send_message(chat_id, "Введите сумму ставки в RUB")
    bot.register_next_step_handler(mes, create_dice_game_step2, bot = bot)
def create_dice_game_step2(message, bot):
    try:
        chat_id = message.chat.id
        user_balanse = func.get_user_information(chat_id)[1]
        sum_bet = float(message.text)
        if sum_bet / 100 * (100 + config.games_comission) <= user_balanse:
            if sum_bet >= config.min_sum_bet and sum_bet <= config.max_sum_bet:
                func.withdraw_sum_from_balanse(chat_id, sum_bet / 100 * (100 + config.games_comission))
                mes = bot.send_message(chat_id, "Выберите тип игры", reply_markup = menu.gen_dice_step3_kb(sum_bet))
            else:
                bot.send_message(chat_id, f"Минимальная сумма ставки - {config.min_sum_bet}\n\nМаксимальная сумма ставки - {config.max_sum_bet}")
        else:
            not_enough_money(message, bot, sum_bet)
    except:
        error_message(message, bot)
def create_dice_game_one_dice(call, bot, user_data):
    chat_id = call.message.chat.id
    sum_bet = float(user_data)
    mes = bot.send_message(chat_id, "Отправьте одним сообщением - 🎲")
    bot.register_next_step_handler(mes, get_value_one_dice_game, bot = bot, sum_bet = sum_bet)
def get_value_one_dice_game(message, bot, sum_bet):
    try:
        chat_id = message.chat.id
        value = message.dice.value
        game_hash = random.randint(1000000000000, 999999999999999)
        func.create_game(game_hash, sum_bet, chat_id, value, '🎲')
        for i in config.chats_ids:
            bot.send_message(i, f"🎲🎲 Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB \n\nИгра создана")
        bot.send_message(chat_id, f"🎲 Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB\n\n♠️ Вам выпало число - {value}\n\n✅ Игра создана")
        bot.send_message(chat_id, "Создайте новую игру или выберите из имеющихся", reply_markup = menu.gen_dice_game_kb()) 
    except:
        error_message(message, bot)
def create_dice_game_two_dice(call, bot, user_data):
    chat_id = call.message.chat.id
    sum_bet = float(user_data)
    mes = bot.send_message(chat_id, "Отправьте одним сообщением - 🎲")
    bot.register_next_step_handler(mes, get_value_firtht_dice_game, bot = bot, sum_bet = sum_bet)
def get_value_firtht_dice_game(message, bot, sum_bet):
    try:
        chat_id = message.chat.id
        value = message.dice.value
        mes = bot.send_message(chat_id, "Отправьте одним сообщением - 🎲")
        bot.register_next_step_handler(mes, get_value_second_dice_game, bot = bot, sum_bet = sum_bet, value = value)
    except:
        error_message(message, bot)
def get_value_second_dice_game(message, bot, sum_bet, value):    
    try:
        game_hash = random.randint(1000000000000, 999999999999999)
        chat_id = message.chat.id
        value = message.dice.value + value
        func.create_game(game_hash, sum_bet, chat_id, value, '🎲🎲')
        for i in config.chats_ids:
            bot.send_message(i, f"🎲🎲 Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB \n\nИгра создана")
        bot.send_message(chat_id, f"🎲🎲 Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB\n\n♠️ Вам выпало число - {value}\n\n✅ Игра создана")
        bot.send_message(chat_id, "Создайте новую игру или выберите из имеющихся", reply_markup = menu.gen_dice_game_kb()) 
    except:
        error_message(message, bot)
def create_dice_game_basketball_dice(call, bot, user_data):
    chat_id = call.message.chat.id
    sum_bet = float(user_data)
    mes = bot.send_message(chat_id, "Отправьте одним сообщением - 🏀")
    bot.register_next_step_handler(mes, get_value_basket_dice_game, bot = bot, sum_bet = sum_bet)
def get_value_basket_dice_game(message, bot, sum_bet):
    try:
        chat_id = message.chat.id
        value = message.dice.value
        game_hash = random.randint(1000000000000, 999999999999999)
        func.create_game(game_hash, sum_bet, chat_id, value, '🏀')
        bot.send_message(chat_id, f"🏀 Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB\n\n♠️ Вам выпало число - {value}\n\n✅ Игра создана")
        chat_id = message.chat.id
        bot.send_message(chat_id, "Создайте новую игру или выберите из имеющихся", reply_markup = menu.gen_dice_game_kb()) 
    except:
        error_message(message, bot)
def create_dice_game_darts_dice(call, bot, user_data):
    chat_id = call.message.chat.id
    sum_bet = float(user_data)
    mes = bot.send_message(chat_id, "Отправьте одним сообщением - 🎯")
    bot.register_next_step_handler(mes, get_value_darts_dice_game, bot = bot, sum_bet = sum_bet)
def get_value_darts_dice_game(message, bot, sum_bet):
    try:
        chat_id = message.chat.id
        value = message.dice.value
        game_hash = random.randint(1000000000000, 999999999999999)
        func.create_game(game_hash, sum_bet, chat_id, value, '🎯')
        bot.send_message(chat_id, f"🎯 Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB\n\n♠️ Вам выпало число - {value}\n\n✅ Игра создана")
        chat_id = message.chat.id
        bot.send_message(chat_id, "Создайте новую игру или выберите из имеющихся", reply_markup = menu.gen_dice_game_kb()) 
    except:
        error_message(message, bot)
def create_dice_game_football_dice(call, bot, user_data):
    chat_id = call.message.chat.id
    sum_bet = float(user_data)
    mes = bot.send_message(chat_id, "Отправьте одним сообщением - ⚽️")
    bot.register_next_step_handler(mes, get_value_football_dice_game, bot = bot, sum_bet = sum_bet)
def get_value_football_dice_game(message, bot, sum_bet):
    try:
        chat_id = message.chat.id
        game_hash = random.randint(1000000000000, 999999999999999)
        value = message.dice.value
        func.create_game(game_hash, sum_bet, chat_id, value, '⚽️')
        bot.send_message(chat_id, f"⚽️ Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB\n\n♠️ Вам выпало число - {value}\n\n✅ Игра создана")
        chat_id = message.chat.id
        bot.send_message(chat_id, "Создайте новую игру или выберите из имеющихся", reply_markup = menu.gen_dice_game_kb()) 
    except:
        error_message(message, bot)
def play_dice(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Выберите игру в которую хотите сыграть", reply_markup = menu.create_kb_dices())
def dice_game_call(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Создайте новую игру или выберите из имеющихся", reply_markup = menu.gen_dice_game_kb()) 
def get_game_information(call, bot, user_data):
    chat_id = call.message.chat.id
    game = func.get_dice_by_hash(user_data)
    bot.send_message(chat_id, f"{game[6]} Dice #{game[0]}\n\n💰 Сумма ставки {game[1]} RUB", reply_markup = menu.create_kb_play_dice(user_data))
def play_dice_step_1(call, bot, user_data):
    chat_id = call.message.chat.id
    sum_bet = func.get_dice_by_hash(user_data)[1]
    type = func.get_dice_by_hash(user_data)[6]
    user_balanse = func.get_user_information(chat_id)[1]
    if sum_bet / 100 * (100 + config.games_comission) <= user_balanse:
        if func.check_non_true_user(chat_id):
            if type != "🎲🎲":
                mes = bot.send_message(chat_id, f"Отправьте одним сообщением - {type}")
                bot.register_next_step_handler(mes, get_player_value_dice_game, bot = bot, game_hash = user_data)
            else:
                mes = bot.send_message(chat_id, "Отправьте одним сообщением - 🎲")
                bot.register_next_step_handler(mes, get_firtht_player_value_dice_game, bot = bot, game_hash = user_data)
        else:
            if type != "🎲🎲":
                player_value = func.get_dice_by_hash(user_data)[4]
                if player_value == 6:
                    play_non_true_user(chat_id, bot, user_data, 6)
                else:
                    play_non_true_user(chat_id, bot, user_data, player_value + 1)
            else:
                player_value = func.get_dice_by_hash(user_data)[4]
                if player_value == 12:
                    play_non_true_user(chat_id, bot, user_data, 12)
                else:
                    play_non_true_user(chat_id, bot, user_data, player_value + 1)
    else:
        not_enough_money(call.message, bot, sum_bet)
def get_firtht_player_value_dice_game(message, bot, game_hash):
    chat_id = message.chat.id
    player_value = message.dice.value
    mes = bot.send_message(chat_id, "Отправьте одним сообщением - 🎲")
    bot.register_next_step_handler(mes, get_second_player_value_dice_game, bot = bot, game_hash = game_hash, value = player_value)
def get_second_player_value_dice_game(message, bot, game_hash, value):
    chat_id = message.chat.id
    player_value = message.dice.value + value
    game = func.get_dice_by_hash(game_hash)
    func.withdraw_sum_from_balanse(chat_id, game[1] / 100 * (100 + config.games_comission))
    if game[4] > player_value:
        winner_message(game[2], game[1], game[4], player_value, game[6], game_hash, bot)
        lose_message(chat_id, game[1], player_value, game[4], game[6], game_hash, bot)
    elif game[4] < player_value:
        lose_message(game[2], game[1], game[4], player_value, game[6], game_hash, bot)
        winner_message(chat_id, game[1], player_value, game[4], game[6], game_hash, bot)
    elif game[4] == player_value:
        func.popoln_user_balanse(chat_id, game[1])
        func.popoln_user_balanse(game[2], game[1])
        bot.send_message(chat_id, f"{game[6]} Dice #{game[0]}\n\n Ничья")
        bot.send_message(game[2], f"{game[6]} Dice #{game[0]}\n\n Ничья")
    func.delete_dice_game_by_hash(game_hash)
def get_player_value_dice_game(message, bot, game_hash):
    chat_id = message.chat.id
    player_value = message.dice.value
    game = func.get_dice_by_hash(game_hash)
    func.withdraw_sum_from_balanse(chat_id, game[1] / 100 * (config.games_comission))
    if game[4] > player_value:
        winner_message(game[2], game[1], game[4], player_value, game[6], game_hash, bot)
        lose_message(chat_id, game[1], player_value, game[4], game[6], game_hash, bot)
    elif game[4] < player_value:
        lose_message(game[2], game[1], game[4], player_value, game[6], game_hash, bot)
        winner_message(chat_id, game[1], player_value, game[4], game[6], game_hash, bot)
    elif game[4] == player_value:
        func.popoln_user_balanse(chat_id, game[1])
        func.popoln_user_balanse(game[2], game[1])
        bot.send_message(chat_id, f"{game[6]} Dice #{game[0]}\n\n Ничья")
        bot.send_message(game[2], f"{game[6]} Dice #{game[0]}\n\n Ничья")
    func.delete_dice_game_by_hash(game_hash)
def winner_message(chat_id, sum_bet, value, vrag_value, type, game_hash, bot):
    bot.send_message(chat_id, f"{type} Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB\n\n👆 Ваше число {value}\n\n👇 Число соперника {vrag_value}\n\n✅Сумма выигрыша {sum_bet * 2} RUB")
    func.popoln_user_balanse(chat_id, sum_bet * 2)
    func.create_new_history(chat_id, game_hash, sum_bet * 2)
    func.update_user_count_games(chat_id)
    func.update_user_sum_games(chat_id, sum_bet * 2)
def lose_message(chat_id, sum_bet, value, vrag_value, type, game_hash, bot):
    bot.send_message(chat_id, f"{type} Dice #{game_hash}\n\n💰 Сумма ставки {sum_bet} RUB\n\n👆Число соперника {vrag_value}\n\n👇 Ваше число {value}\n\n❌Вы проиграли, повезет в следующий раз")
    func.create_new_history(chat_id, game_hash, 0)
    func.update_user_count_games(chat_id)
def help_dice(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, config.dice_help, reply_markup = menu.create_kb_retrun_main_dice())
def get_all_games(call, bot, user_data):
    chat_id = call.message.chat.id
    games = func.get_all_history(chat_id)
    mes = "Ваши игры:\n"
    for i in games:
        mes += f"Dice #{i[1]} Сумма выигрыша {i[2]}\n"
    bot.send_message(chat_id, mes, reply_markup = menu.create_kb_retrun_main_dice())
def get_rating(call, bot, user_data):
    chat_id = call.message.chat.id
    count, all_users_count = func.get_rating(chat_id)
    bot.send_message(chat_id, f"Вы занимаете {count} место 🏆 из {all_users_count} пользователей👥", reply_markup = menu.create_kb_retrun_main_dice())
def play_non_true_user(chat_id, bot, game_hash, value_non_true_user):
    player_value = value_non_true_user
    game = func.get_dice_by_hash(game_hash)
    func.withdraw_sum_from_balanse(chat_id, game[1] / 100 * (config.games_comission))
    if game[4] > player_value:
        winner_message(game[2], game[1], game[4], player_value, game[6], game_hash, bot)
        lose_message(chat_id, game[1], player_value, game[4], game[6], game_hash, bot)
    elif game[4] < player_value:
        lose_message(game[2], game[1], game[4], player_value, game[6], game_hash, bot)
        winner_message(chat_id, game[1], player_value, game[4], game[6], game_hash, bot)
    elif game[4] == player_value:
        func.popoln_user_balanse(chat_id, game[1])
        func.popoln_user_balanse(game[2], game[1])
        bot.send_message(chat_id, f"{game[6]} Dice #{game[0]}\n\n Ничья")
        bot.send_message(game[2], f"{game[6]} Dice #{game[0]}\n\n Ничья")
    func.delete_dice_game_by_hash(game_hash)



def update_user_balanse(call, bot, user_data):
    chat_id = call.message.chat.id
    mes = bot.send_message(chat_id, "Введите ID пользователя для обновления баланса")
    bot.register_next_step_handler(mes, update_user_balanse_step1, bot = bot) 
def update_user_balanse_step1(message, bot):
    try:
        chat_id = message.chat.id
        Id = int(message.text)
        mes = bot.send_message(chat_id, "Введите новую сумму баланса пользователя в рублях")
        bot.register_next_step_handler(mes, update_user_balanse_step2, bot = bot, Id = Id)
    except:
        error_message(message, bot)
def update_user_balanse_step2(message, bot, Id):
    try:
        sum_update = float(message.text)
        chat_id = message.chat.id
        func.update_user_balanse(Id, sum_update)
        usrname = bot.get_chat(Id).username
        bot.send_message(chat_id, f"Баланс пользователя @{usrname} Равен {sum_update} RUB")
        bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
    except:
        error_message(message, bot)
def ban_user(call, bot, user_data):
    chat_id = call.message.chat.id
    mes = bot.send_message(chat_id, "Введите ID пользователя для блокировки")
    bot.register_next_step_handler(mes, ban_user_step1, bot = bot)
def ban_user_step1(message, bot):
    try:
        chat_id = message.chat.id
        Id = int(message.text)
        func.add_user_to_ban(Id)
        usrname = bot.get_chat(Id).username
        bot.send_message(chat_id, f"Пользователь @{usrname} заблокирован")
        bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
    except:
        error_message(message, bot)
def unban_user(call, bot, user_data):
    chat_id = call.message.chat.id
    mes = bot.send_message(chat_id, "Введите ID пользователя для разблокировки")
    bot.register_next_step_handler(mes, unban_user_step1, bot = bot)
def unban_user_step1(message, bot):
    try:
        chat_id = message.chat.id
        Id = int(message.text)
        func.delete_user_from_ban(Id)
        usrname = bot.get_chat(Id).username
        bot.send_message(chat_id, f"Пользователь @{usrname} разблокирован")
        bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
    except:
        error_message(message, bot)
def send_messages_all_users(call, bot, user_data):
    chat_id = call.message.chat.id
    mes = bot.send_message(chat_id, "Введите сообщение для рассылки пользователям")
    bot.register_next_step_handler(mes, send_messages_all_users_step1, bot = bot)
def send_messages_all_users_step1(message, bot):
    chat_id = message.chat.id
    Users = func.get_all_users_inform()
    Count = 0
    try:
        for i in Users:
            i = i[0]
            Count = Count + 1
            if message.text != None:
                bot.send_message(i, message.text)
            elif message.photo != None:
                try:
                    file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    src= file_info.file_path 
                    with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                except Exception as e:
                    bot.reply_to(message,e )
                with open(src, 'rb') as f:
                    contents = f.read()
                if message.caption != None:
                    C = message.caption
                    bot.send_photo(i, contents, caption = C)
                else:
                    bot.send_photo(i, contents)
            elif message.video != None:
                try:
                    file_info = bot.get_file(message.video.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    src= file_info.file_path 
                    with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                except Exception as e:
                    bot.reply_to(message,e )
                with open(src, 'rb') as f:
                    contents = f.read()
                if message.caption != None:
                    C = message.caption
                    bot.send_video(i, contents, caption = C)
                else:
                    bot.send_video(i, contents)
    except:
        error_message(message)
    bot.send_message(chat_id, "Сообщение отправлено " + str(Count) + " пользователям")
    bot.send_message(chat_id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
def check_withdraws(call, bot, user_data):
    chat_id = call.message.chat.id
    withdraw = func.get_last_withdraw()
    if withdraw == 0:
        bot.send_message(chat_id, "Выводов нет")
    else:
        usrname = bot.get_chat(withdraw[0]).username
        type_withdraw = withdraw[3]
        if type_withdraw == 1:
            type_withdraw = "🥝 Qiwi"
        else:
            type_withdraw = "☢️ Bitcoin"
        bot.send_message(chat_id, f"Вывод от @{usrname}\n\nТип вывода {type_withdraw}\n\nСумма вывода {withdraw[1]}\n\nКошелек для вывода {withdraw[2]}", reply_markup = menu.gen_check_withdraw_kb(withdraw[0]))
def confirm_withdraw(call, bot, user_data):
    bot.send_message(user_data, "Ваша выплата произведена")
    bot.send_message(call.message.chat.id, "Вы подтвердили данную заявку на вывод")
    bot.send_message(call.message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
    func.delete_withdraw(user_data)
def delete_withdraw(call, bot, user_data):
    bot.send_message(user_data, "Ваша выплата удалена")
    bot.send_message(call.message.chat.id, "Вы подтвердили данную заявку на вывод")
    bot.send_message(call.message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
    func.delete_withdraw(user_data)
def add_no_true_user(call, bot, user_data):
    chat_id = call.message.chat.id
    mes = bot.send_message(chat_id, "Введите Id пользователя, у которого будет функция подкрутки")
    bot.register_next_step_handler(mes, get_id_non_true_user, bot = bot)
def get_id_non_true_user(message, bot):
    try:
        chat_id = message.chat.id
        Id = message.text
        func.add_non_true_user(Id)
        username = bot.get_chat(Id).username
        bot.send_message(chat_id, f"Теперь пользователь @{username} будет выигрывать")
        bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
    except:
        error_message(message, bot)
def delete_non_true_user(call, bot, user_data):
    chat_id = call.message.chat.id
    mes = bot.send_message(chat_id, "Введите Id пользователя, у которого будет недоступна функция подкрутки")
    bot.register_next_step_handler(mes, delete_non_true_user_step1, bot = bot)
def delete_non_true_user_step1(message, bot):
    try:
        chat_id = message.chat.id
        Id = message.text
        func.delete_non_true_user(Id)
        username = bot.get_chat(Id).username
        bot.send_message(chat_id, f"Теперь пользователь @{username} не будет выигрывать")
        bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
    except:
        error_message(message, bot)
def get_last_message_support(call, bot, user_data):
    chat_id = call.message.chat.id
    quetion = func.get_last_quetion()
    if quetion != 0:
        username = bot.get_chat(quetion[0]).username
        bot.send_message(chat_id, f"Вопрос от @{username}\n\nСам вопрос {quetion[1]}", reply_markup = menu.answer_quetion_support(quetion[0]))
    else:
        bot.send_message(chat_id, "Вопросов нет")
        bot.send_message(call.message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
def delete_quetion(call, bot, user_data):
    chat_id = call.message.chat.id
    quetion = func.get_last_quetion()
    username = bot.get_chat(quetion[0]).username
    func.delete_quetion(quetion[0])
    bot.send_message(quetion[0], "Ваш запрос в поддержку был удален")
    bot.send_message(chat_id, f"Вы удалили вопрос от @{username}")
    bot.send_message(call.message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
def answer_quetion(call, bot, user_data):
    chat_id = call.message.chat.id
    username = bot.get_chat(user_data).username
    mes = bot.send_message(chat_id, f"Введите ответ на вопрос от @{username}")
    bot.register_next_step_handler(mes, answer_quetion_step1, bot = bot, user_id = user_data)
def answer_quetion_step1(message, bot, user_id):
    chat_id = message.chat.id
    answer = message.text
    quetion = func.get_last_quetion()
    func.delete_quetion(quetion[0])
    username = bot.get_chat(quetion[0]).username
    bot.send_message(quetion[0], f"На ваш вопрос в поддержку был дан ответ\n\nВопрос:{quetion[1]}\n\nОтвет:{answer}")
    bot.send_message(chat_id, f"Вы ответили на вопрос вопрос от @{username}")
    bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
def add_answer(call, bot, message):
    chat_id = call.message.chat.id
    mes = bot.send_message(chat_id, "Введите вопрос")
    bot.register_next_step_handler(mes, add_answer_step1, bot = bot)
def add_answer_step1(message, bot):
    chat_id = message.chat.id
    quetion = message.text
    mes = bot.send_message(chat_id, "Введите ответ на вопрос")
    bot.register_next_step_handler(mes, add_answer_step2, bot = bot, quetion = quetion)
def add_answer_step2(message, bot, quetion):
    chat_id = message.chat.id
    hash = random.randint(1000000000000, 999999999999999)
    answer = message.text
    func.create_answer(hash, quetion, answer)
    bot.send_message(chat_id, "Вопрос создан")
    bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())
def delete_answer(call, bot, user_data):
    chat_id = call.message.chat.id
    answers = func.get_all_answers()
    mes = "Введите хэш вопроса, который вы хотите удалить:\n"
    for i in answers:
        mes += str(i[0]) + " " + str(i[1]) + "\n"
    mes = bot.send_message(chat_id, mes)
    bot.register_next_step_handler(mes,delete_answer_step1, bot = bot)
def delete_answer_step1(message, bot):
    chat_id = message.chat.id
    func.delete_answer(message.text)
    bot.send_message(chat_id, "Вопрос удален")
    bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = menu.gen_admin_kb())

def main_support(message, bot):
    chat_id = message.chat.id
    bot.send_message(chat_id, '❓Бот работает полностью в автоматическом режиме. Перед написанием сообщения в службу поддержки просьба ознакомиться с разделом "Ответы на вопросы"', reply_markup = menu.gen_support_kb())
def rules(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, config.rules_bot, reply_markup = menu.return_support())
def support_call(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, '❓Бот работает полностью в автоматическом режиме. Перед написанием сообщения в службу поддержки просьба ознакомиться с разделом "Ответы на вопросы"', reply_markup = menu.gen_support_kb())
def create_support(call, bot, user_data):
    chat_id = call.message.chat.id
    if func.check_unik_quetion(chat_id):
        bot.register_next_step_handler(bot.send_message(chat_id, "Введите ваш вопрос, пожалуйста", reply_markup = menu.return_support()), get_support_message, bot = bot)
    else:
        bot.send_message(chat_id, "Перед созданием нового вопроса дождитесь ответ на старый")
def get_support_message(message, bot):
    chat_id = message.chat.id
    func.create_support_quetion(chat_id, message.text)
    bot.send_message(chat_id, "Ваш вопрос отослан в поддержку, ожидайте ответа в течении 3-х дней")
    bot.send_message(chat_id, '❓Бот работает полностью в автоматическом режиме. Перед написанием сообщения в службу поддержки просьба ознакомиться с разделом "Ответы на вопросы"', reply_markup = menu.gen_support_kb())
def get_answers_message(call, bot, user_data):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Выберите вопрос, который вас интересует", reply_markup = menu.create_answers_kb())
def get_answer(call, bot, user_data):
    chat_id = call.message.chat.id
    answer = func.get_answer_by_hash(user_data)
    bot.send_message(chat_id, f"Вопрос: {answer[1]}\n\nОтвет на вопрос {answer[2]}", reply_markup = menu.create_return_answers_kb())

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
