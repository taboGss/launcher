import sqlite3

def create_data_base(name_db):
    conn = sqlite3.connect(name_db)
    conn.commit()

    cursor = conn.cursor()
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


