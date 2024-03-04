from hh_api import Hh_vacancies
from save_vacancies import SaveVacancies


def search_by_keyword(vacancies, keyword):
    keyword_vacancies = [v for v in vacancies if keyword.lower() in v.requirement.lower()]
    return keyword_vacancies


def display_vacancies(vacancies):
    if not vacancies:
        print("Вакансии не найдены.")
        return
    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy.profession}: {vacancy.payment_from}-{vacancy.payment_to} {vacancy.currency} - {vacancy.vacancy_link}")


def interact_with_user():
    print("Добро пожаловать в программу по поиску вакансий!")

    while True:
        profession = input("Введите профессию (для выхода из программы введите 'выход'): ")
        if not profession:
            print("Пожалуйста, введите профессию.")
            continue
        if profession.lower() == "выход":
            print("Выход из программы.")
            break

        city = input("Введите город: ")
        if city.lower() == "выход":
            print("Выход из программы.")
            break
        if not city:
            print("К сожалению, вы не ввели город, поэтому я выдам вам все профессии.")
            all_vacancies = []
        else:
            hh_api = Hh_vacancies()
            all_vacancies = hh_api.get_vacancies(f"{profession} {city}")
            if not all_vacancies:
                print(f"К сожалению, я не нашёл вакансий по запросу '{profession}' в городе '{city}'.")
                continue

        print("\nЧто вы хотите сделать?")
        print("1. Вывести топ N профессий по зарплате")
        print("2. Поиск вакансий по ключевым словам в описании")
        print("3. Вывести все профессии")

        action = input("Введите номер действия: ")
        if action == "выход":
            print("Выход из программы.")
            break

        if action == "1":
            top_n_input = input("Введите количество вакансий для вывода: ")
            if top_n_input.isdigit():
                top_n = int(top_n_input)
                top_vacancies = sorted(all_vacancies, key=lambda x: (x.payment_from + x.payment_to) / 2, reverse=True)[:top_n]
                display_vacancies(top_vacancies)
                save_choice = input("Хотите ли вы сохранить данные в JSON файл? (да/нет): ")
                if save_choice.lower() == "да":
                    filename = input("Введите имя файла для сохранения (без расширения): ")
                    save_vacancies = SaveVacancies(filename)
                    save_vacancies.add_vacancy(top_vacancies)
                    print("Данные успешно сохранены в JSON файл.")
                else:
                    print("Данные не были сохранены.")
            else:
                print("Введите только число.")
                continue
        elif action == "2":
            keyword = input("Введите ключевое слово для поиска в описании вакансии: ")
            keyword_vacancies = search_by_keyword(all_vacancies, keyword)
            if not keyword_vacancies:
                print(f"Вакансии с ключевым словом '{keyword}' в описании не найдены.")
                continue
            display_vacancies(keyword_vacancies)
            save_choice = input("Хотите ли вы сохранить данные в JSON файл? (да/нет): ")
            if save_choice.lower() == "да":
                filename = input("Введите имя файла для сохранения (без расширения): ")
                save_vacancies = SaveVacancies(filename)
                save_vacancies.add_vacancy(keyword_vacancies)
                print("Данные успешно сохранены в JSON файл.")
            else:
                print("Данные не были сохранены.")
        elif action == "3":
            display_vacancies(all_vacancies)
            save_choice = input("Хотите ли вы сохранить данные в JSON файл? (да/нет): ")
            if save_choice.lower() == "да":
                filename = input("Введите имя файла для сохранения (без расширения): ")
                save_vacancies = SaveVacancies(filename)
                save_vacancies.add_vacancy(all_vacancies)
                print("Данные успешно сохранены в JSON файл.")
            else:
                print("Данные не были сохранены.")


# if __name__ == "__main__":
#     interact_with_user()
