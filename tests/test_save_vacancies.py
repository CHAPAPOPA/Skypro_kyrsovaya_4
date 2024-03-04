import os
import json
import pytest
from src.save_vacancies import SaveVacancies


@pytest.fixture
def empty_save_vacancies(tmpdir):
    return SaveVacancies(filename="test_data", folder=tmpdir)


@pytest.fixture
def filled_save_vacancies(tmpdir):
    save_vacancies = SaveVacancies(filename="test_data", folder=tmpdir)
    vacancies = [
        {"profession": "Software Engineer", "payment_from": 50000, "payment_to": 80000, "currency": "RUR"},
        {"profession": "Data Scientist", "payment_from": 70000, "payment_to": 100000, "currency": "RUR"}
    ]
    save_vacancies.add_vacancy(vacancies)
    return save_vacancies


def test_save_data(empty_save_vacancies, tmpdir):
    data = [{"profession": "Software Engineer", "payment_from": 50000, "payment_to": 80000, "currency": "RUR"}]
    empty_save_vacancies._save_data(data)
    filepath = os.path.join(tmpdir, "test_data.json")
    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        saved_data = json.load(f)
    assert saved_data == data
