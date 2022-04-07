from dis import Instruction
import sqlite3

def create_data_base(name_db):
    conn = sqlite3.connect(name_db)
    conn.commit()

    cursor = conn.cursor()

    if table_exits(name_db, 'statusScripts'):
        clean_data_base(name_db)
    
    else:
        cursor.execute(
            """ CREATE TABLE statusScripts (
                script text,
                pid integer,
                rtsp text,
                status integer
            )"""
        )

    conn.commit()
    conn.close()

def insertRow(name_db, script, pid, rtsp, status):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    instruccion = f"INSERT INTO statusScripts VALUES ('{script}', {pid}, '{rtsp}', {status})" 
    cursor.execute(instruccion)

    conn.commit()
    conn.close()

def update_status(name_db, pid, status):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    instruccion = f"UPDATE statusScripts SET status={status} WHERE pid like {pid}"
    cursor.execute(instruccion)

    conn.commit()
    conn.close()

def table_exits(name_db, name_tb):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    instruccion = f"SELECT count(name) from sqlite_master WHERE type='table' AND name='{name_tb}'"
    cursor.execute(instruccion)

    already_exists = cursor.fetchone()[0] == 1

    conn.commit()
    conn.close()

    return already_exists

def clean_data_base(name_db):
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    instruccion = f"DELETE FROM statusScripts"
    cursor.execute(instruccion)

    conn.commit()
    conn.close()



