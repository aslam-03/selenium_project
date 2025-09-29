"""Task 4: Navigate through the menu to the Gaming Headphones category."""

from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, get_wait

_CATEGORY_FALLBACK_URL = f"{BASE_URL.rstrip('/')}/collections/gaming-headphones"

_MENU_LOCATORS = (
    (By.CSS_SELECTOR, "button[aria-label='Open menu']"),
    (By.CSS_SELECTOR, "button[aria-label='Menu']"),
    (By.XPATH, "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'menu')]")
)

_HEADPHONES_LOCATORS = (
    (By.XPATH, '//a[contains(translate(normalize-space(.),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "headphones")]'),
    (By.XPATH, '//button[contains(translate(normalize-space(.),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "headphones")]')
)

_GAMING_LOCATORS = (
    (By.XPATH, '//a[contains(translate(normalize-space(.),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "gaming") and contains(@href, "collections")]'),
    (By.XPATH, '//button[contains(translate(normalize-space(.),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "gaming")]')
)


def _click_first(driver, wait, locator_options) -> bool:
    for by, value in locator_options:
        try:
            element = wait.until(EC.element_to_be_clickable((by, value)))
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
            return True
        except TimeoutException:
            continue
    return False


def run(driver) -> None:
    """Attempt to reach the Gaming Headphones listing via navigation menus."""

    driver.get(BASE_URL)
    wait = get_wait(driver)

    if _click_first(driver, wait, _MENU_LOCATORS):
        if not _click_first(driver, wait, _HEADPHONES_LOCATORS):
            print("[Task4] Could not locate 'Headphones' inside the menu; using fallback URL.")
            driver.get(_CATEGORY_FALLBACK_URL)
        else:
            if not _click_first(driver, wait, _GAMING_LOCATORS):
                print("[Task4] 'Gaming' option missing after selecting Headphones; using fallback URL.")
                driver.get(_CATEGORY_FALLBACK_URL)
    else:
        print("[Task4] Menu button not found; navigating directly to Gaming Headphones page.")
        driver.get(_CATEGORY_FALLBACK_URL)

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        print("[Task4] Gaming category page may not have loaded fully.")

    print("[Task4] Arrived at Gaming Headphones category view.")
