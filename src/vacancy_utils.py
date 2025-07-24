from typing import List

from src.vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам в названии или описании

    Args:
        vacancies: Список объектов Vacancy
        filter_words: Список ключевых слов для фильтрации

    Returns:
        Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        # Проверяем каждое ключевое слово
        for word in filter_words:
            if (
                word.lower() in vacancy.title.lower()
                or word.lower() in vacancy.description.lower()
            ):
                filtered.append(vacancy)
                break
    return filtered


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат

    Args:
        vacancies: Список объектов Vacancy
        salary_range: Строка формата "min-max" (например "100000-150000")

    Returns:
        Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies

    try:
        salary_from, salary_to = map(int, salary_range.split("-"))
    except ValueError:
        print("Неверный формат диапазона зарплат. Используйте формат 'min-max'")
        return vacancies

    filtered = []
    for vacancy in vacancies:
        if vacancy.salary is None:
            continue

        # Для вакансий с указанной зарплатой
        if vacancy.salary and "from" in vacancy.salary and "to" in vacancy.salary:
            salary_from_vacancy = vacancy.salary["from"] or 0
            salary_to_vacancy = vacancy.salary["to"] or float("inf")
            if (
                salary_from <= salary_from_vacancy <= salary_to
                or salary_from <= salary_to_vacancy <= salary_to
            ):
                filtered.append(vacancy)

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по зарплате (по убыванию)

    Args:
        vacancies: Список объектов Vacancy

    Returns:
        Отсортированный список вакансий
    """
    return sorted(
        vacancies,
        key=lambda x: (
            x.salary["from"]
            if x.salary and "from" in x.salary and x.salary["from"] is not None
            else float("-inf")
        ),
        reverse=True,
    )


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий

    Args:
        vacancies: Список объектов Vacancy
        top_n: Количество вакансий для возврата

    Returns:
        Список из top_n вакансий
    """
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Выводит информацию о вакансиях в удобочитаемом формате

    Args:
        vacancies: Список объектов Vacancy
    """
    if not vacancies:
        print("Нет вакансий для отображения")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy.title}")
        print(f"Зарплата: {vacancy.salary or 'не указана'}")
        print(f"Ссылка: {vacancy.link}")
        print(f"Описание: {vacancy.description[:200]}...")
        print("-" * 50)
