import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import math
import argparse


def read_config(config_file):
    """
    Чтение конфигурации из XML файла.

    Аргументы:
    config_file (str): Путь к XML файлу конфигурации.

    Возвращает:
    dict: Словарь с параметрами n0, h, nk, a, b, c.
    """
    tree = ET.parse(config_file)
    root = tree.getroot()

    config = {
        'n0': float(root.find('n0').text),
        'h': float(root.find('h').text),
        'nk': float(root.find('nk').text),
        'a': float(root.find('a').text),
        'b': float(root.find('b').text),
        'c': float(root.find('c').text)
    }

    return config


def compute_y(x, a, b, c):
    """
    Вычисление значения функции y(x).

    Аргументы:
    x (float): Значение x.
    a (float): Параметр a.
    b (float): Параметр b.
    c (float): Параметр c.

    Возвращает:
    float: Вычисленное значение y(x).
    """
    return a * (math.sin(x) ** 2) + b * math.sin(x) + c


def write_results(results_file, results):
    """
    Запись результатов вычислений в XML файл с форматированием.

    Аргументы:
    results_file (str): Путь к файлу для записи результатов.
    results (list): Список кортежей (x, y), содержащих результаты вычислений.
    """
    root = ET.Element("results")

    for x, y in results:
        result_elem = ET.SubElement(root, "result")
        x_elem = ET.SubElement(result_elem, "x")
        y_elem = ET.SubElement(result_elem, "y")

        x_elem.text = str(x)
        y_elem.text = str(y)

    # Создание строки из XML-дерева
    rough_string = ET.tostring(root, 'utf-8')

    # Использование minidom для форматирования
    reparsed = minidom.parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    # Запись форматированного XML в файл
    with open(results_file, "w", encoding='utf-8') as f:
        f.write(pretty_xml_as_string)


def run(config_file="config.xml", results_file="results.xml"):
    """
    Функция для автоматического запуска вычислений без аргументов командной строки.

    Аргументы:
    config_file (str): Путь к файлу конфигурации (по умолчанию 'config.xml').
    results_file (str): Путь к файлу для записи результатов (по умолчанию 'results.xml').
    """
    config = read_config(config_file)
    n0 = config['n0']
    h = config['h']
    nk = config['nk']
    a = config['a']
    b = config['b']
    c = config['c']

    # Вычисление значений
    x = n0
    results = []
    while x <= nk:
        y = compute_y(x, a, b, c)
        results.append((x, y))
        x += h

    # Запись результатов в файл
    write_results(results_file, results)


def main():
    """
    Основная функция для запуска программы через консольные аргументы или автоматически.
    """
    parser = argparse.ArgumentParser(description="Вычисление y(x) на заданном диапазоне.")
    parser.add_argument("config", nargs='?', default=None, help="Путь к XML файлу конфигурации")
    parser.add_argument("output", nargs='?', default=None, help="Путь к XML файлу для записи результатов")

    args = parser.parse_args()

    if args.config and args.output:
        # Запуск через консольные аргументы
        run(args.config, args.output)
    else:
        # Автоматический запуск (значения по умолчанию)
        print("Запуск с параметрами по умолчанию")
        run()


if __name__ == "__main__":
    main()
