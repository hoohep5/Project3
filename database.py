import sqlite3

class Desk:

    def __init__(self, name):
        self.db = sqlite3.connect(f'{name}.db')
        self.c = self.db.cursor()

    def createNewDesk(self, name):
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS {name} (title TEXT, about TEXT)""")
        self.db.commit()

    def addText(self, name, title, text):
        self.c.execute(f"""INSERT INTO {name} VALUES('{title}', '{text}')""")
        self.db.commit()

    def returnAbouts(self, name):
        self.c.execute(f"""SELECT about FROM {name}""")
        return self.c.fetchall()

    def returnTitles(self, name):
        self.c.execute(f"""SELECT title FROM {name}""")
        return self.c.fetchall()

    def returnById(self, name, id):
        self.c.execute(f"""SELECT * FROM {name} WHERE rowid = {id}""")
        return self.c.fetchall()

    def returnAll(self, name):
        self.c.execute(f"""SELECT * FROM {name}""")
        return self.c.fetchall()

    def deleteAboutDesk(self, name):
        self.c.execute(f"""DELETE FROM {name}""")
        self.db.commit()
    def deleteDesk(self, name):
        self.c.execute(f"""DROP TABLE {name}""")
        self.db.commit()

    def update(self, name, object, new):
        self.c.execute(f"""UPDATE {name} SET {object} = {new}""")
        self.db.commit()

    def returnNameTables(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.c.fetchall()

#Board = Desk("desk1")
#Board.createNewDesk("Desk1")
#Board.addText("Desk1", "Title1", "Text1")
#Board.addText("Desk1", "Title2", "Text2")
#Board.deleteAboutDesk("Desk1")
#Board.addText("Desk1", "Title3", "Text3")
#print(Board.returnAll("Desk1"))
#print(Board.returnById("Desk1", 2))
#Board.deleteDesk("Desk1")
