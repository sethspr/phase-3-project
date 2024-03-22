# lib/config.py
import sqlite3

CONN = sqlite3.connect('users.db')
CURSOR = CONN.cursor()