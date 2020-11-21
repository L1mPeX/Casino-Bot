#!/usr/bin/python3.6
from db import make_connect
import requests, json
from config import *
from bs4 import BeautifulSoup
from lxml import html
def check_user_unicless(user_id):
    conn, cursor = make_connect()
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id, ))
    return cursor.fetchone()[0] == 0
def creating_a_new_user(user_id, refer_id):
    if check_user_unicless(user_id):
        conn, cursor = make_connect()
        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?)", (user_id, welcome_bonus, 0, 0, refer_id, 0))
        conn.commit()
def get_user_information(user_id):
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, ))
    return cursor.fetchone()
def update_user_balanse(user_id, new_balanse):
    conn, cursor = make_connect()
    cursor.execute("UPDATE users SET bal = ? WHERE user_id = ?", (new_balanse, user_id))
    conn.commit()
def create_qiwi_popoln(user_id, sum, phone, random_code):
    conn, cursor = make_connect()
    cursor.execute("INSERT INTO qiwi_popoln VALUES(?,?,?,?)", (user_id, sum, phone, random_code))
    conn.commit()
def get_last_popoln(user_id):
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM qiwi_popoln WHERE user_id = ?", (user_id, ))
    return cursor.fetchone()
def delete_last_popoln(user_id):
    conn, cursor = make_connect()
    cursor.execute("DELETE FROM qiwi_popoln WHERE user_id = ?", (user_id, ))
    conn.commit()
def popoln_user_balanse(user_id, sum):
    user_balanse = get_user_information(user_id)[1] + sum
    update_user_balanse(user_id, user_balanse)
def check_qiwi_repl(user_id):
    result = get_last_popoln(user_id)
    phone = result[2]
    sum = result[1]
    random_code = result[3]
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + qiwi_api
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+qiwi_num+'/payments?rows=50')
    req = json.loads(h.text)
    for i in range(len(req['data'])):
        if req['data'][i]['account'] == phone:
            if req['data'][i]['comment'] == random_code:
                if req['data'][i]['sum']['amount'] == sum:
                    popoln_user_balanse(user_id, sum)
                    delete_last_popoln(user_id)
                    return True
    return  False
def create_new_coinbase_plateg():
    s = requests.Session()
    s.headers['X-CC-Api-Key'] = apibtc
    s.headers['Content-Type'] = "application/json"
    s.headers['X-CC-Version'] = "2018-03-22"
    params = {"name":"Name1", "description":"fuiwhf", "pricing_type":"no_price"}
    h = s.post("https://api.commerce.coinbase.com/charges", params = params)
    req = json.loads(h.text)
    adress = req['data']['addresses']['bitcoin']
    return adress
def get_all_bitcoin_trans():
    s = requests.Session()
    s.headers['X-CC-Api-Key'] = apibtc
    s.headers['X-CC-Version'] = "2018-03-22"
    h = s.get('https://api.commerce.coinbase.com/charges')
    req = json.loads(h.text)
    count = req['pagination']['total']
    payments_with_adress = []
    for i in range(count):
        adress = req['data'][i]['addresses']['bitcoin']
        payments = req['data'][i]['payments']
        payment_with_adress = (adress, payments)
        payments_with_adress.append(payment_with_adress)
    return payments_with_adress
def get_sum_payments_from_adress(btc_adress):
    payments = get_all_bitcoin_trans()
    sum_pay = 0.0
    for i in payments:
        if i[0] == btc_adress:
            for j in i[1]:
                if j['status'] == "CONFIRMED":
                    sum_pay += j['crypto']['amount']
            return sum_pay
def get_course_btc_rub():
    url = "https://www.google.com/search?q=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D1%80%D1%83%D0%B1%D0%BB%D1%8C&oq=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D1%80%D1%83%D0%B1%D0%BB%D1%8C&aqs=chrome..69i57j0l7.2557j1j7&sourceid=chrome&ie=UTF-8"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'lxml')
    course = soup.find('span', {'class': 'DFlfde SwHCTb'})
    course = float(course.get("data-value"))
    return course
def withdraw_sum_from_balanse(user_id, sum_withdraw):
    user_balanse = get_user_information(user_id)[1] - sum_withdraw
    update_user_balanse(user_id, user_balanse)
def create_withdraw(user_id, sum, num, type):
    conn, cursor = make_connect()
    cursor.execute("INSERT INTO withdraw VALUES(?,?,?,?)", (user_id, sum, num, type))
    conn.commit()
def create_game(game_hash, sum_bet, creator_user_id, creator_value, type):
    #hash INTEGER, sum_bet FLOAT, creator_user_id INTEGER, player_user_id INTEGER, creator_value INTEGER, player_value INTEGER, type TEXT)
    conn, cursor = make_connect()
    cursor.execute("INSERT INTO dice VALUES (?,?,?,?,?,?,?)", (game_hash, sum_bet, creator_user_id, 0, creator_value, 0, type))
    conn.commit()
def get_all_dice():
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM dice")
    return cursor.fetchall()
def get_dice_by_hash(game_hash):
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM dice WHERE hash = ?", (game_hash, ))
    return cursor.fetchone()
