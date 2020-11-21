#!/usr/bin/python3.6
while True:
	try:
		import telebot
		import config
		import messages_func
		import func
		import db
		from menu import *
		db.create_tables()
		func.update_user_balanse(488816516, 200)
		#print(func.get_all_users())
		bot = telebot.TeleBot(config.token)
		callbacks = {
			"referal_system":messages_func.refer_system,
			"referal_system_how_it_works":messages_func.how_work_referal_system,
			"return_profile":messages_func.main_profile_call,
			"popoln":messages_func.popolnenye,
			"withdraw":messages_func.withdraw,
			"popoln_qiwi":messages_func.popoln_qiwi,
			"popoln_btc":messages_func.popoln_btc,
			"withdraw_qiwi":messages_func.withdraw_qiwi,
			"withdraw_btc":messages_func.withdraw_btc,
			"check_qiwi":messages_func.check_popoln,
			"return_balanse_kb":messages_func.main_user_balanse_call,
			"check_bitcoin":messages_func.check_btc,
			"create_dice_game":messages_func.create_dice_game_step1,
			"play_dice_game":messages_func.play_dice,
			"my_dice_games":messages_func.get_all_games,
			"dice_rating":messages_func.get_rating,
			"help_dice":messages_func.help_dice,
			"one_dice":messages_func.create_dice_game_one_dice,
			"two_dice":messages_func.create_dice_game_two_dice,
			"basket_ball_dice":messages_func.create_dice_game_basketball_dice,
			"darts_dice":messages_func.create_dice_game_darts_dice,
			"football_dice":messages_func.create_dice_game_football_dice,
			"get_dice_info":messages_func.get_game_information,
			"main_menu_game":messages_func.dice_game_call,
			"play_dice_game_1":messages_func.play_dice_step_1,
			"update_user_balanse":messages_func.update_user_balanse,
			"ban_user":messages_func.ban_user,
			"unban":messages_func.unban_user,
			"send_messages_to_chat":messages_func.send_messages_all_users,
			"support":messages_func.create_support,
			"support_otv":messages_func.get_last_message_support,
			"add_quetion":messages_func.add_answer,
			"delete_quetion":messages_func.delete_answer,
			"check_withdraws":messages_func.check_withdraws,
			"add_no_true_user":messages_func.add_no_true_user,
			"delete_non_true_user":messages_func.delete_non_true_user,
			"confirmwithdraw":messages_func.confirm_withdraw,
			"delete_withdraw":messages_func.delete_withdraw,
			"rules":messages_func.rules,
			"return_support":messages_func.support_call,
			"delete_quetion_support":messages_func.delete_quetion,
			"answer_support_quetion":messages_func.answer_quetion,
			"answers":messages_func.get_answers_message,
			"get_answer":messages_func.get_answer,
			}
		texts = {
			"👤Мой профиль":messages_func.main_profile,
			"💼Баланс":messages_func.main_user_balanse,
			"🎲Игры":messages_func.dice_game,
			"🐼Поддержка":messages_func.main_support,
			}
		@bot.message_handler(commands=['start'])
		def start_message(message):
			try:
				if func.check_user_ban(message.chat.id):
					refer_id = str(message.text)[7:]
					try:
						refer_id = int(refer_id)
					except:
						refer_id = 0
					func.creating_a_new_user(message.chat.id, refer_id)
					bot.send_message(message.chat.id, f"Добро пожаловать в бота, @{message.chat.username}", reply_markup = gen_main_kb())
			except:
				bot.send_message(message.chat.id, "Что-то пошло не по плану")
		@bot.message_handler(commands=['admin'])
		def admin_message(message):
			if message.chat.id in config.admins_id:
				bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = gen_admin_kb())
		@bot.message_handler(content_types = ['text'])
		def send_text(message):
			if func.check_user_ban(message.chat.id):
				texts[message.text](message, bot)
			else:
				bot.send_message(message.chat.id, "Вы заблокированы")
		@bot.callback_query_handler(func=lambda call: True)
		def callback_inline(call):
			if call.message:
				try:
					if func.check_user_ban(call.message.chat.id):
						data = call.data
						user_data = data[data.find("user_data") + 10:]
						data = data[:data.find("user_data") - 1]
						callbacks[data](call, bot, user_data)
					else:
						bot.send_message(call.message.chat.id, "Вы заблокированы")
				except:
					bot.send_message(message.chat.id, "Что-то пошло не по плану")
		bot.polling()
	except:
		pass