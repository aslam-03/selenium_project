"""Task 1: Navigate to the Headphone Zone homepage and maximize the window."""

from __future__ import annotations

import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, SCROLL_PAUSE_SECONDS, get_wait


def _human_scroll(driver, passes: int = 4) -> None:
    """Scroll down in several increments, then return to the top."""

    for step in range(1, passes + 1):
        jitter = random.randint(120, 260)
        distance = 450 + (step * 180) + jitter
        driver.execute_script("window.scrollBy(arguments[0], arguments[1]);", 0, distance)
        time.sleep(SCROLL_PAUSE_SECONDS)

    # Small pause at the bottom before returning to the top
    time.sleep(SCROLL_PAUSE_SECONDS)
    driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", 0, 0)
    time.sleep(1)


def run(driver) -> None:
    """Open the Headphone Zone website and prepare the viewport."""

    driver.get(BASE_URL)
    try:
        driver.maximize_window()
    except Exception:  # pragma: no cover - some headless environments disallow this
        driver.set_window_size(1920, 1080)

    wait = get_wait(driver)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1.5)

    print("[Task1] Performing initial scroll to warm up page elements.")
    _human_scroll(driver)

    print("[Task1] Navigated to homepage and maximized window.")
