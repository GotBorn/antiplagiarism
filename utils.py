import ast


def del_dockstrings(tree: ast.Module) -> ast.Module:
    """Удаляет из дерева комментарии и docstring, возвращая очищенное синтаксическое дерево

    Args:
        tree (ast.Module): исходное синтаксическое дерево

    Returns:
        ast.Module: очищенное синтаксическое дерево
    """
    for node in ast.walk(tree):
        # https://docs.python.org/3/library/ast.html#ast.get_docstring
        # согласно документации, docstring может быть только у 4 классов ниже
        if (isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and
                len(node.body) != 0 and isinstance(node.body[0], ast.Expr) and
                hasattr(node.body[0], 'value') and isinstance(node.body[0].value, ast.Str)):
            node.body = node.body[1:]

    return tree


def del_spaces_and_newlines(code: str) -> str:
    """Удаляет из кода пробелы и переносы строк

    Args:
        code (str): Код с пробелами и переходами на новую строку

    Returns:
        str: Очищенный код без пробелов и в одну строку
    """
    return code.replace('\n', '').replace(' ', '')


def preprocess_text(code: str) -> str:
    """Предобработка кода программы

    Args:
        code (str): Код программмы, который надо предобработать

    Returns:
        str: Очищенный от комментариев, докстрингов и пробелов код
    """
    try:
        tree = ast.parse(code)  # получение абстрактного дерева с удаленными комментариями
        no_docstr_tree = del_dockstrings(tree)  # удаление докстрингов
        no_docstr_text = ast.unparse(no_docstr_tree)  # очищенное дерево обратно в код
    except SyntaxError:  # синтаксическая ошибка в тексте проверяемой программы
        no_docstr_text = code
    preprocessed_text = del_spaces_and_newlines(no_docstr_text)
    return preprocessed_text


def levenstein(text_1: str, text_2: str) -> int:
    """Возвращет расстояние Левенштейна между двумя строками

    Args:
        text_1 (str): Строка 1
        text_2 (str): Строка 2

    Returns:
        int: Расстояние Левенштейна
    """
    len_1, len_2 = len(text_1), len(text_2)

    current_row = range(len_1 + 1)

    for i in range(1, len_2 + 1):
        previous_row, current_row = current_row, [i] + [0] * len_1
        for j in range(1, len_1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if text_1[j - 1] != text_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[len_1]


def compare_files(file_pair: list) -> float:
    """Сравнивает 2 файла с программами и возвращает метрику схожести в диапазоне [0, 1]

    Args:
        file_pair (list): Пара файлов для сравнения

    Raises:
        ValueError: Список должен содержать только 2 файла

    Returns:
        float: Мера схожести текстов программ
    """
    if len(file_pair) != 2:
        raise ValueError('file_pair должен содержать только 2 файла')

    code_pair = []
    for file in file_pair:
        with open(file, 'rt') as code_file:
            code = code_file.read()
        preprocessed_code = preprocess_text(code)
        code_pair.append(preprocessed_code)

    code_1, code_2 = code_pair
    distance = levenstein(code_1, code_2)
    similarity = 1 - distance / max(len(code_1), len(code_2))
    return similarity


def read_input(input_path: str) -> list:
    """Считывает фходной файл в список

    Args:
        input_path (str): Путь до входного файла

    Returns:
        list: список с парами
    """
    with open(input_path, 'rt') as input_file:
        return [line.replace('\n', '').split(' ') for line in input_file.readlines()]