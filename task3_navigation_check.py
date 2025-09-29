"""Task 3: Visit several key pages and scroll to mimic a browsing session."""

from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, SCROLL_PAUSE_SECONDS, get_wait

BROWSE_PATHS = [
    "collections/new-launches",
    "collections/headphones",
    "collections/wireless-bluetooth-headphones",
    "blogs/audiophile-101",
]


def _absolute_url(path: str) -> str:
    return f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def _human_scroll(driver, passes: int = 4) -> None:
    for step in range(1, passes + 1):
        driver.execute_script("window.scrollBy(arguments[0], arguments[1]);", 0, 500 + (step * 150))
        time.sleep(SCROLL_PAUSE_SECONDS)
    driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", 0, 0)
    time.sleep(1)


def run(driver) -> None:
    """Cycle through curated pages, waiting for their content and scrolling."""

    wait = get_wait(driver)

    for path in BROWSE_PATHS:
        url = _absolute_url(path)
        driver.get(url)
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except TimeoutException:
            print(f"[Task3] Timed out waiting for page load: {url}")
            continue

        print(f"[Task3] Browsing {url}")
        _human_scroll(driver)
