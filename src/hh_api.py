from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy
from src.save_vacancies import SaveVacancies


class Hh(ABC):
    @abstractmethod
    def get_vacancies(self, text: str):
        pass

    @staticmethod
    def get_json_vacancies(job: list):
        pass

    @staticmethod
    def save_to_json(vacancies_data: list, filename: str):
        pass


class Hh_vacancies(Hh):
    """API HeadHunter"""

    def get_vacancies(self, text: str):
        """Метод выполняет запрос к API HeadHunter для получения списка вакансий на основе переданного текста поиска"""
        vacancies_list = []
        params = {'text': text, 'page': 0, 'per_page': 100, 'salary': 60000, 'currency': "RUR"}
        try:
            while params["page"] < params.get('pages', 2):
                response = requests.get('https://api.hh.ru/vacancies', params=params)
                response.raise_for_status()
                response_data = response.json()
                params["pages"] = response_data["page"]
                params["page"] += 1
                vacancies_list.extend(self.get_json_vacancies(response_data["items"]))
        except requests.RequestException as e:
            print("Ошибка при выполнении запроса:", e)
        return vacancies_list

    @staticmethod
    def get_json_vacancies(jobs: list):
        """Функция, которая принимает список вакансий jobs и преобразует их в экземпляры класса Vacancy"""
        vacancies_list = []
        for job in jobs:
            try:
                salary = job.get("salary") or {}
                address = job.get("address") or {}
                snippet = job.get("snippet") or {}
                requirement = snippet.get("requirement", "") or "Требования не указаны"
                if requirement:
                    requirement = requirement.replace("<highlighttext>", "").replace("</highlighttext>", "")
                payment_from = salary.get("from", 0)
                payment_to = salary.get("to", 0)
                if payment_from is None:
                    payment_from = 0
                if payment_to is None:
                    payment_to = 0
                address_raw = address.get("raw", "") or "Адрес не указан"
                vacancy = Vacancy(
                    profession=job["name"],
                    requirement=requirement,
                    address=address_raw,
                    currency=salary.get("currency", ""),
                    job_finder_name=job["employer"]["name"],
                    job_finder_link=job["employer"].get("alternate_url", ""),
                    vacancy_link=job["alternate_url"],
                    payment_from=payment_from,
                    payment_to=payment_to
                )
                vacancies_list.append(vacancy)
            except Exception as e:
                print("Ошибка при обработке вакансии:", e)
        return vacancies_list

    # @staticmethod
    # def save_to_json(vacancies_data: list, filename: str, folder: str = "data"):
    #     """Сохраняет данные о вакансиях в формате JSON в указанном файле в указанной папке"""
    #     parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    #     folder_path = os.path.join(parent_dir, folder)
    #     print("Folder path:", folder_path)
    #     try:
    #         if not os.path.exists(folder_path):
    #             print("Creating folder...")
    #             os.makedirs(folder_path)
    #         filepath = os.path.join(folder_path, filename if filename.endswith('.json') else filename + '.json')
    #         with open(filepath, 'w', encoding='utf-8') as f:
    #             json.dump(vacancies_data, f, ensure_ascii=False, indent=4)
    #         print("Файл успешно создан:", filepath)
    #     except Exception as e:
    #         print("Ошибка при сохранении в файл:", e)


if __name__ == '__main__':
    vacancies = Hh_vacancies().get_vacancies('Python junior')
    save_vacancies = SaveVacancies(filename='vacancies_data')
    save_vacancies.add_vacancy(vacancies)
    # print(Hh_vacancies().get_vacancies('Python'))
    # y = Hh_vacancies()
    # yy = y.get_vacancies("Python junior")
    # print(yy)
    # y.save_to_json(yy, 'Python_jun')
