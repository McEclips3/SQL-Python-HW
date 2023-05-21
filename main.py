from SQLclass import Sql

if __name__ == '__main__':
    table = Sql()
    # table.delete_table()
    # table.create_table()
    # table.add_client('вася', 'пупкин', 'vasia@pupkin.ru')
    # table.add_client('валя', 'петрова', 'валя собака')
    # table.add_phone(1, 89119119191)
    # table.add_phone(2, 89219212121)
    # table.update_client('петя', 'васин', 'петя собака', 1)
    # table.delete_phone(1)
    # table.delete_client(1)
    table.find_client(name='валя')
    table.find_client(surname='петрова')
    table.find_client(email='валя собака')
    table.find_client(phone='89119119191')




