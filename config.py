"""Shared configuration and utilities for the Headphone Zone Selenium project."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait


BASE_URL = "https://www.headphonezone.in/"
EMAIL = "aslamachu8558@gmail.com"
PASSWORD = "Ar-rahman"
DEFAULT_TIMEOUT = 15
SCROLL_PAUSE_SECONDS = 1.25


@dataclass(slots=True)
class DriverConfig:
    """Runtime options for the Selenium Chrome driver."""

    headless: bool = False
    implicit_wait: float = 5
    user_data_dir: Optional[str] = None


def create_driver(config: DriverConfig | None = None) -> webdriver.Chrome:
    """Instantiate a Chrome WebDriver with sane defaults.

    Args:
        config: Optional overrides for the Chrome session.

    Returns:
        A configured ``webdriver.Chrome`` instance.
    """

    config = config or DriverConfig()

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    if config.headless:
        chrome_options.add_argument("--headless=new")

    if config.user_data_dir:
        chrome_options.add_argument(f"--user-data-dir={config.user_data_dir}")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(config.implicit_wait)
    return driver


def get_wait(driver: webdriver.Chrome, timeout: int = DEFAULT_TIMEOUT) -> WebDriverWait:
    """Return a WebDriverWait bound to ``driver``."""

    return WebDriverWait(driver, timeout)
