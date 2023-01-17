import sys


FILE_TXT = 'users.txt'
CMD_CREATE = 'create'
CMD_UPDATE = 'update'
CMD_VIEW = 'view'
CMD_DELETE = 'delete'


def get_params():
    # python x.py -m pass create serge1 asd1
    # tokens = sys.argv[3:]

    # python x.py -m create serge1 asd1
    try:
        tokens = sys.argv[2:]
        command_name = tokens[0]
        username = tokens[1]
        if command_name in (CMD_CREATE, CMD_UPDATE):
            password = tokens[2]
            return command_name, username, password
        elif command_name in (CMD_VIEW, CMD_DELETE):
            return command_name, username
    except (IndexError, ValueError) as e:
        raise Exception(f'Bad params, exception: {e}.')
    except Exception:
        raise Exception('Bad params.')


def run_command(params, data):
    try:
        command_name = params[0]
        username = params[1]
        if command_name == CMD_CREATE:
            password = params[2]
            data = create_user(data, username, password)

        elif command_name == CMD_UPDATE:
            new_password = params[2]
            data = update_user(data, username, new_password)

        elif command_name == CMD_VIEW:
            retrieve_user(data, username)

        elif command_name == CMD_DELETE:
            data = delete_user(data, username)

        save_data(data)
    except Exception as e:
        print(f'Ошибка: {e}')


def retrieve_user(data, username):
    if check_user_existence(data, username):
        print(f'У пользователя {username} пароль: {data[username]}')
    else:
        raise Exception(f'Пользователя {username} не существует.')


def check_user_existence(data, username):
    if username in data:
        return True
    else:
        return False


def create_user(data, username, password):
    if not check_user_existence(data, username):
        data[username] = password
    return data


def update_user(data, username, new_password):
    if not check_user_existence(data, username):
        raise Exception(f'Пользователя {username} не существует.')
    for username in data:
        data[username] = new_password
    return data


def delete_user(data, username):
    if not check_user_existence(data, username):
        raise Exception(f'Пользователя {username} не существует.')
    data.pop(username)
    return data


def load_data():
    with open(FILE_TXT, 'r') as f:
        s = f.read()
        d = dict()
        for line in s.split('\n'):
            if line != '':
                s1 = line.strip()
                l, p = s1.split(':')
                d[l] = p
        return d


def save_data(data):
    d = data
    strings = ''
    for k, v in d.items():
        strings += f'{k}:{v}\n'
    with open(FILE_TXT, 'w') as f:
        f.write(strings)


def init_data():
    f = open(FILE_TXT, 'w')
    f.close()


def main():
    try:
        params = get_params()
        data = load_data()
        run_command(params, data)
    except FileNotFoundError:
        print(f'Невозможно открыть файл {FILE_TXT}')
        init_data()
        print(f'Создан файл {FILE_TXT}')
    except Exception as e:
        print(f'Unknown error: {e}.')


if __name__ == '__main__':
    main()
