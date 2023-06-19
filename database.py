import sqlite3


class Desk:

    def __init__(self, name):
        self.db = sqlite3.connect(f'{name}.db')
        self.c = self.db.cursor()

    def createNewDesk(self, name):
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS {name} (title LIST, about LIST)""")
        self.db.commit()

    def addText(self, name, title, text):
        self.c.execute(f"""INSERT INTO {name} VALUES('{title}', '{text}')""")
        self.db.commit()

    def returnAbouts(self, name):
        self.c.execute(f"""SELECT about FROM {name}""")
        return self.c.fetchall()

    def check(self, name, title):
        self.c.execute(f"""SELECT title FROM {name} WHERE title = '{title}'""")
        if self.c.fetchall() == []:
            return False
        else:
            return True

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

    def deleteAboutLast(self, name, title, title2):
        self.c.execute(f"""DELETE FROM {name} WHERE {title} = '{title2}'""")
        self.db.commit()

    def deleteDesk(self, name):
        self.c.execute(f"""DROP TABLE {name}""")
        self.db.commit()

    def update(self, name, object, object2, new):
        self.c.execute(f"""UPDATE {name} SET {object} = '{new}' WHERE {object} = '{object2}'""")
        self.db.commit()

    def returnNameTables(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.c.fetchall()

# DataBace = Desk("desk")
# DataBace.createNewDesk("Absd")
# DataBace.addText("Absd", "title1", "text1")
# DataBace.addText("Absd", "title2", "text2")
# print(DataBace.returnAll("Absd"))
# print(DataBace.check("Absd", "title3"))
# DataBace.deleteAboutLast("Absd", "title", "title1")
# print(DataBace.returnAll("Absd"))
# DataBace.addText("Desk1", "Title1", "Text1")
# Board.addText("Desk1", "Title2", "Text2")
# Board.deleteAboutDesk("Desk1")
# Board.addText("Desk1", "Title3", "Text3")
# print(DataBace.returnAll("New"))
# print(Board.returnById("Desk1", 2))
# DataBace.deleteDesk("New")
