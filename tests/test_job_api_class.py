import pytest
from unittest.mock import Mock, patch
from src.job_api_class import HeadHunterAPI
from typing import Dict, List, Any, Union

class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI."""

    def test_init(self) -> None:
        """Тестирование инициализации класса."""
        api: HeadHunterAPI = HeadHunterAPI()
        assert hasattr(api, 'base_url')
        assert api.base_url == "https://api.hh.ru/vacancies"

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get: Mock) -> None:
        """Тестирование успешного получения вакансий."""
        # Настраиваем mock
        mock_response: Mock = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": 1, "name": "Python Developer"}]}
        mock_get.return_value = mock_response

        # Вызываем тестируемый метод
        api: HeadHunterAPI = HeadHunterAPI()
        vacancies: List[Dict[str, Any]] = api.get_vacancies("Python")

        # Проверяем результаты
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_vacancies_with_params(self, mock_get: Mock) -> None:
        """Тестирование получения вакансий с дополнительными параметрами."""
        # Настраиваем mock
        mock_response: Mock = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        # Вызываем тестируемый метод с доп-и параметрами
        api: HeadHunterAPI = HeadHunterAPI()
        api.get_vacancies("Python", salary=100000, experience="between1And3")

        # Проверяем, что параметры переданы правильно
        mock_get.assert_called_once()
        args: tuple
        kwargs: Dict[str, Any]
        args, kwargs = mock_get.call_args
        assert kwargs['params']['salary'] == 100000
        assert kwargs['params']['experience'] == "between1And3"

    @patch('requests.get')
    def test_get_vacancies_failure(self, mock_get: Mock) -> None:
        """Тестирование обработки ошибки запроса."""
        # Настраиваем mock для возврата ошибки
        mock_response: Mock = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # Проверяем, что исключение выбрасывается
        api: HeadHunterAPI = HeadHunterAPI()
        with pytest.raises(Exception) as exc_info:
            api.get_vacancies("Python")

        assert "Ошибка запроса: 500" in str(exc_info.value)

    def test_get_vacancies_default_params(self) -> None:
        """Тестирование параметров по умолчанию."""
        api: HeadHunterAPI = HeadHunterAPI()
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"items": []}

            api.get_vacancies("Python")

            args: tuple
            kwargs: Dict[str, Any]
            args, kwargs = mock_get.call_args
            params: Dict[str, Union[str, int]] = kwargs['params']

            assert params['text'] == "Python"
            assert params['search_field'] == "name"
            assert params['per_page'] == 100
            assert params['area'] == 113
