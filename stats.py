"""Подсчет статистики по логам тестов."""


def count_stats(path_to_log):
    """Подсчитать статистику по логу."""
    results = {
        'tests_number': 0,
        'tests_passed': 0,
        'all_tests_time': 0,
        'all_filters_button_not_found': 0,
        'no_raiting': 0,
        'no_product_in_results': 0,
        'other_fails': 0,
        'passed_percent': 0,
        'test_average_time': 0
    }

    with open(path_to_log, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if 'Тест запущен' in line:
            results['tests_number'] += 1
        elif 'Тест прошел успешно' in line:
            results['tests_passed'] += 1
            results['all_tests_time'] += float(line[30:-8])
        elif 'Не найдена кнопка «Все фильтры»' in line:
            results['all_filters_button_not_found'] += 1
        elif 'На странице отсутствует рейтинг смартфона' in line:
            results['no_raiting'] += 1
        elif 'Смартфон исчез из выдачи после сортировки' in line:
            results['no_product_in_results'] += 1

    results['other_fails'] = (
        results['tests_number'] - results['tests_passed']
        - results['all_filters_button_not_found']
        - results['no_product_in_results']
    )
    results['passed_percent'] = round(
        results['tests_passed'] / results['tests_number'] * 100, 2
    )
    results['test_average_time'] = round(
        results['all_tests_time'] / results['tests_number'], 2
    )
    return results


def print_stats(results):
    """Вывести статистику."""
    print(
        'Тестов проведено: '
        f'{results["tests_number"]} \n'
        'Успешных тестов: '
        f'{results["tests_passed"]}, {results["passed_percent"]}%\n'
        'Среднее время теста: '
        f'{results["test_average_time"]} секунд\n'
        'Не найдена кнопка «Все фильтры»: '
        f'{results["all_filters_button_not_found"]}\n'
        'На странице отсутствует рейтинг смартфона: '
        f'{results["no_raiting"]}\n'
        'Cмартфон исчез из выдачи после сортировки: '
        f'{results["no_product_in_results"]}\n'
        'Незарегистрированные ошибки: '
        f'{results["other_fails"]}'
    )


if __name__ == '__main__':
    print_stats(count_stats('main.log'))
