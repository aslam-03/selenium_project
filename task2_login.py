"""Task 2: Trigger the login flow from the homepage."""

from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, EMAIL, PASSWORD, get_wait

_ACCOUNT_LOCATORS = (
    (By.CSS_SELECTOR, "a[href*='/account/login']"),
    (By.CSS_SELECTOR, "a[href*='/account']"),
    (By.XPATH, "//button[contains(@aria-label, 'Login') or contains(@aria-label, 'Account')]"),
    (By.XPATH, "//a[contains(@aria-label, 'Account')]"),
    (By.XPATH, "//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'login')]"),
    (By.XPATH, "//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'account')]"),
)


def _click_first(locator_iterable, wait):
    for by, value in locator_iterable:
        try:
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            return True
        except TimeoutException:
            continue
    return False


def run(driver) -> None:
    """Click the account button and attempt to sign in."""

    wait = get_wait(driver)

    if not _click_first(_ACCOUNT_LOCATORS, wait):
        print("[Task2] Account trigger not found via header. Navigating directly to login page.")
        driver.get(f"{BASE_URL.rstrip('/')}/account/login")

    try:
        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "customer[email]")))
    except TimeoutException:
        print("[Task2] Login form not detected; skipping credential entry.")
        return

    password_field = wait.until(EC.element_to_be_clickable((By.NAME, "customer[password]")))

    email_field.clear()
    email_field.send_keys(EMAIL)

    password_field.clear()
    password_field.send_keys(PASSWORD)

    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()

    time.sleep(2)

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        print("[Task2] Page did not finish loading after login attempt.")

    error_elements = driver.find_elements(By.CSS_SELECTOR, ".form__message--error, .errors, [data-error]")
    if error_elements:
        print("[Task2] Login attempt completed, but an error message was detected. Confirm credentials.")
    else:
        print("[Task2] Login sequence finished.")
