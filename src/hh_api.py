from abc import ABC, abstractmethod
import requests
import json


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
    """Класс для работы с вакансиями"""

    def get_vacancies(self, text: str):
        vacancies_list = []
        params = {'text': text,
                  'page': 0,
                  'all_page': 100,
                  'payment': 60000,
                  'currency': "RUR",

                  }
        pages = 2
        while params["page"] < pages:
            response_again = requests.get('https://api.hh.ru/vacancies', params=params).json()

            pages = response_again["page"]
            params["page"] += 1
            for json_vacancy in self.get_json_vacancies(response_again["items"]):
                vacancies_list.append(json_vacancy)
        return vacancies_list

    @staticmethod
    def get_json_vacancies(job: list):

        job_list = []

        if not job:
            return job_list
        for i in job:
            data_vacancy = {
                "profession": i["name"],
                "requirement": i["snippet"]["requirement"]
                .replace("<highlighttext>", "").replace("</highlighttext>", "")
                if i["snippet"]["requirement"] else "",
                "address": i["address"]["raw"] if i.get("address") == "None" else "",
                "currency": i["salary"]["currency"] if i["salary"] else "",
                "job_finder_name": i["employer"]["name"],
                "job_finder_link": i["employer"]["alternate_url"] if i["employer"].get(
                    "alternate_url") else ""
                if i["employer"].get("alternate_url") else "",
                "link": i["alternate_url"],
            }
            if i["salary"]:
                data_vacancy["payment_from"] = i["salary"]["from"] if i["salary"]["from"] else 0
                data_vacancy["payment_to"] = i["salary"]["to"] if i["salary"]["to"] else 0
            else:
                data_vacancy["payment_from"] = 0
                data_vacancy["payment_to"] = 0
            job_list.append(data_vacancy)
        return job_list

    @staticmethod
    def save_to_json(vacancies_data: list, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies_data, f, ensure_ascii=False, indent=4)
