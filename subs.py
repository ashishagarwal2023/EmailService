import sqlite3

DB_PATH="./store.db"


def executeSQL(sql, params=None):
    conn = sqlite3.connect(DB_PATH,timeout=1)
    cursor = conn.cursor()
    if params == None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, params)
    conn.commit()
    cursor.close()
    conn.close()
    return True



def addSubscriber(subscriber_email):
    sql = "INSERT INTO subs (email) VALUES (?)"
    try:
        executeSQL(sql, (subscriber_email,))
    except sqlite3.IntegrityError as e:
        print(e)
        return False
    return True


def addSubscriber(subscriber_email):
    sql = "INSERT INTO subs (email) VALUES (?)"
    try:
        executeSQL(sql, (subscriber_email,))
    except sqlite3.IntegrityError as e:
        print(e)
        return False
    return True


def removeSubscriber(email):
    sql = "DELETE FROM subs WHERE email = ?"
    try:
        executeSQL(sql, (email,))
    except Exception as e:
        print(e)
        return False
    return True


def getAllSubs():
    conn = sqlite3.connect(DB_PATH,timeout=1)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subs")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
def getEmails():
    def executeSQLQ(sql):
        conn = sqlite3.connect(DB_PATH,timeout=1)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # Select all rows from the subs table
    sql = "SELECT email FROM subs"
    subs = executeSQLQ(sql)
    return [sub[0] for sub in subs]
# print(getEmails())

# print(addSubscriber("coqade.with.aasheesh@gmail.com"))
# print(addSubscriber("codqe.with.aasheesh@gmail.com"))
# print(addSubscriber("co2de.with.aasheesh@gmail.com"))
# print(addSubscriber("co3de.with.aasheesh@gmail.com"))
# print(addSubscriber("co4de.with.aasheesh@gmail.com"))
# print(addSubscriber("co3de.with.aasheesh@gmail.com"))


# print(removeSubscriber("code.with.aasheesh@gmail.com"))
# print(getAllSubs())
