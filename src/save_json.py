import csv
import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, cast


class FileSaver(ABC):
    """Абстрактный базовый класс для работы с файлами вакансий."""

    def __init__(self, filename: str) -> None:
        self._filename = filename

    @abstractmethod
    def load_vacancies(self) -> List[Dict[str, Any]]:
        """Загрузка вакансий из файла."""
        pass

    @abstractmethod
    def save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """Сохранение вакансий в файл."""
        pass

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавление вакансии в файл без дублирования."""
        data = self.load_vacancies()
        if vacancy not in data:
            data.append(vacancy)
            self.save_vacancies(data)

    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Удаление вакансии из файла."""
        data = self.load_vacancies()
        if vacancy in data:
            data.remove(vacancy)
            self.save_vacancies(data)


class JSONSaver(FileSaver):
    """Класс для работы с JSON-файлами вакансий."""

    def __init__(self, filename: str = "vacancies.json") -> None:
        super().__init__(filename)

    def load_vacancies(self) -> List[Dict[str, Any]]:
        """Загрузка вакансий из JSON-файла."""
        if not os.path.exists(self._filename):
            return []
        with open(self._filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return cast(List[Dict[str, Any]], data)

    def save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """Сохранение вакансий в JSON-файл."""
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class CSVSaver(FileSaver):
    """Класс для работы с CSV-файлами вакансий."""

    def __init__(self, filename: str = "vacancies.csv") -> None:
        super().__init__(filename)

    def load_vacancies(self) -> List[Dict[str, Any]]:
        """Загрузка вакансий из CSV-файла."""
        if not os.path.exists(self._filename):
            return []

        with open(self._filename, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """Сохранение вакансий в CSV-файл."""
        if not data:
            return

        fieldnames = data[0].keys()
        with open(self._filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


class TXTSaver(FileSaver):
    """Класс для работы с текстовыми файлами вакансий."""

    def __init__(self, filename: str = "vacancies.txt") -> None:
        super().__init__(filename)

    def load_vacancies(self) -> List[Dict[str, Any]]:
        """Загрузка вакансий из текстового файла."""
        if not os.path.exists(self._filename):
            return []

        with open(self._filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            return [json.loads(line.strip()) for line in lines if line.strip()]

    def save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """Сохранение вакансий в текстовый файл."""
        with open(self._filename, "w", encoding="utf-8") as file:
            for vacancy in data:
                file.write(json.dumps(vacancy, ensure_ascii=False) + "\n")
