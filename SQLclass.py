import psycopg2


class Sql:
    def __init__(self):
        self.connection = psycopg2.connect(database='hwsqlpy', user='postgres', password='postgres')
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def commit_and_close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def delete_table(self):
        cur = self.cursor
        cur.execute("""
                    DROP TABLE phone;
                    DROP TABLE client;
                    """)
        self.commit_and_close()
        return print('Таблицы удалены')

    def create_table(self):
        cur = self.cursor
        cur.execute("""
                CREATE TABLE IF NOT EXISTS client(
                    client_id SERIAL PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    surname VARCHAR(40) NOT NULL,
                    email VARCHAR(40) NOT NULL UNIQUE
                    );
                """)

        cur.execute("""
                   CREATE TABLE IF NOT EXISTS phone(
                       phone_id SERIAL PRIMARY KEY,
                       client_id INTEGER NOT NULL REFERENCES client(client_id),
                       phone BIGINT
                   );
                   """)
        self.commit_and_close()
        return print('Таблица создана')

    def add_client(self, name, surname, email):
        cur = self.cursor
        cur.execute("""INSERT INTO client(name, surname, email) VALUES(%s, %s, %s) RETURNING client_id, name;
            """, (name, surname, email))
        self.connection.commit()
        print(cur.fetchone())
        self.close()

    def add_phone(self, client_id, phone):
        cur = self.cursor
        cur.execute("""INSERT INTO phone(client_id, phone) VALUES(%s, %s) RETURNING phone_id, phone;
            """, (client_id, phone))
        self.connection.commit()
        print(cur.fetchone())
        self.close()

    def delete_phone(self, client_id):
        cur = self.cursor
        cur.execute("""DELETE FROM phone 
            WHERE client_id=%s;
                """, (client_id,))
        self.commit_and_close()
        print('Телефон удален')

    def find_client(self, name=None, surname=None, email=None, phone=None):
        cur = self.cursor
        if name and surname:
            cur.execute("""SELECT c.client_id, name, surname, email, p.phone FROM client c
                           LEFT JOIN phone p ON c.client_id = p.client_id
                           WHERE name=%s AND surname=%s;""", (name, surname,))
        elif email:
            cur.execute("""SELECT c.client_id, name, surname, email, p.phone FROM client c
                            LEFT JOIN phone p ON c.client_id = p.client_id
                            WHERE email=%s;""", (email,))
        elif phone:
            cur.execute("""SELECT c.client_id, name, surname, email, p.phone FROM client c
                           LEFT JOIN phone p ON c.client_id = p.client_id
                           WHERE phone=%s;""", (phone,))
        print(cur.fetchall())
        self.close()

    def update_client(self, name=None, surname=None, email=None, phone=None):
        cur = self.cursor
        if name and surname:
            cur.execute("""SELECT c.client_id, name, surname, email, p.phone FROM client c
                           LEFT JOIN phone p ON c.client_id = p.client_id
                           WHERE name=%s AND surname=%s;""", (name, surname,))
        elif email:
            cur.execute("""SELECT c.client_id, name, surname, email, p.phone FROM client c
                            LEFT JOIN phone p ON c.client_id = p.client_id
                            WHERE email=%s;""", (email,))
        elif phone:
            cur.execute("""SELECT c.client_id, name, surname, email, p.phone FROM client c
                           LEFT JOIN phone p ON c.client_id = p.client_id
                           WHERE phone=%s;""", (phone,))
        client = cur.fetchall()[0]
        client_id = client[0]
        name = client[1]
        surname = client[2]
        email = client[3]
        phone = client[4]
        phone_check = client[4]
        new_name = input('Введите новое имя клиента или оставьте поле пустым, если не хотите менять имя.')
        if new_name != '':
            name = new_name
        new_surname = input('Введите новую фамилию клиента или оставьте поле пустым, если не хотите менять фамилию.')
        if new_surname != '':
            surname = new_surname
        new_email = input('Введите новый email клиента или оставьте поле пустым, если не хотите менять email.')
        if new_email != '':
            email = new_email
        new_phone = input('Введите новый номер телефона клиента или оставьте поле пустым, если не хотите менять номер.')
        if new_phone != '':
            phone = new_phone
        print(name, surname, email, phone, 'test')
        cur.execute("""
                UPDATE client SET name=%s, surname=%s, email=%s WHERE client_id=%s RETURNING client_id, name;
                """, (name, surname, email, client_id))
        print(cur.fetchall())
        if phone_check is not None:
            cur.execute("""
                UPDATE phone SET phone=%s
                WHERE client_id=%s 
                RETURNING client_id, phone
                ;
                """, (phone, client_id))
        else:
            cur.execute("""INSERT INTO phone(client_id, phone) VALUES(%s, %s) RETURNING phone_id, phone;
                """, (client_id, phone))
        self.connection.commit()
        print(cur.fetchall())
        self.close()

    def delete_client2(self, client_id):
        cur = self.cursor
        cur.execute("""SELECT c.client_id, name, surname, email, p.phone FROM client c
                           LEFT JOIN phone p ON c.client_id = p.client_id
                           WHERE c.client_id=%s;""", (client_id,))
        client = cur.fetchall()[0]
        phone_check = client[4]
        if phone_check is not None:
            cur.execute("""DELETE FROM phone 
                           WHERE client_id=%s;
                           """, (client_id,))
            cur.execute("""DELETE FROM client
                           WHERE client_id=%s;
                           """, (client_id,))
            self.commit_and_close()
        else:
            cur.execute("""DELETE FROM client
                           WHERE client_id=%s;
                           """, (client_id,))
            self.commit_and_close()
        print('Клиент удален')
