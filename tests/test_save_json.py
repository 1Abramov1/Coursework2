import unittest
import os
import json

from src.save_json import JSONSaver


class TestJSONSaver(unittest.TestCase):
    """Тесты для класса JSONSaver."""

    def setUp(self) -> None:
        """Настройка перед каждым тестом."""
        self.filename = "test_vacancies.json"
        self.saver = JSONSaver()
        self.saver._JSONSaver__filename = self.filename  # Доступ к приватному полю для тестов
        # Очищаем файл перед каждым тестом
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self) -> None:
        """Очистка после каждого теста."""
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_vacancy_empty_file(self) -> None:
        """Тест загрузки из пустого/несуществующего файла."""
        result = self.saver.load_vacancy()
        self.assertEqual(result, [])

    def test_load_vacancy_non_empty_file(self) -> None:
        """Тест загрузки из файла с данными."""
        test_data = [{"title": "Developer"}, {"title": "Manager"}]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(test_data, file)

        result = self.saver.load_vacancy()
        self.assertEqual(result, test_data)

    def test_add_vacancy_new(self) -> None:
        """Тест добавления новой вакансии."""
        vacancy = {"title": "Developer"}
        self.saver.add_vacancy(vacancy)

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, [vacancy])

    def test_add_vacancy_duplicate(self) -> None:
        """Тест добавления существующей вакансии (дубликата)."""
        vacancy = {"title": "Developer"}
        self.saver.add_vacancy(vacancy)
        self.saver.add_vacancy(vacancy)  # Пытаемся добавить дубликат

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)  # Дубликат не должен добавиться

    def test_delete_vacancy_existing(self) -> None:
        """Тест удаления существующей вакансии."""
        vacancy = {"title": "Developer"}
        self.saver.add_vacancy(vacancy)
        self.saver.delete_vacancy(vacancy)

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, [])

    def test_delete_vacancy_non_existing(self) -> None:
        """Тест удаления несуществующей вакансии."""
        vacancy = {"title": "Developer"}
        non_existing_vacancy = {"title": "Manager"}
        self.saver.add_vacancy(vacancy)
        self.saver.delete_vacancy(non_existing_vacancy)  # Пытаемся удалить несуществующую

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, [vacancy])  # Данные не должны измениться

    def test_save(self) -> None:
        """Тест сохранения данных в файл."""
        test_data = [{"title": "Developer"}, {"title": "Manager"}]
        self.saver.save(test_data)

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, test_data)


if __name__ == "__main__":
    unittest.main()