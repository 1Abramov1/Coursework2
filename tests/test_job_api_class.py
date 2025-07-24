import pytest
from unittest.mock import Mock, patch
from src.job_api_class import HeadHunterAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI."""

    def test_init(self):
        """Тестирование инициализации класса."""
        api = HeadHunterAPI()
        assert hasattr(api, 'base_url')
        assert api.base_url == "https://api.hh.ru/vacancies"

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Тестирование успешного получения вакансий."""
        # Настраиваем mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": 1, "name": "Python Developer"}]}
        mock_get.return_value = mock_response

        # Вызываем тестируемый метод
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        # Проверяем результаты
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_vacancies_with_params(self, mock_get):
        """Тестирование получения вакансий с дополнительными параметрами."""
        # Настраиваем mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        # Вызываем тестируемый метод с доп-и параметрами
        api = HeadHunterAPI()
        api.get_vacancies("Python", salary=100000, experience="between1And3")

        # Проверяем, что параметры переданы правильно
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs['params']['salary'] == 100000
        assert kwargs['params']['experience'] == "between1And3"

    @patch('requests.get')
    def test_get_vacancies_failure(self, mock_get):
        """Тестирование обработки ошибки запроса."""
        # Настраиваем mock для возврата ошибки
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # Проверяем, что исключение выбрасывается
        api = HeadHunterAPI()
        with pytest.raises(Exception) as exc_info:
            api.get_vacancies("Python")

        assert "Ошибка запроса: 500" in str(exc_info.value)

    def test_get_vacancies_default_params(self):
        """Тестирование параметров по умолчанию."""
        api = HeadHunterAPI()
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"items": []}

            api.get_vacancies("Python")

            args, kwargs = mock_get.call_args
            params = kwargs['params']

            assert params['text'] == "Python"
            assert params['search_field'] == "name"
            assert params['per_page'] == 100
            assert params['area'] == 113
