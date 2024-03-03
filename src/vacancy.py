class Vacancy:
    """Класс для работы с вакансиями"""
    profession: str
    requirement: str
    link: str
    currency: str
    job_finder_name: str
    job_finder_link: str
    vacancy_link: str
    payment_from: int
    payment_to: int

    def __init__(self, profession, requirement, link, currency, job_finder_name,
                 job_finder_link, vacancy_link, payment_from, payment_to):

        self.profession = profession
        self.requirement = requirement
        self.link = link
        self.currency = currency
        self.job_finder_name = job_finder_name
        self.job_finder_link = job_finder_link
        self.vacancy_link = vacancy_link
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.average_payment = 0
        self.verification()
        self.change_average_payment()

    def change_average_payment(self):
        """Метод, который при отсутствии зп, считает среднюю"""
        if self.payment_from == 0:
            self.average_payment = "По договоренности"
        elif self.payment_to == 0:
            self.average_payment = self.payment_from
        else:
            self.average_payment = (int(self.payment_to) + int(self.payment_from)) / 2

    def verification(self):
        for k, v in self.__dict__.items():
            if v is None:
                raise ValueError(f"Не указана информация по вакансии: {k}")

            return True

    def __gt__(self, other):
        return self.average_payment > other.average_payment

    def __ge__(self, other):
        return self.average_payment >= other.average_payment

    def __lt__(self, other):
        return self.average_payment < other.average_payment

    def __le__(self, other):
        return self.average_payment <= other.average_payment

    def __eq__(self, other):
        return self.average_payment == other.average_payment
