import csv
import re
import zipfile
import os
import hashlib
import requests


def zip_unpack(directory, name_file):
    try:
        os.mkdir(directory)
    except OSError:
        print("Создать директорию %s не удалось" % directory)
    else:
        print("Успешно создана директория %s " % directory)
    test_zip = zipfile.ZipFile(name_file)
    test_zip.extractall(directory)
    test_zip.close()


def search(directory):
    txt_files = []
    tmp = ['.txt']
    check = r'\.\w+'
    target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
    for r, d, f in os.walk(directory):
        for filename in f:
            if re.findall(check, filename) == tmp:
                txt_files += [os.path.join(r, filename)]
    print(txt_files)
    for r, d, f in os.walk(directory):
        for filename in f:
            temp_file = os.path.join(r, filename)
            target_file_data = open(temp_file, 'rb').read()
            res = hashlib.md5(target_file_data).hexdigest()
            if res == target_hash:
                print('This', res)
                target_file = [os.path.join(r, filename)]
                print(target_file_data)
                print(target_file)
                return target_file_data


def work_with_site(URL):
    print(URL)
    r = requests.get(URL)
    result_dct = {}  # словарь для записи содержимого таблицы
    counter = 0
    dlt_pc = '\;{2}'
    dlt_xa = '[\D\0]'
    # Получение списка строк таблицы
    lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
    for line in lines:
        if counter == 0:
            pat = '(\<(/?[^\>]+)\>)'
            repl = ','
            # Удаление тегов
            he = re.sub(pat, repl, line)
            # Извлечение списка заголовков
            he = re.findall(r'[А-я ]+', he)
            counter += 1
            continue
        temp = re.sub(pat, ';', line)   # Удаление знаков
        temp = re.sub(dlt_pc, ';', temp)
        temp = re.sub(dlt_pc, ';', temp)
        temp = re.sub('^\;', '', temp)
        temp = re.sub('\;$', '', temp)
        temp = re.sub('\(\+\d+\D?\d+\)', '', temp)
        temp = re.sub(dlt_pc, ';', temp)
        temp = re.sub('^\W+', '', temp)
        tmp_split = temp.split(';')
        country_name = str(tmp_split[0])
        tmp_split.remove(country_name)
        country_name = re.sub('^\W+', '', country_name)
        col1_val = re.sub(dlt_xa, '', tmp_split[0])
        col2_val = re.sub(dlt_xa, '', tmp_split[1])
        col3_val = re.sub(dlt_xa, '', tmp_split[2])
        if tmp_split[3] == '_':
            tmp_split[3] = '-1'
            col4_val = tmp_split[3]
        else:
            col4_val = re.sub(dlt_xa, '', tmp_split[3])
        result_dct[country_name] = {}
        result_dct[country_name][he[0]] = int(col1_val)
        result_dct[country_name][he[1]] = int(col2_val)
        result_dct[country_name][he[2]] = int(col3_val)
        result_dct[country_name][he[3]] = int(col4_val)
    return result_dct, he


directory_to_extract_to = 'F:\\University\\Programms\\PP\\test'  # директория извлечения файлов архива
arch_file = 'F:\\University\\Programms\\PP\\tiff-4.2.0_lab1.zip'  # путь к архиву
# zip_unpack(directory_to_extract_to, arch_file)
result, headers = work_with_site(search(directory_to_extract_to))
output = open('F:\\University\\Programms\\PP\\test\\data.csv', 'w')
output.write(f'Страна;Заболело;Умерли;Вылечились;Активные случаи\n')
for key in result.keys():
    output.write(f'{key};')
    for n in range(4):
        output.write(f'{result[key][headers[n]]};')
    output.write(f'\n')
output.close()
target_country = input("Введите название страны: ").lower()
with open('F:\\University\\Programms\\PP\\test\\data.csv', 'r') as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    # Считывание данных из CSV файла
    for row in file_reader:
        # Вывод строк
        if row[0].lower() == target_country:
            for n in range(5):
                print(f'\t{row[n]}', end='')
print('\nComplete')
