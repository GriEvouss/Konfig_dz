from unittest import removeResult

import toml
import os
import time


# Чтение конфигурационного файла
def load_config(filename):
    with open(filename, 'r') as f:
        config = toml.load(f)
    return config


# Команды эмулятора
class Emulator:
    def __init__(self, username, hostname):
        self.username = username
        self.hostname = hostname
        self.history = []

    def execute_command(self, command):
        self.history.append(command)
        if command == "exit":
            return False
        elif command == "ls":
            return "\n".join(os.listdir('.'))
        elif command.startswith("cd "):
            path = command.split(" ")[1]
            try:
                os.chdir(path)
                return f"Перешли в {path}"
            except FileNotFoundError:
                return f"Не удалось найти путь: {path}"
            except NotADirectoryError:
                return f"{path} не является директорией"
            except PermissionError:
                return f"Нет доступа к {path}"
        elif command == "history":
            return "\n".join(self.history)
        elif command == "date":
            return time.strftime("%Y-%m-%d %H:%M:%S")
        elif command == "rev":
            return "\n".join(reversed(self.history))
        else:
            return "Неизвестная команда"


    def prompt(self):
        return f"{self.username}@{self.hostname}$ "

    def execute_startup_commands(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                commands = file.readlines()
                for command in commands:
                    command = command.strip()  # Удаляем пробелы и символы новой строки
                    self.execute_command(command)
        else:
            return f"Файл {filepath} не найден."

def main():
    # Загрузка конфигурацииda
    config = load_config('config.toml')

    # Инициализация эмулятора
    emulator = Emulator(config["username"], config["hostname"])

    # Выполнение команд из стартового скрипта
    startup_result = emulator.execute_startup_commands(config["startup_script"])
    if startup_result:
        print(startup_result)

    # Основной цикл
    while True:
        command = input(emulator.prompt())
        result = emulator.execute_command(command)
        if result is False:
            print("Выход из программы.")
            break
        elif result:
            print(result)


if __name__ == "__main__":
    main()