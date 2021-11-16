import argparse
import json
import os
import re
from tqdm import tqdm


def read_file(patch: str):
    try:
        if os.path.exists(patch):
            data = json.load(open(patch, encoding='windows-1251'))
            return data
    except OSError:
        print("Такого файла не существует (неверный путь к файлу)")


class Validator:
    ''' Класс Validator хранит объекты данных и проводит проверку на валидность '''
    __telephone: str
    __weight: int
    __inn: str
    __passport_number: int
    __university: str
    __age: int
    __political_views: str
    __worldview: str
    __address: str

    def __init__(
            self,
            telephone: str,
            weight: int,
            inn: str,
            passport_number: int,
            university: str,
            age: int,
            political_views: str,
            worldview: str,
            address: str):
        '''Инициализация полей данных'''
        self.__telephone = telephone
        self.__weight = weight
        self.__inn = inn
        self.__passport_number = passport_number
        self.__university = university
        self.__age = age
        self.__political_views = political_views
        self.__worldview = worldview
        self.__address = address

    def check_telephone(self) -> bool:
        '''
        Проверка номера телефона на валидность. Номер считается валидным, если
        он имеет вид: +7-(921)-049-89-86
        Возвращает:
        True - номер валидный
        False - номер невалидный
        '''
        check_number = "\\+\\d\\-\\(\\d+\\)\\-\\d+\\-\\d+\\-\\d+"
        if re.match(check_number, self.__telephone):
            return True
        else:
            return False

    def check_weight(self) -> bool:
        '''Проверка массы человека на валидность. Валидной массой является от 20кг до 250кг возвращает:
        True - масса валидный
        False - масса невалидный'''
        if (isinstance(self.__weight, int)) and (
                self.__weight > 20) and (self.__weight < 250):
            return True
        else:
            return False

    def check_inn(self) -> bool:
        '''Проверка ИННа физического лица на валидность.
         Валидным ИНН яляется 12-ти значная последовательность натуральных чисел'''
        check_inn = "\\d{12}"
        if re.match(check_inn, str(self.__inn)):
            return True
        else:
            return False

    def check_passport_number(self) -> bool:
        ''' Проверка номера паспорта на валидность.
        Валидным номером является последоватьльность из 6-ти натуральных чисел'''
        check_passport_number = "\\d{6}"
        if re.match(check_passport_number, str(self.__passport_number)):
            return True
        else:
            return False

    def check_university(self) -> bool:
        '''Проверка наименования иниверситета на валидность.
        Валидным наиминованием является полное название со всеми пробелами, абриавиатура'''
        check_university = "^[А-Я]+\\s*[а-я-.\\s]+\\s*?\\s([А-Я][А-я-.\\s]+\\s*[А-я-.\\s]+)|[А-я-]+\\s+[а-я\\s-]+\\s+[а-я]*|[А-я]{2}[а-я]*[А-Я]{2}"
        if re.match(check_university, self.__university):
            return True
        else:
            return False

    def check_age(self) -> bool:
        '''Проверка возраста на валидность.
        Валидным возрастом является диапозо от 10-ти лет до 100-та лет'''
        if (isinstance(self.__age, int)) and (
                self.__age > 10) and (self.__age < 100):
            return True
        else:
            return False

    def check_political_views(self) -> bool:
        '''Проверка политических взглядов на валидность.
        Политический взгляд является валидным, если он существует и состоит из одного слова'''
        check_polit = "[А-Я][а-я]+"
        if re.match(check_polit, self.__political_views):
            return True
        else:
            return False

    def check_world_view(self) -> bool:
        '''Проверка мировоззрения на валидность.
        Мировозрение является валидным если оно реально существует и состоит в основном из одного слова'''
        check_world = "^[А-я]+$|\\Секулярный гуманизм"
        if re.match(check_world, self.__worldview):
            return True
        else:
            return False

    def check_address(self) -> bool:
        '''Проверка адреса на валидность.
        Адрес является валидным если он записан в форме "улица пробел номер дома"
        Например: ул. Истринская 982'''
        check_address = "^[А-я]+\\.\\s[А-я-.()0-9\\s]+\\d+|^[А-я]+\\s[А-я-0-9().\\s]+\\d+|^[А-я]+\\.\\s[А-я-.\\s]+\\d+"
        if re.match(check_address, self.__address):
            return True
        else:
            return False


parser = argparse.ArgumentParser(description='SecondL.py')
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
args = parser.parse_args()
input_filename = os.path.relpath(args.inputfilename)
output_filename = os.path.relpath(args.outputfilename)
data = read_file(input_filename)
if __name__ == "__main__":
    n = int(len(data))
    count1 = count2 = count3 = count4 = count5 = int(n)
    count6 = count7 = count8 = count9 = int(n)
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
                count1 -= 1
            if temp.check_weight():
                count2 -= 1
            if temp.check_inn():
                count3 -= 1
            if temp.check_passport_number():
                count4 -= 1
            if temp.check_university():
                count5 -= 1
            if temp.check_age():
                count6 -= 1
            if temp.check_political_views():
                count7 -= 1
            if temp.check_world_view():
                count8 -= 1
            if temp.check_address():
                count9 -= 1
            progressbar.update(1)
write_data = {
    'errors in telephone': int(count1),
    'errors in weight': int(count2),
    'errors in inn': int(count3),
    'errors in passport_number': int(count4),
    'errors in university': int(count5),
    'errors in age': int(count6),
    'errors in political_views': int(count7),
    'errors in worldview': int(count8),
    'errors in address': int(count9)
}
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(write_data, f)
print(f'Количество невалидных значений телефона: {count1}')
print(f'Количество невалидных значений массы: {count2}')
print(f'Количество невалидных ИННов: {count3}')
print(f'Количество невалидных номеров паспортов: {count4}')
print(f'Количество невалидных наименований университета: {count5}')
print(f'Количество невалидных возрастов: {count6}')
print(f'Количество невалидных политических взглядов: {count7}')
print(f'Количество невалидных мировозрений: {count8}')
print(f'Количество невалидных адресов: {count9}')

# SecondL.py -i 78.txt -o test.txt