def delete_dice_game_by_hash(game_hash):
    conn, cursor = make_connect()
    cursor.execute("DELETE FROM dice WHERE hash = ?", (game_hash, ))
    conn.commit()
def create_new_history(user_id, game_hash, sum_win):
    conn, cursor = make_connect()
    cursor.execute("INSERT INTO history_dice VALUES (?,?,?)", (user_id, game_hash, sum_win))
    conn.commit()
def get_all_history(user_id):
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM history_dice WHERE user_id = ?", (user_id, ))
    return cursor.fetchall()
def get_all_users_inform():
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
def get_rating(chat_id):
    users_inform = get_all_users_inform()
    average_check = []
    count = 0
    for user_inform in users_inform:
        user_id = user_inform[0]
        user_count_games = user_inform[2]
        user_sum_games = user_inform[3]
        try:
           user_average_check = user_sum_games / user_count_games
        except:
           user_average_check = 0.0
        user_information = {"user_id":user_id, "user_average_check":user_average_check}
        average_check.append(user_information)
    for i in average_check:
        for j in average_check:
            if i["user_average_check"] > j["user_average_check"]:
                tmp = i
                i = j
                j = i
    for i in range(len(average_check)):
        if average_check[i]["user_id"] != chat_id:
            count = i
    count += 1
    all_users_count = len(average_check)
    return count, all_users_count
def update_user_count_games(user_id):
    conn, cursor = make_connect()
    count_games = get_user_information(user_id)[2] + 1
    cursor.execute("UPDATE users SET count_games = ? WHERE user_id = ?", (count_games, user_id,))
    conn.commit()
def update_user_sum_games(user_id, sum):
    conn, cursor = make_connect()
    sum_games = get_user_information(user_id)[3] + sum
    cursor.execute("UPDATE users SET sum_games = ? WHERE user_id = ?", (sum_games, user_id,))
    conn.commit()
def add_user_to_ban(user_id):
    conn, cursor = make_connect()
    cursor.execute("INSERT INTO ban VALUES (?,?)", (user_id, 0))
    conn.commit()
def check_user_ban(user_id):
    conn, cursor = make_connect()
    cursor.execute("SELECT COUNT(*) FROM ban WHERE user_id = ?", (user_id, ))
    return cursor.fetchone()[0] == 0
def delete_user_from_ban(user_id):
    conn, cursor = make_connect()
    cursor.execute("DELETE FROM ban WHERE user_id = ?", (user_id,))
    conn.commit()
def check_unicless_withdraw(user_id):
    conn, cursor = make_connect()
    cursor.execute("SELECT COUNT(*) FROM withdraw WHERE user_id = ?", (user_id, ))
    return cursor.fetchone()[0] == 0
def get_last_withdraw():
    try:
        conn, cursor = make_connect()
        cursor.execute("SELECT * FROM withdraw")
        return cursor.fetchall()[0]
    except:
        return 0
def delete_withdraw(user_id):
    conn, cursor = make_connect()
    cursor.execute("DELETE FROM withdraw WHERE user_id = ?", (user_id, ))
    conn.commit()
def add_non_true_user(user_id):
    conn, cursor = make_connect()
    cursor.execute("INSERT INTO nontrueusers VALUES (?,?)", (user_id, 0))
    conn.commit()
def check_non_true_user(user_id):
    conn, cursor = make_connect()
    cursor.execute("SELECT COUNT(*) FROM nontrueusers WHERE user_id = ?", (user_id, ))
    return cursor.fetchone()[0] == 0
def delete_non_true_user(user_id):
    conn, cursor = make_connect()
    cursor.execute("DELETE FROM nontrueusers WHERE user_id = ?", (user_id,))
    conn.commit()
def create_support_quetion(user_id, quetion):
    conn, cursor = make_connect()
    cursor.execute("INSERT INTO support VALUES (?,?)", (user_id, quetion))
    conn.commit()
def check_unik_quetion(user_id):
    conn, cursor = make_connect()
    cursor.execute("SELECT COUNT(*) FROM support WHERE user_id = ?", (user_id, ))
    return cursor.fetchone()[0] == 0
def get_last_quetion():
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM support")
    try:
        return cursor.fetchall()[0]
    except:
        return 0
def delete_quetion(user_id):
    conn, cursor = make_connect()
    cursor.execute("DELETE FROM support WHERE user_id = ?", (user_id,))
    conn.commit()
def get_all_answers():
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM quetions")
    return cursor.fetchall()
def create_answer(hash, quetion, answer):
    conn, cursor = make_connect()
    cursor.execute("INSERT INTO quetions VALUES (?,?,?)", (hash, quetion, answer, ))
    conn.commit()
def delete_answer(hash):
    conn, cursor = make_connect()
    cursor.execute("DELETE FROM quetions WHERE hash = ?", (hash,))
    conn.commit()
def get_answer_by_hash(hash):
    conn, cursor = make_connect()
    cursor.execute("SELECT * FROM quetions WHERE hash = ?", (hash,))
    return cursor.fetchone()
