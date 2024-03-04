from src.vacancy import Vacancy


def test_vacancy_creation():
    vacancy = Vacancy("Software Engineer", "Python, Java", "Moscow, Russia", "RUR", "Company", "company.com",
                      "vacancy.com", 50000, 80000)
    assert isinstance(vacancy, Vacancy)
    assert vacancy.profession == "Software Engineer"
    assert vacancy.requirement == "Python, Java"
    assert vacancy.address == "Moscow, Russia"
    assert vacancy.currency == "RUR"
    assert vacancy.job_finder_name == "Company"
    assert vacancy.job_finder_link == "company.com"
    assert vacancy.vacancy_link == "vacancy.com"
    assert vacancy.payment_from == 50000
    assert vacancy.payment_to == 80000
    assert vacancy.average_payment == 65000


def test_vacancy_verification_missing_data():
    try:
        vacancy = Vacancy("Software Engineer", None, "Moscow, Russia", "RUR", "Company", "company.com", "vacancy.com",
                          50000, None)
    except ValueError as e:
        assert str(e) == "Не указана информация по вакансии: requirement"
