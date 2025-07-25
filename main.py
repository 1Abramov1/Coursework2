from typing import List
from src.vacancy import Vacancy
from src.save_json import JSONSaver
from src.job_api_class import HeadHunterAPI
from src.vacancy_utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, \
    print_vacancies
import os


def main() -> None:
    user_interaction()
    """Точка входа в программу. Запускает основной цикл взаимодействия с пользователем"""

def user_interaction() -> None:
    """Обрабатывает взаимодействие с пользователем и управляет workflow приложения"""
    # Получаем параметры от пользователя
    search_query: str = input("Введите поисковый запрос: ")
    top_n: int = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words: List[str] = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range: str = input("Введите диапазон зарплат (например '100000-150000'): ")

    # Получаем вакансии с hh.ru
    hh_api: HeadHunterAPI = HeadHunterAPI()
    vacancies_data: List[dict] = hh_api.get_vacancies(search_query)

    # Создаем объекты Vacancy
    vacancies: List[Vacancy] = [Vacancy.from_dict(v) for v in vacancies_data]

    # Фильтрация по ключевым словам
    filtered: List[Vacancy] = filter_vacancies(vacancies, filter_words)

    # Фильтрация по зарплате
    ranged: List[Vacancy] = get_vacancies_by_salary(filtered, salary_range)

    # Сортировка
    sorted_vacs: List[Vacancy] = sort_vacancies(ranged)

    # Выбор топ N
    top_vacancies: List[Vacancy] = get_top_vacancies(sorted_vacs, top_n)

    # Вывод в консоль
    print("\nРезультаты поиска вакансий:")
    print("=" * 50)
    print_vacancies(top_vacancies)

    # Сохранение в JSON
    file_path = os.path.join('data', 'vacancies.json')  # Путь к файлу в папке data
    os.makedirs('data', exist_ok=True)  # Создаем папку, если ее нет

    saver: JSONSaver = JSONSaver(file_path)
    data_to_save: List[dict] = [vacancy.to_dict() for vacancy in top_vacancies]  # Преобразуем в словари
    saver.save(data_to_save)
    print(f"\nДанные сохранены в файл: {os.path.abspath(file_path)}")


if __name__ == "__main__":
    main()