import json
import os
from collections import defaultdict
import requests


# Чтение конфигурационного файла
def read_config(config_file='config.json'):
    with open(config_file, 'r') as file:
        return json.load(file)


# Получение зависимостей пакета с сайта PyPI
def fetch_dependencies_from_pypi(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        package_info = response.json()
        dependencies = package_info.get('info', {}).get('requires_dist', [])
        return [dep.split(';')[0].split()[0].strip() for dep in dependencies if dep]
    else:
        print(f"Ошибка при получении данных для {package_name}")
        return []


# Запись зависимостей в файл
def write_dependencies_to_file(dependencies, filename='dependencies.txt'):
    with open(filename, 'w') as file:
        for package, deps in dependencies.items():
            file.write(f"{package}:\n")
            for dep in deps:
                # Удаляем версии и условия из строки зависимости
                dep_cleaned = dep.split('[')[0].split('=')[0].split('<')[0].split('>')[0].strip()
                file.write(f"  - {dep_cleaned}\n")


# Чтение зависимостей из файла
def read_dependencies(dependencies_file='dependencies.txt'):
    dependencies = defaultdict(list)
    with open(dependencies_file, 'r') as file:
        current_package = None
        for line in file:
            line = line.strip()
            if line.endswith(':'):
                current_package = line[:-1]
            elif line.startswith('-') and current_package:
                dependencies[current_package].append(line[1:].strip())
    return dependencies


# Получение транзитивных зависимостей
def get_transitive_dependencies(package_name, dependencies):
    transitive_deps = set()

    def recurse(package):
        for dep in dependencies.get(package, []):
            if dep not in transitive_deps:
                transitive_deps.add(dep)
                recurse(dep)

    recurse(package_name)
    return transitive_deps


# Построение и визуализация графа в формате Mermaid
def visualize_graph(package_name, dependencies):
    transitive_deps = get_transitive_dependencies(package_name, dependencies)
    graph_lines = ["graph TD"]
    for dep in transitive_deps:
        graph_lines.append(f"    {package_name} --> {dep}")
    mermaid_code = "\n".join(graph_lines)

    # Сохранение в файл
    output_file = "graph.mmd"
    with open(output_file, "w") as f:
        f.write(mermaid_code)

    print(f"Граф сохранен в {output_file}")
    return mermaid_code


# Основная функция
def main():
    config = read_config()
    package_name = config['package_name']
    dependencies = defaultdict(list)

    # Получение зависимостей
    dependencies[package_name] = fetch_dependencies_from_pypi(package_name)
    write_dependencies_to_file(dependencies)

    # Чтение зависимостей из файла и построение графа
    dependencies = read_dependencies()
    graph_output = visualize_graph(package_name, dependencies)
    print(graph_output)


if __name__ == "__main__":
    main()
