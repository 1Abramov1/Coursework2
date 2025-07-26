from typing import Any, Dict, Optional


class Vacancy:
    """Класс для представления и обработки данных вакансии.

    Attributes:
        title (str): Название вакансии
        link (str): URL вакансии
        salary (Optional[Dict[str, Any]]): Информация о зарплате
        description (str): Описание вакансии
    """

    def __init__(
        self, title: str, link: str, salary: Optional[Dict[str, Any]], description: str
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
        self.salary: Dict[str, Any] = self._validate_salary(salary)
        self.description: str = description

    @staticmethod
    def _validate_salary(salary: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Валидирует данные о зарплате.

        Если зарплата не указана, возвращает словарь с нулевыми значениями.

        Args:
            salary: Словарь с данными о зарплате или None

        Returns:
            Валидный словарь с данными о зарплате
        """
        if salary is None:
            return {"from": 0, "to": 0, "currency": ""}

        # Проверяем наличие ключей 'from' и 'to'
        validated_salary = salary.copy()
        validated_salary.setdefault("from", 0)
        validated_salary.setdefault("to", 0)
        validated_salary.setdefault("currency", "")

        # Если зарплата не указана (None), устанавливаем 0
        if validated_salary["from"] is None:
            validated_salary["from"] = 0
        if validated_salary["to"] is None:
            validated_salary["to"] = 0

        return validated_salary

    def __str__(self) -> str:
        """Возвращает строковое представление вакансии в читаемом формате.

        Returns:
            Форматированная строка с основной информацией о вакансии
        """
        salary_info = "Зарплата не указана"
        if self.salary:
            from_salary = self.salary.get("from", "?")
            to_salary = self.salary.get("to", "?")
            currency = self.salary.get("currency", "")
            salary_info = f"Зарплата: {from_salary} - {to_salary} {currency}".strip()
        return (
            f"{self.title}\n"
            f"{salary_info}\n"
            f"Ссылка: {self.link}\n"
            f"Описание: {self.description[:100]}...\n"
        )

    def __repr__(self) -> str:
        """Возвращает официальное строковое представление объекта."""
        return (f"Vacancy(title='{self.title}', link='{self.link}', "
                f"salary={self.salary}, description='{self.description[:20]}...')")

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по минимальной зарплате (для оператора <)."""
        return self.get_min_salary() < other.get_min_salary()

    def __le__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по минимальной зарплате (для оператора <=)."""
        return self.get_min_salary() <= other.get_min_salary()

    def __gt__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по минимальной зарплате (для оператора >)."""
        return self.get_min_salary() > other.get_min_salary()

    def __ge__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по минимальной зарплате (для оператора >=)."""
        return self.get_min_salary() >= other.get_min_salary()

    def __eq__(self, other: object) -> bool:
        """Проверяет вакансии на равенство по всем атрибутам."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (
            self.title == other.title
            and self.link == other.link
            and self.salary == other.salary
            and self.description == other.description
        )

    def get_min_salary(self) -> int:
        """Возвращает минимальное значение зарплаты для сравнения.

        Returns:
            Минимальное значение зарплаты (0 если не указано)
        """
        if not self.salary:
            return 0
        return max(self.salary.get("from", 0), 0)

    def get_max_salary(self) -> int:
        """Возвращает максимальное значение зарплаты для сравнения.

        Returns:
            Максимальное значение зарплаты (0 если не указано)
        """
        if not self.salary:
            return 0
        return max(self.salary.get("to", 0), 0)

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
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
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
