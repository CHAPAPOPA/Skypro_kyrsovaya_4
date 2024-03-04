class Vacancy:
    """Класс для работы с вакансиями"""
    profession: str
    requirement: str
    address: str
    currency: str
    job_finder_name: str
    job_finder_link: str
    vacancy_link: str
    payment_from: int
    payment_to: int

    def __init__(self, profession, requirement, address, currency, job_finder_name,
                 job_finder_link, vacancy_link, payment_from, payment_to):
        self.profession = profession
        self.requirement = requirement
        self.address = address
        self.currency = currency
        self.job_finder_name = job_finder_name
        self.job_finder_link = job_finder_link
        self.vacancy_link = vacancy_link
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.average_payment = self.calculate_average_payment()
        self.verification()

    def calculate_average_payment(self):
        """Метод, который при отсутствии зп, считает среднюю"""
        if self.payment_from is None:
            return "По договоренности"
        elif self.payment_to is None:
            return self.payment_from
        else:
            return (self.payment_to + self.payment_from) / 2

    def verification(self):
        for k, v in self.__dict__.items():
            if v is None:
                raise ValueError(f"Не указана информация по вакансии: {k}")

    def __repr__(self):
        return f"Vacancy(profession='{self.profession}', average_payment={self.average_payment})"

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
