import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "promo" (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        number text NOT NULL,
        amount integer NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "keyboard" (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        text text NOT NULL UNIQUE,
        show integer NOT NULL
        )
        ''')

        try:
          with self.connection:
            self.cursor.execute('''
                              INSERT INTO 'keyboard' ('id' ,'text','show') VALUES (?, ?, ?)
                              ''', (7, 'Купить промокод 7 дней (220р)', 1,))

          
            self.cursor.execute('''
                              INSERT INTO 'keyboard' ('id' ,'text','show') VALUES (?, ?, ?)
                              ''', (14, 'Купить промокод 14 дней (380р)', 1,))

            self.cursor.execute('''
                              INSERT INTO 'keyboard' ('id' ,'text','show') VALUES (?, ?, ?)
                              ''', (30, 'Купить промокод 30 дней (760р)', 1,))
          
            self.cursor.execute('''
                              INSERT INTO 'keyboard' ('id' ,'text','show') VALUES (?, ?, ?)
                              ''', (60, 'Купить промокод 60 дней (1300р)', 1,))
        except sqlite3.IntegrityError:
            pass
    def add_product(self, amount, number):
        with self.connection:
            for i in range(len(number)):
              self.cursor.execute("INSERT INTO 'promo' ('amount','number') VALUES (?, ?)", (amount, str(number[i]),))      

    def del_product(self, number):
        with self.connection:
            self.cursor.execute("DELETE FROM promo WHERE number = ?", (number,))

    def new_buy(self, amount):
        with self.connection:
            number = str(self.cursor.execute("SELECT number FROM promo WHERE amount = ?", (amount,)).fetchone()).split("'")[1]

            self.cursor.execute("DELETE FROM promo WHERE number = ?", (number,))
            return number

    def check_remain(self, amount):
        with self.connection:
            return len(self.cursor.execute("SELECT number FROM promo WHERE amount = ?", (amount,)).fetchall())

    def check_promo(self):
        with self.connection:
            if len(self.cursor.execute("SELECT * FROM promo").fetchall()) != 0:
                return True
            else:
                return False
            
    def showed_gifts(self):
        with self.connection:
            return self.cursor.execute("SELECT text FROM keyboard where show = 1").fetchall()
    
    def hide_gifts(self, id):
        with self.connection:
            return self.cursor.execute("UPDATE keyboard SET show = 0 WHERE id = ?", (id,)).fetchall()
        
    def show_gifts(self, id):
        with self.connection:
            return self.cursor.execute("UPDATE keyboard SET show = 1 WHERE id = ?", (id,)).fetchall()