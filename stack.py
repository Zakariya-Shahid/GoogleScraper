import sqlite3

conn = sqlite3.connect('cnpj.db')
c = conn.cursor()

# creating a table with only one column 'link'
c.execute('''CREATE TABLE IF NOT EXISTS links
                (id integer primary key autoincrement, link text, status integer default 0)''')


def appendLink(link):
    # adding the link into the table if the link does not exist in the table
    c.execute("SELECT * FROM links WHERE link = ?", (link,))
    if c.fetchone() is None:
        c.execute("INSERT OR IGNORE INTO links VALUES (?, ?, 0)", (None, link))
        conn.commit()
    else:
        pass


def getLink(id):
    # getting all the links from the table
    c.execute("SELECT * FROM links WHERE id = ? AND status = 0", (id,))
    return c.fetchall()


def deleteLink(id):
    # updating the status of the link to 1
    c.execute("UPDATE links SET status = 1 WHERE id = ?", (id,))
    conn.commit()


def getLinksLength():
    # getting the length of the table
    c.execute("SELECT COUNT(*) FROM links WHERE status = 0")
    return c.fetchone()[0]


if __name__ == "__main__":
    appendLink("=========================")
    print(getLink(1))
    deleteLink(1)
    print(getLinksLength())
