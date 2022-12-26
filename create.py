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


def run_command(params, data):
    try:
        command_name = params[0]
        if command_name == CMD_CREATE:
            username = params[1][0]
            password = params[1][1]
            data = create_user(data, username, password)

        elif command_name == CMD_UPDATE:
            username = params[1][0]
            new_password = params[1][1]
            data = update_user(data, username, new_password)

        elif command_name == CMD_VIEW:
            username = params[1]
            retrieve_user(data, username)

        elif command_name == CMD_DELETE:
            username = params[1]
            data = delete_user(data, username)

        save_data(data)
    except Exception as e:
        print(f'Ошибка: {e}')


def retrieve_user(data, username):
    if check_user_existence(data, username):
        password = get_user_password(data, username)
        print(f'У пользователя {username} пароль: {password}!')
    else:
        raise Exception(f'Пользователя {username} не существует.')


def check_user_existence(data, username):
    lines = data.split('\n')
    for line in lines:
        if line.startswith(f'{username}:'):
            return True
    return False


def create_user(data, username, password):
    if not check_user_existence(data, username):
        data += f'{username}:{password}\n'
    return data


def get_user_password(data, username):
    password = None
    raw_users = data.split('\n')
    for raw_user in raw_users:
        if raw_user.startswith(f'{username}:'):
            password = raw_user.split(':')[1]
            break
    return password


def update_user(data, username, new_password):
    if not check_user_existence(data, username):
        raise Exception(f'Пользователя {username} не существует.')

    lines = data.split('\n')
    for line in lines:
        if line.startswith(f'{username}:'):
            index = lines.index(line)
    lines.pop(index)

    data = '\n'.join(lines)
    data = create_user(data, username, new_password)
    return data


def delete_user(data, username):
    if not check_user_existence(data, username):
        raise Exception(f'Пользователя {username} не существует.')

    lines = data.split('\n')
    for line in lines:
        if line.startswith(f'{username}:'):
            index = lines.index(line)
    lines.pop(index)

    data = '\n'.join(lines)
    return data


def load_data():
    try:
        with open(FILE_TXT, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f'Невозможно открыть файл {FILE_TXT}')


def save_data(data):
    try:
        with open(FILE_TXT, 'w') as f:
            f.write(data)
    except FileNotFoundError:
        print(f'Невозможно открыть файл {FILE_TXT}')


def main():
    try:
        data = load_data()
        params = get_params()
        run_command(params, data)
    except Exception as e:
        print(f'Unknown error: {e}.')


if __name__ == '__main__':
    main()
