"""Локаторы элементов и вспомогательные функции."""

import json
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

ELEMENTS = {
    'market_main_button': (By.XPATH, '//a[@data-id="market"]'),
    'market_search_input': (By.ID, 'header-search'),
    'market_search_button': (By.XPATH, '//button[@data-r="search-button"]'),
    'market_all_filters_button': (
        By.XPATH,
        '//a[@data-auto="allFiltersButton"]'
    ),
    'market_products_articles': (
        By.XPATH,
        '//article'
    ),
    'market_sort_buttons': {
        'по популярности': (
            By.XPATH,
            '//button[contains(text(), "по популярности")]'
        ),
        'по цене': (
            By.XPATH,
            '//button[contains(text(), "по цене")]'
        ),
        'по рейтингу': (
            By.XPATH,
            '//button[contains(text(), "по рейтингу")]'
        ),
        'по скидке': (
            By.XPATH,
            '//button[contains(text(), "по скидке")]'
        )
    },
    'market_next_page_button': (
        By.XPATH,
        '//span[contains(text(), "Вперёд")]'
    ),
    'market_all_results_button': (
        By.XPATH,
        '//a[contains(text(), "Все результаты поиска")]'
    ),
    'filters_max_price_input': (
        By.XPATH,
        '(//div[@data-filter-id="glprice"]//input)[2]'
    ),
    'filters_diagonal_exact_bar': (
        By.XPATH,
        '//div[@data-filter-id="14805766"]'
    ),
    'filters_min_diagonal_exact_input': (
        By.XPATH,
        '//div[@data-filter-id="14805766"]//input[1]'
    ),
    'filters_producers_labels': (
        By.XPATH,
        '//div[@data-filter-id="7893318"]//label'
    ),
    'filters_apply_button': (
        By.XPATH,
        '//a[@class="_2qvOO _3qN-v _1Rc6L"]'
    ),
    'product_page_raiting_badge': (
        By.XPATH,
        '(//span[@data-auto="rating-badge-value"])[2]'
    )
}


def get_product_sku(article):
    """Получить skuId продукта."""
    return json.loads(
        article.get_attribute('data-zone-data')
    )['skuId']


def scroll_down(driver):
    """Переместиться в конец страницы."""
    driver.execute_script(
        'window.scrollTo({'
        '    top: document.body.scrollHeight, behavior: "smooth"'
        '});'
    )


def move_to(element, scroll=500):
    """Переместиться к элементу."""
    ActionChains(element._parent).move_to_element(element).perform()
    element._parent.execute_script(f'window.scrollBy(0, {scroll})')


def highlight(element, effect_time, color, border):
    """Подсветить элемент."""
    driver = element._parent

    def apply_style(s):
        driver.execute_script(
            'arguments[0].setAttribute("style", arguments[1]);',
            element, s
        )

    original_style = element.get_attribute('style')
    apply_style(f'border: {border}px solid {color};')
    time.sleep(effect_time)
    apply_style(original_style)


def get_product_elements(driver, sku):
    """Найти article и span товара по skuId в поисковой выдаче."""
    try:
        product_article = driver.find_element(
            By.XPATH,
            f'//article[contains(@data-zone-data,"{sku}")]'
        )
        product_span = product_article.find_element(
            By.XPATH,
            './/span'
        )
        return (product_article, product_span)
    except NoSuchElementException:
        return None, None
