import pytest
from unittest.mock import patch

import requests

from src.hh_api import Hh_vacancies


@pytest.fixture
def mock_response():
    return {
        "page": 1,
        "items": [
            {
                "name": "Software Engineer",
                "salary": {"from": 50000, "to": 80000, "currency": "RUR"},
                "address": {"raw": "Moscow, Russia"},
                "snippet": {"requirement": "Python, Java"},
                "employer": {"name": "Company A", "alternate_url": "http://companya.com"}
            },
            {
                "name": "Data Scientist",
                "salary": {"from": 70000, "to": 100000, "currency": "RUR"},
                "address": {"raw": "St. Petersburg, Russia"},
                "snippet": {"requirement": "Python, SQL"},
                "employer": {"name": "Company B", "alternate_url": "http://companyb.com"}
            }
        ]
    }


@pytest.fixture
def mock_requests_get(mock_response):
    with patch('src.hh_api.requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        yield mock_get


def test_get_vacancies_error(mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException("Connection error")
    hh_api = Hh_vacancies()
    vacancies = hh_api.get_vacancies("Python Developer")
    assert vacancies == []


def test_get_vacancies_empty_list(mock_requests_get):
    mock_requests_get.return_value.json.return_value = {"page": 1, "items": []}
    hh_api = Hh_vacancies()
    vacancies = hh_api.get_vacancies("Python Developer")
    assert vacancies == []
