import psycopg2


class Sql:
    def __init__(self):
        self.connection = psycopg2.connect(database='hwsqlpy', user='postgres', password='postgres')

    def delete_table(self):
        conn = self.connection
        with conn.cursor() as cur:
            cur.execute("""
                    DROP TABLE phone;
                    DROP TABLE client;
                    """)
            conn.commit()
        conn.close()
        return print('Таблицы удалены')

    def create_table(self):
        conn = self.connection
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS client(
                    client_id SERIAL PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    surname VARCHAR(40) NOT NULL,
                    email VARCHAR(40) NOT NULL
                    );
                """)

            cur.execute("""
                   CREATE TABLE IF NOT EXISTS phone(
                       phone_id SERIAL PRIMARY KEY,
                       client_id INTEGER NOT NULL REFERENCES client(client_id),
                       phone BIGINT
                   );
                   """)
            conn.commit()
        conn.close()
        return print('Таблица создана')

    def add_client(self, name, surname, email):
        conn = self.connection
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO client(name, surname, email) VALUES(%s, %s, %s) RETURNING client_id, name;
            """, (name, surname, email))
            conn.commit()
            print(cur.fetchone())
        conn.close()

    def add_phone(self, client_id, phone):
        conn = self.connection
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO phone(client_id, phone) VALUES(%s, %s) RETURNING phone_id, phone;
            """, (client_id, phone))
            conn.commit()
            print(cur.fetchone())
        conn.close()

    def update_client(self, name, surname, email, client_id):
        conn = self.connection
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE client SET name=%s, surname=%s, email=%s WHERE client_id=%s RETURNING client_id, name;
                """, (name, surname, email, client_id))
            conn.commit()
            print(cur.fetchone())
        conn.close()

    def delete_phone(self, client_id):
        conn = self.connection
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM phone 
            WHERE client_id=%s;
                """, (client_id,))
            conn.commit()
        conn.close()
        print('Телефон удален')

    def delete_client(self, client_id):
        conn = self.connection
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM client WHERE client_id=%s;
        """, (client_id,))
            conn.commit()
            print('Клиент удален')
        conn.close()

    def find_client(self, name=None, surname=None, email=None, phone=None):
        conn = self.connection
        with conn.cursor() as cur:
            cur.execute("""SELECT c.client_id, name, surname, email, p.phone FROM client c
                JOIN phone p ON c.client_id = p.client_id
                WHERE name=%s OR surname=%s OR email=%s OR phone=%s
                GROUP BY c.client_id, p.phone;""", (name, surname, email, phone))
            print(cur.fetchall())
