import argparse
import json
import os
from Validator3000 import Validator
from tqdm import tqdm


def read_file(patch: str):
    try:
        if os.path.exists(patch):
            data = json.load(open(patch, encoding='windows-1251'))
            return data
    except OSError:
        print("Такого файла не существует (неверный путь к файлу)")


def heapify(arr, n, i, by):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i][by] < arr[l][by]:
        largest = l

    if r < n and arr[largest][by] < arr[r][by]:
        largest = r

    if largest != i:
        arr[i][by], arr[largest][by] = arr[largest][by], arr[i][by]
        heapify(arr, n, largest, by)
        

def sort(sorted_list: list, by_sort: str, name_file: str) -> None:
    '''Реализация пирамидальной сортировки'''
    n = int(len(sorted_list))
    print(f'\nСортировка данных\n')
    with tqdm(total=100, desc='Progress: ') as progressbar:
        for i in range(n, -1, -1):
            heapify(sorted_list, n, i, by_sort)
        progressbar.update(50)
        for i in range(n - 1, 0, -1):
            sorted_list[i][by_sort], sorted_list[0][by_sort] = sorted_list[0][by_sort], sorted_list[i][by_sort]  # свап
            heapify(sorted_list, i, 0, by_sort)
        progressbar.update(50)

    name_file = open(name_file, "w", encoding='windows-1251')
    print(f'\nЗапись отсортированных данных в файл\n')
    with tqdm(total=n, desc='Progress: ') as progressbar:
        data111 = json.dumps(sorted_list, ensure_ascii=False, indent=4)
        name_file.write(data111)
        name_file.close()
        progressbar.update(int(n))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='thirdl.py')
    input_filename = ""
    output_filename = ""
    parser.add_argument(
        '-i',
        type=str,
        help='Путь к файлу или его название, из которого должны '
             'считываться данные',
        required=True,
        dest='inputfilename')
    parser.add_argument(
        '-o',
        type=str,
        help='Путь к файлу или его название, в который нужно сохранить данные',
        required=True,
        dest='outputfilename')
    parser.add_argument('-so', type=str, help='Название файла для отсортированных даннных', default=None,
                        dest='file_for_sorted_data')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-wght', help='Сортировка данных по весу', default=None, dest='sort_by_weight')
    group.add_argument('-passnum', help='Сортировка данных по номеру паспорта', default=None, dest='sort_by_passnum')
    group.add_argument('-age', help='Сортировка данных по возрасту', default=None, dest='sort_by_age')
    args = parser.parse_args()
    input_filename = os.path.relpath(args.inputfilename) + ".txt"
    output_filename = os.path.relpath(args.outputfilename) + ".txt"
    data = read_file(input_filename)
    data_for_sort = list()
    n = int(len(data))
    count1 = count2 = count3 = count4 = count5 = int(0)
    count6 = count7 = count8 = count9 = count10 = int(0)
    with tqdm(total=n, desc='Progress: ') as progressbar:
        for dat in data:
            temp = Validator(
                dat['telephone'],
                dat['weight'],
                dat['inn'],
                dat['passport_number'],
                dat['university'],
                dat['age'],
                dat['political_views'],
                dat['worldview'],
                dat['address'])
            if temp.check_telephone():
                count1 += 1
            if temp.check_weight():
                count2 += 1
            if temp.check_inn():
                count3 += 1
            if temp.check_passport_number():
                count4 += 1
                if type(dat["passport_number"]) == str:
                    print(dat["passport_number"])
            if temp.check_university():
                count5 += 1
            if temp.check_age():
                count6 += 1
            if temp.check_political_views():
                count7 += 1
            if temp.check_world_view():
                count8 += 1
            if temp.check_address():
                count9 += 1
            if temp.check_all():
                count10 += 1
                data_for_sort.append(dat)
            progressbar.update(1)
    write_data = {
        'valid of records in telephone': int(count1),
        'valid of records in weight': int(count2),
        'valid of records in inn': int(count3),
        'valid of records in passport_number': int(count4),
        'valid of records in university': int(count5),
        'valid of records in age': int(count6),
        'valid of records in political_views': int(count7),
        'valid of records in worldview': int(count8),
        'valid of records in address': int(count9),
        'valid number of records': int(count10)
    }
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(write_data, f)
    print(f'Количество валидных значений телефона: {count1}')
    print(f'Количество валидных значений массы: {count2}')
    print(f'Количество валидных ИННов: {count3}')
    print(f'Количество валидных номеров паспортов: {count4}')
    print(f'Количество валидных наименований университета: {count5}')
    print(f'Количество валидных возрастов: {count6}')
    print(f'Количество валидных политических взглядов: {count7}')
    print(f'Количество валидных мировозрений: {count8}')
    print(f'Количество валидных адресов: {count9}')
    print(f'Общее количество валидных записей: {count10}')

    file_by_sort = os.path.relpath(args.file_for_sorted_data) + ".txt"
    if args.sort_by_weight is not None:
        sort(data_for_sort, 'weight', file_by_sort)
        print(f'\n\tДанные успешно отсортированы и сохранены в файл "{file_by_sort}"!\t')
    if args.sort_by_passnum is not None:
        sort(data_for_sort, 'passport_number', file_by_sort)
        print(f'\n\tДанные успешно отсортированы и сохранены в файл "{file_by_sort}"!\t')
    if args.sort_by_age is not None:
        sort(data_for_sort, 'age', file_by_sort)
        print(f'\n\tДанные успешно отсортированы и сохранены в файл "{file_by_sort}"!\t')

# Проверка отсортированных данных на читаемость
# data1 = read_file(file_by_sort)
# for d1 in data1:
#    temp = Validator(
#                d1['telephone'],
#                d1['weight'],
#                d1['inn'],
#                d1['passport_number'],
#                d1['university'],
#                d1['age'],
#                d1['political_views'],
#                d1['worldview'],
#                d1['address'])
#    print(f'{d1["telephone"]}, {d1["weight"]}, {d1["inn"]}, {d1["passport_number"]}, {d1["university"]}, {d1["age"]},\
#    {d1["political_views"]}, {d1["worldview"]}, {d1["address"]}')
