"""Task 5: Apply availability, price, and brand filters on the gaming category."""

from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, get_wait

_CATEGORY_URL = f"{BASE_URL.rstrip('/')}/collections/gaming-headphones"


def _scroll_into_view(driver, element) -> None:
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.6)


def _expand_section(driver, wait, keyword: str) -> bool:
    locators = (
        (By.XPATH, f"//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{keyword}')]")
        ,
        (By.XPATH, f"//summary[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{keyword}')]")
        ,
        (By.XPATH, f"//details[contains(@id, '{keyword.title()}')]/summary"),
    )
    for by, value in locators:
        try:
            section_trigger = wait.until(EC.element_to_be_clickable((by, value)))
            _scroll_into_view(driver, section_trigger)
            section_trigger.click()
            time.sleep(0.8)
            return True
        except TimeoutException:
            continue
    return False


def _toggle_checkbox(driver, wait, keyword: str) -> bool:
    locator = (
        By.XPATH,
        f"//label[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{keyword}')]",
    )
    try:
        checkbox_label = wait.until(EC.element_to_be_clickable(locator))
    except TimeoutException:
        return False

    _scroll_into_view(driver, checkbox_label)
    checkbox_label.click()
    time.sleep(0.5)
    return True


def _set_price_range(driver, wait, minimum: int, maximum: int) -> bool:
    selectors = [
        (By.CSS_SELECTOR, "input[name='filter.v.price.gte']"),
        (By.CSS_SELECTOR, "input[name='filter.p.price.gte']"),
    ]
    min_input = None
    for selector in selectors:
        try:
            min_input = wait.until(EC.presence_of_element_located(selector))
            break
        except TimeoutException:
            continue
    if not min_input:
        return False

    max_input = None
    for selector in (
        (By.CSS_SELECTOR, "input[name='filter.v.price.lte']"),
        (By.CSS_SELECTOR, "input[name='filter.p.price.lte']"),
    ):
        try:
            max_input = wait.until(EC.presence_of_element_located(selector))
            break
        except TimeoutException:
            continue
    if not max_input:
        return False

    _scroll_into_view(driver, min_input)
    min_input.clear()
    min_input.send_keys(str(minimum))

    _scroll_into_view(driver, max_input)
    max_input.clear()
    max_input.send_keys(str(maximum))

    time.sleep(0.5)
    return True


def _select_brands(driver, wait, count: int = 5) -> int:
    brand_inputs = []
    try:
        brand_inputs = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "input[type='checkbox'][name*='brand']")
            )
        )
    except TimeoutException:
        pass

    selected = 0
    for checkbox in brand_inputs:
        if selected >= count:
            break
        checkbox_id = checkbox.get_attribute("id")
        if not checkbox_id:
            continue
        label = driver.find_element(By.CSS_SELECTOR, f"label[for='{checkbox_id}']")
        _scroll_into_view(driver, label)
        if not checkbox.is_selected():
            label.click()
            time.sleep(0.4)
        selected += 1
    return selected


def _apply_filters(driver, wait) -> None:
    locators = (
        (By.XPATH, "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'apply')]"),
        (By.CSS_SELECTOR, "button[data-filter-apply]"),
    )
    for by, value in locators:
        try:
            apply_button = wait.until(EC.element_to_be_clickable((by, value)))
            _scroll_into_view(driver, apply_button)
            apply_button.click()
            time.sleep(1.5)
            return
        except TimeoutException:
            continue


def run(driver) -> None:
    """Apply desired filters on the gaming headphones listing."""

    driver.get(_CATEGORY_URL)
    wait = get_wait(driver)

    try:
        filter_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'filter')]")
            )
        )
    except TimeoutException:
        print("[Task5] Filter control not found on the page.")
        return

    _scroll_into_view(driver, filter_button)
    filter_button.click()
    time.sleep(1)

    if not _expand_section(driver, wait, "availability"):
        print("[Task5] Unable to expand the Availability filter section.")
    elif not _toggle_checkbox(driver, wait, "in stock"):
        print("[Task5] 'In Stock' option not found.")

    if not _expand_section(driver, wait, "price"):
        print("[Task5] Unable to expand the Price filter section.")
    elif not _set_price_range(driver, wait, 0, 5000):
        print("[Task5] Could not set the price range inputs.")

    if not _expand_section(driver, wait, "brand"):
        print("[Task5] Unable to expand the Brand filter section.")
    else:
        selected_count = _select_brands(driver, wait)
        if selected_count < 5:
            print(f"[Task5] Only {selected_count} brand options were selected; fewer than requested.")

    _apply_filters(driver, wait)

    print("[Task5] Filter sequence executed.")
