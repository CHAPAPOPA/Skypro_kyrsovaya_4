import pytest
from src.interaction import search_by_keyword, display_vacancies
from src.save_vacancies import SaveVacancies
from src.hh_api import Hh_vacancies
from src.vacancy import Vacancy


@pytest.fixture
def mock_Hh_vacancies(mocker):
    mock_api = mocker.MagicMock(spec=Hh_vacancies)
    mock_api.get_vacancies.return_value = [
        Vacancy(profession='Software Engineer', requirement='Python, Java', address='Moscow, Russia',
                currency='RUR', job_finder_name='Company A', job_finder_link='https://companyA.com',
                vacancy_link='https://vacancy1.com', payment_from=50000, payment_to=80000),
        Vacancy(profession='Data Scientist', requirement='Python, SQL', address='St. Petersburg, Russia',
                currency='RUR', job_finder_name='Company B', job_finder_link='https://companyB.com',
                vacancy_link='https://vacancy2.com', payment_from=70000, payment_to=100000)
    ]
    return mock_api


@pytest.fixture
def mock_SaveVacancies(mocker):
    mock_saver = mocker.MagicMock(spec=SaveVacancies)
    return mock_saver


def test_search_by_keyword():
    vacancies = [
        Vacancy(profession='Software Engineer', requirement='Python, Java', address='Moscow, Russia',
                currency='RUR', job_finder_name='Company A', job_finder_link='https://companyA.com',
                vacancy_link='https://vacancy1.com', payment_from=50000, payment_to=80000),
        Vacancy(profession='Data Scientist', requirement='Python, SQL', address='St. Petersburg, Russia',
                currency='RUR', job_finder_name='Company B', job_finder_link='https://companyB.com',
                vacancy_link='https://vacancy2.com', payment_from=70000, payment_to=100000)
    ]
    assert len(search_by_keyword(vacancies, 'Java')) == 1
    assert len(search_by_keyword(vacancies, 'Python')) == 2
    assert len(search_by_keyword(vacancies, 'C++')) == 0


def test_display_vacancies(capsys):
    vacancies = [
        Vacancy(profession='Software Engineer', requirement='Python, Java', address='Moscow, Russia',
                currency='RUR', job_finder_name='Company A', job_finder_link='https://companyA.com',
                vacancy_link='https://vacancy1.com', payment_from=50000, payment_to=80000),
        Vacancy(profession='Data Scientist', requirement='Python, SQL', address='St. Petersburg, Russia',
                currency='RUR', job_finder_name='Company B', job_finder_link='https://companyB.com',
                vacancy_link='https://vacancy2.com', payment_from=70000, payment_to=100000)
    ]
    display_vacancies(vacancies)
    captured = capsys.readouterr()
    assert "1. Software Engineer" in captured.out
    assert "2. Data Scientist" in captured.out
