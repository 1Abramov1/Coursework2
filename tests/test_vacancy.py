import unittest
from typing import Optional, Union
from src.vacancy import Vacancy


class TestVacancyMethods(unittest.TestCase):
    """Тесты для методов класса Vacancy."""

    def setUp(self) -> None:
        """Подготовка тестовых данных."""
        self.sample_data = {
            "name": "Python Developer",
            "alternate_url": "http://example.com",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"requirement": "Опыт работы с Python"},
        }
        self.vacancy = Vacancy.from_dict(self.sample_data)

    def test_get_min_salary(self) -> None:
        """Тест метода get_min_salary()."""
        # Тест с указанной зарплатой
        self.assertEqual(self.vacancy.get_min_salary(), 100000)

        # Тест с отсутствующей зарплатой
        vacancy_no_salary = Vacancy.from_dict({**self.sample_data, "salary": None})
        self.assertEqual(vacancy_no_salary.get_min_salary(), 0)

        # Тест с отсутствующим 'from' в зарплате
        vacancy_no_from = Vacancy.from_dict(
            {**self.sample_data, "salary": {"to": 120000}}
        )
        self.assertEqual(vacancy_no_from.get_min_salary(), 0)

        # Тест с отрицательной зарплатой
        vacancy_negative = Vacancy.from_dict(
            {**self.sample_data, "salary": {"from": -50000, "to": 100000}}
        )
        self.assertEqual(vacancy_negative.get_min_salary(), 0)

    def test_get_max_salary(self) -> None:
        """Тест метода get_max_salary()."""
        # Тест с указанной зарплатой
        self.assertEqual(self.vacancy.get_max_salary(), 150000)

        # Тест с отсутствующей зарплатой
        vacancy_no_salary = Vacancy.from_dict({**self.sample_data, "salary": None})
        self.assertEqual(vacancy_no_salary.get_max_salary(), 0)

        # Тест с отсутствующим 'to' в зарплате
        vacancy_no_to = Vacancy.from_dict(
            {**self.sample_data, "salary": {"from": 100000}}
        )
        self.assertEqual(vacancy_no_to.get_max_salary(), 0)

        # Тест с отрицательной зарплатой
        vacancy_negative = Vacancy.from_dict(
            {**self.sample_data, "salary": {"from": 50000, "to": -100000}}
        )
        self.assertEqual(vacancy_negative.get_max_salary(), 0)

    def test_to_dict(self) -> None:
        """Тест метода to_dict()."""
        expected_dict = {
            "title": "Python Developer",
            "link": "http://example.com",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "description": "Опыт работы с Python",
        }
        self.assertDictEqual(self.vacancy.to_dict(), expected_dict)

        # Тест с отсутствующей зарплатой
        vacancy_no_salary = Vacancy.from_dict({**self.sample_data, "salary": None})
        expected_no_salary = {
            "title": "Python Developer",
            "link": "http://example.com",
            "salary": {"from": 0, "to": 0, "currency": ""},
            "description": "Опыт работы с Python",
        }
        self.assertDictEqual(vacancy_no_salary.to_dict(), expected_no_salary)

    def test_from_dict(self) -> None:
        """Тест метода from_dict()."""
        # Проверка основных полей
        self.assertEqual(self.vacancy.title, "Python Developer")
        self.assertEqual(self.vacancy.link, "http://example.com")
        self.assertEqual(self.vacancy.description, "Опыт работы с Python")
        self.assertDictEqual(
            self.vacancy.salary, {"from": 100000, "to": 150000, "currency": "RUR"}
        )

        # Тест с неполными данными
        incomplete_data: dict[str, Optional[Union[str, dict]]] = {
            "name": "Incomplete Job",
            "alternate_url": None,
            "salary": None,
            "snippet": {},
        }

        vacancy_incomplete = Vacancy.from_dict(incomplete_data)
        self.assertEqual(vacancy_incomplete.title, "Incomplete Job")
        self.assertEqual(vacancy_incomplete.link, None)  # Изменено ожидаемое значение
        self.assertEqual(vacancy_incomplete.description, "Описание не указано")
        self.assertDictEqual(
            vacancy_incomplete.salary, {"from": 0, "to": 0, "currency": ""}
        )


if __name__ == "__main__":
    unittest.main()
