# Визуализатор графа зависимостей

Этот проект представляет собой инструмент командной строки для визуализации графов зависимостей пакетов Python, включая их транзитивные зависимости. Вывод предоставляется в формате Mermaid для легкого представления в графической форме.

## Особенности

- Чтение зависимостей пакетов из указанного текстового файла.
- Поддержка визуализации транзитивных зависимостей.
- Вывод графа зависимостей в текстовом формате для удобной проверки.
- Генерация графических представлений графа зависимостей.

## Использование

Чтобы запустить визуализатор, выполните следующую команду в терминале:

```bash
python visual.py
```

Вы увидите вывод в консоли в формате Mermaid, а графическое представление графа зависимостей будет отображено в файле graph.png в текущей директории.

## Пример

Учитывая следующий dependencies.txt:

```text
matplotlib:
  - contourpy
  - cycler
  - fonttools
  - kiwisolver
  - numpy
  - packaging
  - pillow
  - pyparsing
  - python-dateutil
  - meson-python
  - pybind11!
  - setuptools_scm
  - setuptools
```

И файл config.json, указывающий:
```json
{
    "package_name": "matplotlib",
    "output_graph_file": "graph.mmd",
    "repository_path": "./"
} 
```

Запуск скрипта выведет:

    Граф сохранен в graph.mmd
    graph TD
        matplotlib --> contourpy
        matplotlib --> python-dateutil
        matplotlib --> pyparsing
        matplotlib --> kiwisolver
        matplotlib --> packaging
        matplotlib --> pillow
        matplotlib --> fonttools
        matplotlib --> setuptools_scm
        matplotlib --> cycler
        matplotlib --> meson-python
        matplotlib --> setuptools
        matplotlib --> numpy
        matplotlib --> pybind11!



