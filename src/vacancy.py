class Vacancy:
    """Класс для представления вакансии."""

    def __init__(self, title: str, link: str, salary: dict, description: str):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description

    def __str__(self):
        salary_info = "Зарплата не указана"
        if self.salary:
            from_salary = self.salary.get("from", "?")
            to_salary = self.salary.get("to", "?")
            salary_info = f"Зарплата: {from_salary} - {to_salary} {self.salary.get('currency', '')}"
        return f"{self.title}\n{salary_info}\nСсылка: {self.link}\nОписание: {self.description[:100]}...\n"

    def to_dict(self):
        """Преобразует вакансию в словарь для сохранения в JSON."""
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создает объект Vacancy из словаря."""
        return cls(
            title=data.get("name", "Без названия"),
            link=data.get("alternate_url", "Ссылка не указана"),
            salary=data.get("salary"),
            description=data.get("snippet", {}).get("requirement", "Описание не указано")
        )

