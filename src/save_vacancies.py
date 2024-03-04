import os
import json
from abc import ABC, abstractmethod


class VacanciesStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def remove_vacancy(self, criteria):
        pass


class SaveVacancies(VacanciesStorage):
    def __init__(self, filename, folder="data"):
        self.filename = filename
        self.folder = folder
        self._create_folder_if_not_exists()

    def _create_folder_if_not_exists(self):
        folder_path = os.path.join(os.getcwd(), self.folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def add_vacancy(self, vacancies):
        vacancies_data = self._load_data()
        for vacancy in vacancies:
            vacancies_data.append(vacancy.__dict__)  # Преобразование экземпляра класса Vacancy в словарь
        self._save_data(vacancies_data)

    def get_vacancies(self, criteria):
        vacancies_data = self._load_data()
        return [v for v in vacancies_data if criteria(v)]

    def remove_vacancy(self, criteria):
        vacancies_data = self._load_data()
        filtered_vacancies = [v for v in vacancies_data if not criteria(v)]
        self._save_data(filtered_vacancies)

    def _load_data(self):
        folder_path = os.path.join(os.getcwd(), self.folder)
        filepath = os.path.join(folder_path, self.filename if self.filename.endswith('.json') else self.filename +
                                                                                                   '.json')
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, data):
        self._create_folder_if_not_exists()
        filepath = os.path.join(os.getcwd(), self.folder,
                                self.filename if self.filename.endswith('.json') else self.filename + '.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
