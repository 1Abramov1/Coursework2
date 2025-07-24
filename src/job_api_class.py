from abc import ABC, abstractmethod
import requests


class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий."""

    @abstractmethod
    def get_vacancies(self, search_query: str, **kwargs):
        """Получает вакансии по заданному запросу."""
        pass

class HeadHunterAPI(JobAPI):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str, **kwargs):
        """Получает вакансии с hh.ru по ключевому слову."""
        params = {
            "text": search_query,
            "search_field": "name",  # поиск по названию вакансии
            "per_page": 100,  # Кол-во вакансий (макс. 100)
            "area": 113,  # 113 - Россия
            **kwargs  # дополнительные параметры (например, salary, experience)
        }

        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            raise Exception(f"Ошибка запроса: {response.status_code}")