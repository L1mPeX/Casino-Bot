#!/usr/bin/python3.6
from telebot import types
import func
import config
def gen_main_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = 2)
    markup.row("👤Мой профиль", "💼Баланс")
    markup.row("🎲Игры", "🐼Поддержка")
    return markup
def gen_refer_kb():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "👥Реферальная система", callback_data = "referal_system user_data"),
        )
    return markup
def gen_ref_system_kb():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "🐼Как это работает", callback_data = "referal_system_how_it_works user_data"),
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "return_profile user_data"),
        )
    return markup
def gen_return_referal_system_how_it_works():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "referal_system user_data"),
        )
    return markup
def gen_balanse_kb():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "📥Пополнить баланс", callback_data = "popoln user_data"),
        types.InlineKeyboardButton(text = "📤Вывести средства", callback_data = "withdraw user_data"),
        )
    return markup
def gen_popoln_plateg_sys_kb():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "🥝Qiwi", callback_data = "popoln_qiwi user_data"),
        types.InlineKeyboardButton(text = "☢️Bitcoin", callback_data = "popoln_btc user_data"),
        )
    return markup
def gen_withdraw_plateg_sys_kb():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "🥝Qiwi", callback_data = "withdraw_qiwi user_data"),
        types.InlineKeyboardButton(text = "☢️Bitcoin", callback_data = "withdraw_btc user_data"),
        )
    return markup
def gen_check_popoln():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "🔁Проверить оплату", callback_data = "check_qiwi user_data"),
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "return_balanse_kb user_data"),
        )
    return markup
def gen_check_btc_kb(adress):
    markup= types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "Проверить поступившие платежи🔁", callback_data ="check_bitcoin user_data " + str(adress))
    )
    return markup
def gen_dice_game_kb():
    markup= types.InlineKeyboardMarkup(row_width = 2)
    markup.add(
        types.InlineKeyboardButton(text = "❇️Создать игру", callback_data = "create_dice_game user_data"),
        types.InlineKeyboardButton(text = "💠Сыграть в игры", callback_data = "play_dice_game user_data"),
        types.InlineKeyboardButton(text = "📝Мои игры", callback_data = "my_dice_games user_data"),
        types.InlineKeyboardButton(text = "🏆Рейтинг", callback_data = "dice_rating user_data"),
        types.InlineKeyboardButton(text = "🐼Помощь", callback_data = "help_dice user_data"),
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "return_profile user_data"),
        )
    return markup
def gen_dice_step3_kb(sum_bet):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(text = "🎲Один кубик", callback_data = f"one_dice user_data {sum_bet}"),
        types.InlineKeyboardButton(text = "🎲🎲Два кубика", callback_data = f"two_dice user_data {sum_bet}"),
        types.InlineKeyboardButton(text = "🏀Баскетбол", callback_data = f"basket_ball_dice user_data {sum_bet}"),
        types.InlineKeyboardButton(text = "🎯Дартс", callback_data = f"darts_dice user_data {sum_bet}"),
        types.InlineKeyboardButton(text = "⚽️Футбол", callback_data = f"football_dice user_data {sum_bet}"),
        )
    return markup
def create_kb_dices():
    dices = func.get_all_dice()
    markup = types.InlineKeyboardMarkup(row_width = 1)
    for i in dices:
        markup.add(
            types.InlineKeyboardButton(text = f"{i[6]} {i[1]} RUB", callback_data = f"get_dice_info user_data {i[0]}")
            )
    markup.add(
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "main_menu_game user_data")
        )
    return markup
def create_kb_play_dice(hash):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
         types.InlineKeyboardButton(text = "🎮Сыграть", callback_data = f"play_dice_game_1 user_data {hash}"),
         types.InlineKeyboardButton(text = "↩️Назад", callback_data = "play_dice_game user_data"),
        )
    return markup
def create_kb_retrun_main_dice():
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "main_menu_game user_data")
        )
    return markup
def gen_admin_kb():
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(text = "🤑 Обновить баланс пользователю", callback_data = "update_user_balanse user_data"),
        types.InlineKeyboardButton(text = "🚫Заблокировать пользователя", callback_data = "ban_user user_data"),
        types.InlineKeyboardButton(text = "☑️Разблокировать пользователя", callback_data = "unban user_data"),
        types.InlineKeyboardButton(text = "📨Рассылка сообщений", callback_data = "send_messages_to_chat user_data"),
        types.InlineKeyboardButton(text = "ℹ️Ответить на сообщение в поддержку", callback_data = "support_otv user_data"),
        types.InlineKeyboardButton(text = "🆕Добавить ответ на вопрос", callback_data = "add_quetion user_data"),
        types.InlineKeyboardButton(text = "🛑Удалить ответ на вопрос", callback_data = "delete_quetion user_data"),
        types.InlineKeyboardButton(text = "💵Просмотреть выводы и подтвердить их", callback_data = "check_withdraws user_data"),
        types.InlineKeyboardButton(text = "🆕Добавить пользователя в список подкрутчиков", callback_data = "add_no_true_user user_data"),
        types.InlineKeyboardButton(text = "🚫Удалить пользователя из списка подкрутчиков", callback_data = "delete_non_true_user user_data"),
        )
    return markup
def gen_check_withdraw_kb(checking_user_id):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(text = "✔️ Подтвердить выплату", callback_data = f"confirmwithdraw user_data {checking_user_id}"),
        types.InlineKeyboardButton(text = "🛑 Удалить выплату", callback_data = f"delete_withdraw user_data {checking_user_id}"),
        )
    return markup
def gen_support_kb():
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(text = "✉️Служба поддержки", callback_data = "support user_data"),
        types.InlineKeyboardButton(text = "💾Ответы на вопросы", callback_data = "answers user_data"),
        types.InlineKeyboardButton(text = "📃Правила", callback_data = "rules user_data"),
        types.InlineKeyboardButton(text = "🗯Чат", url = config.chat_link),
        types.InlineKeyboardButton(text = "👍Отзывы", url = config.votes_link),
        )
    return markup
def return_support():
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "return_support user_data"),
        )
    return markup
def answer_quetion_support(user_id):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(text = "🔖 Ответить на вопрос", callback_data = f"answer_support_quetion user_data {user_id}"),
        types.InlineKeyboardButton(text = "❌ Удалить вопрос", callback_data = f"delete_quetion_support user_data {user_id}"),
        )
    return markup
def create_answers_kb():
    answers = func.get_all_answers()
    markup = types.InlineKeyboardMarkup(row_width = 1)
    for i in answers:
        markup.add(
            types.InlineKeyboardButton(text = str(i[1]), callback_data = f"get_answer user_data {i[0]}")
            )
    markup.add(
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "return_support user_data"),
        )
    return markup
def create_return_answers_kb():
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(text = "↩️Назад", callback_data = "answers user_data"),
        )
    return markup

            
            
            
            
