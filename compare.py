from argparse import ArgumentParser
from utils import read_input, compare_files


def main():
    parser = ArgumentParser(description='Антиплагиат by Alexandr Utkov')
    parser.add_argument('input_file', type=str, help='Входной файл с документами')
    parser.add_argument('output_file', type=str, help='Выходной файл с оценками')
    args = parser.parse_args()

    input_files = read_input(args.input_file)

    with open(args.output_file, 'wt') as output_file:
        for file_pair in input_files:
            try:
                result = compare_files(file_pair)
            except OSError:
                result = 'Проблема с открытием файлов'
            except UnicodeDecodeError:
                result = 'Битая кодировка одного или обоих файлов'
            except ValueError:
                result = 'В строке должно быть ровно 2 файла'

            output_file.write(f'{result}\n')


if __name__ == '__main__':
    main()
