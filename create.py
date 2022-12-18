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
            return command_name, (username, password)
        elif command_name in (CMD_VIEW, CMD_DELETE):
            return command_name, username
    except (IndexError, ValueError) as e:
        raise Exception(f'Bad params, exception: {e}.')
    except Exception:
        raise Exception('Bad params.')


def run_command(params, f):
    try:
        command_name = params[0]
        if command_name == CMD_CREATE:
            username = params[1][0]
            password = params[1][1]
            create_user(f, username, password)
            print(f'Создан пользователь {username}')
        elif command_name == CMD_UPDATE:
            username = params[1][0]
            new_password = params[1][1]
            update_user(f, username, new_password)
        elif command_name == CMD_VIEW:
            username = params[1]
            retrieve_user(f, username)
        elif command_name == CMD_DELETE:
            username = params[1]
            delete_user(f, username)
    except Exception as e:
        print(f'Ошибка: {e}')


def retrieve_user(f, username):
    if check_user_existence(f, username):
        password = get_user_password(f, username)
        print(f'У пользователя {username} пароль: {password}!')
    else:
        raise Exception(f'Пользователя {username} не существует.')


def check_user_existence(f, username):
    lines = f.readlines()
    for line in lines:
        if line.startswith(f'{username}:'):
            return True
    return False


def create_user(f, username, password):
    if check_user_existence(f, username):
        raise Exception(f'Пользователь {username} уже существует')
    f.write(f'{username}:{password}\n')


def get_user_password(f, username):
    password = None
    raw_users = f.readlines()
    for raw_user in raw_users:
        if raw_user.startswith(f'{username}:'):
            password = raw_user.replace('\n', '').split(':')[1]
            break
    return password


def update_user(f, username, new_password):
    if not check_user_existence(f, username):
        raise Exception(f'Пользователя {username} не существует.')
    lines = f.readlines()
    for line in lines:
        if line.startswith(f'{username}:'):
            index = lines.index(line)
            lines.pop(index)
    lines.append(f'{username}:{new_password}\n')
    f.write(''.join(lines))


def delete_user(f, username):
    if not check_user_existence(f, username):
        raise Exception(f'Пользователя {username} не существует.')
    lines = f.readlines()
    for line in lines:
        if line.startswith(f'{username}:'):
            index = lines.index(line)
            lines.pop(index)
    f.write(''.join(lines))


def init_file():
    f = open(FILE_TXT, 'w+')
    return f


def main():
    try:
        f = init_file()
        params = get_params()
        run_command(params, f)
    except FileNotFoundError:
        print(f'Невозможно открыть файл {FILE_TXT}')
    except Exception as e:
        print(f'Unknown error: {e}.')


if __name__ == '__main__':
    main()
