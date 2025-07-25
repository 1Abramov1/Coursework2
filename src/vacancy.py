from typing import Dict, Optional, Any


class Vacancy:
    """Класс для представления и обработки данных вакансии.

    Attributes:
        title (str): Название вакансии
        link (str): URL вакансии
        salary (Optional[Dict[str, Any]]): Информация о зарплате
        description (str): Описание вакансии
    """

    def __init__(
            self,
            title: str,
            link: str,
            salary: Optional[Dict[str, Any]],
            description: str
    ) -> None:
        """Инициализирует объект вакансии.

        Args:
            title: Название вакансии
            link: Ссылка на вакансию
            salary: Словарь с данными о зарплате (может быть None)
            description: Текст описания вакансии
        """
        self.title: str = title
        self.link: str = link
        self.salary: Optional[Dict[str, Any]] = salary
        self.description: str = description

    def __str__(self) -> str:
        """Возвращает строковое представление вакансии в читаемом формате.

        Returns:
            Форматированная строка с основной информацией о вакансии
        """
        salary_info = "Зарплата не указана"
        if self.salary:
            from_salary = self.salary.get("from", "?")
            to_salary = self.salary.get("to", "?")
            currency = self.salary.get('currency', '')
            salary_info = f"Зарплата: {from_salary} - {to_salary} {currency}".strip()
        return (
            f"{self.title}\n"
            f"{salary_info}\n"
            f"Ссылка: {self.link}\n"
            f"Описание: {self.description[:100]}...\n"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует вакансию в словарь для сериализации в JSON.

        Returns:
            Словарь с основными полями вакансии, готовый для сохранения
        """
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Vacancy':
        """Создает объект Vacancy из словаря с данными API.

        Args:
            data: Словарь с данными вакансии из API

        Returns:
            Новый экземпляр класса Vacancy

        Note:
            Обрабатывает данные специфичные для API HeadHunter
        """
        return cls(
            title=data.get("name", "Без названия"),
            link=data.get("alternate_url", "Ссылка не указана"),
            salary=data.get("salary"),
            description=data.get("snippet", {}).get(
                "requirement", "Описание не указано"
            ),
        )
