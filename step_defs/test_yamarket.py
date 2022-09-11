"""Тесты для feature/yamarket.future."""

import random
import time

from pytest_bdd import given, parsers, scenario, then, when
from selenium.common.exceptions import NoSuchElementException

from .utils import (ELEMENTS, get_product_elements, get_product_skuId,
                    highlight, move_to, scroll_down)


@scenario('../feature/yamarket.feature', 'Поиск смартфона на ЯндексМаркете')
def test_start():
    pass


@given('пользователь заходит на yandex.ru', target_fixture='start_time')
def get_page_yandex(driver, log):
    log.info('Тест запущен')

    driver.get('http://www.yandex.ru')
    log.info('Пользователь заходит на yandex.ru')
    return time.time()


@given('пользователь нажимает на кнопку «Маркет»')
def press_button_market(driver, log):
    button = driver.find_element(*ELEMENTS['market_main_button'])
    highlight(button, 1, 'blue', 5)
    button.click()
    driver.switch_to.window(driver.window_handles[1])

    log.info('Пользователь нажимает на кнопку «Маркет»')


@given('пользователь вводит «Смартфоны» в поле поиска')
def input_search(driver, log):
    input = driver.find_element(*ELEMENTS['market_search_input'])
    highlight(input, 1, 'blue', 5)
    input.send_keys("смартфоны")

    log.info('Пользователь вводит «Смартфоны» в поле поиска')


@given('пользователь нажимает кнопку «Найти»')
def press_search_button(driver, log):
    button = driver.find_element(*ELEMENTS['market_search_button'])
    highlight(button, 1, 'blue', 5)
    button.click()

    log.info('пользователь нажимает кнопку «Найти»')


@given('пользователь нажимает на кнопку «Все фильтры»')
def press_all_filters_button(driver, log):
    try:
        button = driver.find_element(*ELEMENTS['market_all_filters_button'])
        move_to(button)
        highlight(button, 1, 'blue', 5)
        button.click()
    except NoSuchElementException:
        assert False, log.error('Не найдена кнопка «Все фильтры»\n')

    log.info('Пользователь нажимает на кнопку «Все фильтры»')


@given(
    parsers.parse(
        'пользователь вводит "{max_price}" в разделе «Цена, ₽» в инпуте «до»'
    )
)
@given('пользователь вводит "<max_price>" в разделе «Цена, ₽» в инпуте «до»')
def input_max_price(driver, max_price, log):
    input = driver.find_element(*ELEMENTS['filters_max_price_input'])
    input.send_keys(max_price)
    highlight(input, 1, 'blue', 5)

    log.info(
        f'Пользователь вводит "{max_price}" в разделе «Цена, ₽» в инпуте «до»'
    )


@given(
    parsers.parse(
        'пользователь вводит "{min_diagonal}" '
        'в разделе «Диагональ экрана (точно)» в инпуте «от»'
    )
)
@given(
    'пользователь вводит "<min_diagonal>" в разделе '
    '«Диагональ экрана (точно)» в инпуте «от»')
def input_min_diagonal(driver, min_diagonal, log):
    bar = driver.find_element(*ELEMENTS['filters_diagonal_exact_bar'])
    move_to(bar, 300)
    bar.click()

    input = driver.find_element(*ELEMENTS['filters_min_diagonal_exact_input'])
    input.send_keys(min_diagonal)
    highlight(input, 1, 'blue', 5)

    log.info(
        f'Пользователь вводит "{min_diagonal}" '
        'в разделе «Диагональ экрана (точно)» в инпуте «от»'
    )


@given(
    parsers.parse(
        'пользователь выбирает "{producers_number}" '
        'случайных производителей в разделе «Производитель»'
    )
)
@given(
    'пользователь выбирает "<producers_number>" '
    'случайных производителей в разделе «Производитель»'
)
def select_producers_labels(driver, producers_number, log):
    labels = driver.find_elements(*ELEMENTS['filters_producers_labels'])
    for element in random.sample(labels, int(producers_number)):
        element.click()

    log.info(
        f'Пользователь выбирает "{producers_number}" '
        'случайных производителей в разделе «Производитель»'
    )


@given('пользователь нажимает на кнопку «Показать предложения»')
def press_apply_filters_button(driver, log):
    button = driver.find_element(*ELEMENTS['filters_apply_button'])
    highlight(button, 2, 'blue', 5)
    button.click()

    log.info('Пользователь нажимает на кнопку «Показать предложения»')


@given(
    'пользователь считает число смартфонов '
    'на странице, запоминает последний смартфон',
    target_fixture='skuId'
)
def remember_product(driver, log):
    time.sleep(2)
    scroll_down(driver)
    time.sleep(1)

    articles = driver.find_elements(
        *ELEMENTS['market_products_articles']
    )
    move_to(articles[-1])
    highlight(articles[-1], 5, 'blue', 5)

    log.info(f'Количество смартфонов на странице: {len(articles)}')
    return get_product_skuId(articles[-1])


@when(
    parsers.parse(
        'пользователь нажимает на кнопку "{sort_type}" в панели сортировки'
    )
)
@when('пользователь нажимает на кнопку "<sort_type>" в панели сортировки')
def press_sort_button(driver, sort_type, log):
    button = driver.find_element(*ELEMENTS['market_sort_buttons'][sort_type])
    move_to(button, 0)
    highlight(button, 1, 'blue', 5)
    button.click()

    log.info(
        f'Пользователь нажимает на кнопку "{sort_type}" в панели сортировки'
    )


@then('пользователь находит смартфон в выдаче и нажимает на его название')
def find_product(driver, skuId, log):
    while True:
        time.sleep(2)
        scroll_down(driver)
        time.sleep(1)
        article, span = get_product_elements(driver, skuId)
        if article:
            break

        try:
            button = driver.find_element(
                *ELEMENTS['market_next_page_button']
            )
            move_to(button, 300)
            highlight(button, 1, 'blue', 5)
            button.click()
        except NoSuchElementException:
            assert False, log.error(
                'Смартфон исчез из выдачи после сортировки\n'
            )

    move_to(article, 0)
    highlight(article, 3, 'blue', 5)
    span.click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[2])

    log.info('Смартфон найден в выдаче')


@then('на странице смартфона указан его рейтинг')
def get_raiting(driver, log, start_time):
    try:
        raiting = driver.find_element(
            *ELEMENTS['product_page_raiting_badge']
        )
        highlight(raiting, 3, 'blue', 5)
        log.info(f'Рейтинг смартфона: {raiting.text}')
    except NoSuchElementException:
        log.warning('На странице отсутствует рейтинг смартфона')

    test_time = round(time.time() - start_time, 2)
    log.info(f'Тест прошел успешно за {test_time} секунд\n')
