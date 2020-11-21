#!/usr/bin/python3.6
import sqlite3
def make_connect():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    return conn, cursor
def create_tables():
    conn, cursor = make_connect()
    try:
        cursor.execute("CREATE TABLE users(user_id INTEGER, bal FLOAT, count_games INTEGER, sum_games FLOAT, ref_id INTEGER, ref_sum FLOAT)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE qiwi_popoln(user_id INTEGER, sum FLOAT, phone INTEGER, random_code INTEGER)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE withdraw(user_id INTEGER, sum FLOAT, num TEXT, type INTEGER)")
    except:
        pass
    try:
         cursor.execute("CREATE TABLE dice(hash INTEGER, sum_bet FLOAT, creator_user_id INTEGER, player_user_id INTEGER, creator_value INTEGER, player_value INTEGER, type TEXT)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE history_dice(user_id INTEGER, hash INTEGER, sum_win FLOAT)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE ban(user_id INTEGER, S INTEGER)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE nontrueusers(user_id INTEGER, S INTEGER)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE quetions(hash TEXT, quetion TEXT, answer TEXT)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE support(user_id INTEGER, quetion TEXT)")
    except:
        pass
