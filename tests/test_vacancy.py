import unittest
from typing import Dict, Any
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    """Тесты для класса Vacancy."""

    def setUp(self) -> None:
        """Подготовка тестовых данных."""
        self.sample_data: Dict[str, Any] = {
            "title": "Python Developer",
            "link": "https://example.com/job/1",
            "salary": {
                "from": 100000,
                "to": 150000,
                "currency": "RUR"
            },
            "description": "Требуется опытный Python-разработчик."
        }
        self.vacancy = Vacancy(
            title=self.sample_data["title"],
            link=self.sample_data["link"],
            salary=self.sample_data["salary"],
            description=self.sample_data["description"]
        )

    def test_init(self) -> None:
        """Тест инициализации вакансии."""
        self.assertEqual(self.vacancy.title, self.sample_data["title"])
        self.assertEqual(self.vacancy.link, self.sample_data["link"])
        self.assertEqual(self.vacancy.salary, self.sample_data["salary"])
        self.assertEqual(self.vacancy.description, self.sample_data["description"])

    def test_str_with_salary(self) -> None:
        """Тест строкового представления вакансии с указанной зарплатой."""
        expected_str = (
            "Python Developer\n"
            "Зарплата: 100000 - 150000 RUR\n"
            "Ссылка: https://example.com/job/1\n"
            "Описание: Требуется опытный Python-разработчик....\n"
        )
        self.assertEqual(str(self.vacancy), expected_str)

    def test_str_without_salary(self) -> None:
        """Тест строкового представления вакансии без зарплаты."""
        vacancy = Vacancy(
            title="Python Developer",
            link="https://example.com/job/1",
            salary=None,
            description="Требуется опытный Python-разработчик."
        )
        expected_str = (
            "Python Developer\n"
            "Зарплата не указана\n"
            "Ссылка: https://example.com/job/1\n"
            "Описание: Требуется опытный Python-разработчик....\n"
        )
        self.assertEqual(str(vacancy), expected_str)

    def test_to_dict(self) -> None:
        """Тест преобразования вакансии в словарь."""
        expected_dict = {
            "title": self.sample_data["title"],
            "link": self.sample_data["link"],
            "salary": self.sample_data["salary"],
            "description": self.sample_data["description"]
        }
        self.assertEqual(self.vacancy.to_dict(), expected_dict)

    def test_from_dict(self) -> None:
        """Тест создания вакансии из словаря."""
        data: Dict[str, Any] = {
            "name": "Python Developer",
            "alternate_url": "https://example.com/job/1",
            "salary": {
                "from": 100000,
                "to": 150000,
                "currency": "RUR"
            },
            "snippet": {
                "requirement": "Требуется опытный Python-разработчик."
            }
        }
        vacancy = Vacancy.from_dict(data)
        self.assertEqual(vacancy.title, data["name"])
        self.assertEqual(vacancy.link, data["alternate_url"])
        self.assertEqual(vacancy.salary, data["salary"])
        self.assertEqual(vacancy.description, data["snippet"]["requirement"])

    def test_from_dict_missing_fields(self) -> None:
        """Тест создания вакансии из словаря с отсутствующими полями."""
        data: Dict[str, Any] = {}
        vacancy = Vacancy.from_dict(data)
        self.assertEqual(vacancy.title, "Без названия")
        self.assertEqual(vacancy.link, "Ссылка не указана")
        self.assertIsNone(vacancy.salary)
        self.assertEqual(vacancy.description, "Описание не указано")


if __name__ == "__main__":
    unittest.main()