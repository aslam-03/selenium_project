"""Task 6: Select a filtered product and add it to the shopping cart."""

from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, get_wait

_CATEGORY_URL = f"{BASE_URL.rstrip('/')}/collections/gaming-headphones"

_PRODUCT_LOCATOR = (
    By.XPATH,
    "(//a[contains(@href, '/products/') and (contains(@class, 'card') or contains(@class, 'product'))])[1]",
)

_ADD_TO_CART_LOCATORS = (
    (By.XPATH, "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'add to cart')]")
        ,
    (By.CSS_SELECTOR, "button[name='add']"),
)

_CONFIRMATION_LOCATORS = (
    (By.CSS_SELECTOR, "[id*='Cart']"),
    (By.CSS_SELECTOR, "div.cart-notification"),
    (By.XPATH, "//a[contains(@href, '/cart')]"),
)


def run(driver) -> None:
    """Open the first available product from the filtered list and add it to the cart."""

    driver.get(_CATEGORY_URL)
    wait = get_wait(driver)

    try:
        product_tile = wait.until(EC.element_to_be_clickable(_PRODUCT_LOCATOR))
    except TimeoutException:
        print("[Task6] No product tiles detected on the page.")
        return

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product_tile)
    time.sleep(0.5)
    product_tile.click()

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        print("[Task6] Product page did not complete loading.")

    for by, value in _ADD_TO_CART_LOCATORS:
        try:
            add_button = wait.until(EC.element_to_be_clickable((by, value)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
            time.sleep(0.5)
            add_button.click()
            break
        except TimeoutException:
            add_button = None
            continue
    else:
        print("[Task6] Unable to locate the add-to-cart button.")
        return

    time.sleep(2)

    for by, value in _CONFIRMATION_LOCATORS:
        try:
            wait.until(EC.presence_of_element_located((by, value)))
            print("[Task6] Item added to cart (confirmation detected).")
            return
        except TimeoutException:
            continue

    print("[Task6] Add-to-cart action executed, but confirmation was not detected.")
