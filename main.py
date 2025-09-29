"""Entry point to execute the Headphone Zone Selenium automation suite."""

from __future__ import annotations

import argparse
import sys
import time
from typing import Callable, Iterable

from config import DriverConfig, create_driver
import task1_navigate
import task2_login
import task3_navigation_check
import task4_category_selection
import task5_filters
import task6_add_to_cart

TaskFn = Callable[[object], None]

_TASK_SEQUENCE: Iterable[tuple[str, TaskFn]] = (
    ("Task 1 - Navigate", task1_navigate.run),
    ("Task 2 - Login", task2_login.run),
    ("Task 3 - Navigation Check", task3_navigation_check.run),
    ("Task 4 - Category Selection", task4_category_selection.run),
    ("Task 5 - Filters", task5_filters.run),
    ("Task 6 - Add to Cart", task6_add_to_cart.run),
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Headphone Zone automation runner")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode (useful for CI environments).",
    )
    parser.add_argument(
        "--implicit-wait",
        type=float,
        default=5.0,
        help="Implicit wait duration in seconds configured on the WebDriver.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    driver = create_driver(DriverConfig(headless=args.headless, implicit_wait=args.implicit_wait))

    try:
        for step_name, task_fn in _TASK_SEQUENCE:
            print(f"\n[Main] Starting {step_name}")
            task_fn(driver)
            time.sleep(1)
        print("\n[Main] All tasks completed successfully.")
        return 0
    except Exception as exc:  # noqa: BLE001 - top-level guard
        print(f"\n[Main] Aborting sequence due to unexpected error: {exc!r}")
        return 1
    finally:
        print("[Main] Closing browser session.")
        driver.quit()


if __name__ == "__main__":
    sys.exit(main())
