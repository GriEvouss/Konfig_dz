# Конвертер конфигурационного языка

        Разработать инструмент командной строки для учебного конфигурационного
    языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
    входного формата в выходной. Синтаксические ошибки выявляются с выдачей
    сообщений.
        Входной текст на языке json принимается из файла, путь к которому задан
    ключом командной строки. Выходной текст на учебном конфигурационном
    языке попадает в стандартный вывод
## Использование

Чтобы использовать инструмент, выполните файл `config_tool.py`, указав путь к вашему JSON-файлу в качестве аргумента командной строки:
```
python config_tool.py <путь_к_json_файлу>
```
----
## Примеры 
### Команда 
    python config_tool.py fatalconfig.json
### Входной JSON файл () 
```json
{
    "APP_NAME": "MyApplication",
    "VERSION": 1.0,
    "SETTINGS": {
        "DEBUG": true,
        "LOG_LEVEL": "info"
    }
}
```
### Вывод программы
    struct {
        APP_NAME = "MyApplication",
        VERSION = 1.0,
        SETTINGS =     struct {
            DEBUG = True,
            LOG_LEVEL = "info",
        },
    }

---
### Команда 
    python config_tool.py config.json
### Входной JSON файл с операциями ()
```json
{
    "PROJECT_NAME": "NewProject",
    "VERSION": 0.1,
    "CONST_SUM": "? 3 + 5",
    "CONST_PI": 3.14,
    "CONST_SQRT_TWO": "sqrt 2",
    "ENABLE_NOTIFICATIONS": false
}
```
### Вывод программы

    struct {
        PROJECT_NAME = "NewProject",
        VERSION = 0.1,
        SUM <- 8.0,
        PI <- 3.14,
        SQRT_TWO <- 1.4142135623730951,
        ENABLE_NOTIFICATIONS = False,
    }
-----
### Команда 
    python config_tool.py project_management_config.json
### Входной JSON файл для системы управления проектами
```json
{
    "PROJECT_NAME": "NewProject",
    "VERSION": 0.1,
    "TEAM_MEMBERS": [
        "Alice",
        "Bob",
        "Charlie"
    ],
    "TASKS": {
        "TOTAL": 10,
        "COMPLETED": 4,
        "PENDING": 6
    },
    "ENABLE_NOTIFICATIONS": false
}

```
### Вывод программы
    struct {
        PROJECT_NAME = "NewProject",
        VERSION = 0.1,
        TEAM_MEMBERS = "Alice", "Bob", "Charlie",
        TASKS =     struct {
            TOTAL = 10,
            COMPLETED = 4,
            PENDING = 6,
        },
        ENABLE_NOTIFICATIONS = False,
    }

---
### Команда 
    python config_tool.py web_app_config.json
### Входной JSON файл для веб-приложения
```json
{
    "APP_NAME": "MyWebApp",
    "VERSION": 1.2,
    "DATABASE": {
        "HOST": "localhost",
        "PORT": 5432,
        "USERNAME": "admin",
        "PASSWORD": "password"
    },
    "DEBUG": true,
    "LOG_LEVEL": "info"
}

```
### Вывод программы
    struct {
        APP_NAME = "MyWebApp",
        VERSION = 1.2,
        DATABASE =     struct {
            HOST = "localhost",
            PORT = 5432,
            USERNAME = "admin",
            PASSWORD = "password",
        },
        DEBUG = True,
        LOG_LEVEL = "info",
    }


