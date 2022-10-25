from pprint import pprint
from managers import HostelManager
from datetime import datetime

def print_data(data):
    print()
    print('Данные:')
    pprint(data)


if __name__ == '__main__':
    manager = HostelManager()

    while True:
        print('Выберите действие:')
        print('1. Вывести отчет по предоставленным услугам')
        print('2. Получить статистику заболеваний за определенный период')
        print('3. Получить количество зарегистрированных случаев каждого заболевания')
        print('4. Получить статику по количеству направлений, выписанных каждым врачом'
              ' (для врачей, выписавших больше 1 направления)')
        print('0. Выход')

        flag = int(input('Ваш выбор: '))
        print()
        match flag:
            case 0:
                break

            case 1:
                print_data(manager.get_service_report())

            case 2:
                format_str = '%d.%m.%Y'
                print_data(manager.get_hiled_diagnosis_for_period(
                    datetime.strptime(input('Начало периода: '), format_str),
                    datetime.strptime(input('Окончание периода: '), format_str)
                ))

            case 3:
                print_data(manager.get_count_all_cases_of_diagnosis())

            case 4:
                print_data(manager.get_statistics_of_doctors_refferals())

            case _:
                print('Неправильный ввод.')

        print()
