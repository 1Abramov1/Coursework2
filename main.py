from typing import List, Dict, Any
from src.vacancy import Vacancy
from src.save_json import JSONSaver, CSVSaver, TXTSaver
from src.job_api_class import HeadHunterAPI
from src.vacancy_utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, \
    print_vacancies
import os


def main() -> None:
    """Точка входа в программу. Запускает основной цикл взаимодействия с пользователем"""
    user_interaction()


def save_vacancies_to_all_formats(vacancies: List[Vacancy], dir_path: str = 'data') -> None:
    """Сохраняет вакансии в файлы разных форматов (JSON, CSV, TXT)

    Args:
        vacancies: Список объектов Vacancy для сохранения
        dir_path: Путь к директории для сохранения (по умолчанию 'data')
    """
    os.makedirs(dir_path, exist_ok=True)

    # Преобразуем вакансии в словари
    vacancies_data = [vacancy.to_dict() for vacancy in vacancies]

    # Сохраняем в JSON
    json_path = os.path.join(dir_path, 'vacancies.json')
    json_saver = JSONSaver(json_path)
    json_saver.save_vacancies(vacancies_data)  # Исправлено с save на save_vacancies
    print(f"Данные сохранены в JSON: {os.path.abspath(json_path)}")

    # Сохраняем в CSV
    csv_path = os.path.join(dir_path, 'vacancies.csv')
    csv_saver = CSVSaver(csv_path)
    csv_saver.save_vacancies(vacancies_data)
    print(f"Данные сохранены в CSV: {os.path.abspath(csv_path)}")

    # Сохраняем в TXT
    txt_path = os.path.join(dir_path, 'vacancies.txt')
    txt_saver = TXTSaver(txt_path)
    txt_saver.save_vacancies(vacancies_data)
    print(f"Данные сохранены в TXT: {os.path.abspath(txt_path)}")


def user_interaction() -> None:
    """Обрабатывает взаимодействие с пользователем и управляет workflow приложения"""
    # Получаем параметры от пользователя
    search_query: str = input("Введите поисковый запрос: ")
    top_n: int = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words: List[str] = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range: str = input("Введите диапазон зарплат (например '100000-150000'): ")

    # Получаем вакансии с hh.ru
    hh_api: HeadHunterAPI = HeadHunterAPI()
    vacancies_data: List[Dict[str, Any]] = hh_api.get_vacancies(search_query)

    # Создаем объекты Vacancy
    vacancies: List[Vacancy] = [Vacancy.from_dict(v) for v in vacancies_data]

    # Фильтрация по ключевым словам
    filtered: List[Vacancy] = filter_vacancies(vacancies, filter_words)

    # Фильтрация по зарплате
    ranged: List[Vacancy] = get_vacancies_by_salary(filtered, salary_range)

    # Сортировка
    sorted_vacs: List[Vacancy] = sort_vacancies(ranged)

    # Выбор топ N
    top_vacancies: List[Vacancy] = get_top_vacancies(sorted_vacs, top_n)  # Исправлено с top_vacancies на top_vacancies

    # Вывод в консоль
    print("\nРезультаты поиска вакансий:")
    print("=" * 50)
    print_vacancies(top_vacancies)

    # Сохранение в разные форматы
    save_vacancies_to_all_formats(top_vacancies)


if __name__ == "__main__":
    main()