"""Конфигурации и фикстуры для тестов."""

import logging
from logging.handlers import RotatingFileHandler

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    """Фикстура для запуска браузера."""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('log-level=3')
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield browser

    browser.quit()


@pytest.fixture()
def log():
    """Фикстура для логов."""
    logger = logging.getLogger(__name__)
    handler = RotatingFileHandler(
        'main.log', maxBytes=50000000, backupCount=5
    )
    handler.setFormatter(logging.Formatter(u'[%(levelname)s] %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
