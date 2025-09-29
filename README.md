# Headphone Zone Selenium Automation

An end-to-end Selenium workflow that exercises critical buyer journeys on [headphonezone.in](https://www.headphonezone.in/). The suite orchestrates six focused tasks (navigation, login, browsing, category drilling, filtering, and carting) through a shared Chrome session.

## Prerequisites

- Python 3.10+
- Google Chrome 115+ (the bundled Selenium Manager will fetch a matching driver)
- Recommended: create and activate a virtual environment before installing dependencies

## Install dependencies

```cmd
pip install -r requirements.txt
```

## Configure credentials & runtime

Edit `config.py` and update:

- `EMAIL` / `PASSWORD` with valid Headphone Zone credentials
- Optional: adjust `DEFAULT_TIMEOUT`, `SCROLL_PAUSE_SECONDS`, or enable headless mode via `DriverConfig`

## Run the automation

```cmd
python main.py
```

Additional flags:

- `--headless` to suppress the browser UI
- `--implicit-wait` to tweak Selenium's implicit wait (default 5 seconds)

## Task breakdown

| Task file | Responsibility |
| --- | --- |
| `task1_navigate.py` | load homepage and maximize the viewport |
| `task2_login.py` | trigger the account flow and submit credentials |
| `task3_navigation_check.py` | hop through curated sections with human-like scrolling |
| `task4_category_selection.py` | reach the Gaming Headphones category through the menu (with URL fallback) |
| `task5_filters.py` | apply availability, price, and brand filters on the listing |
| `task6_add_to_cart.py` | open a filtered product and add it to the cart |

All steps are linked together by `main.py` using a single shared browser session.

## Troubleshooting tips

- If the UI layout changes, adjust the locators inside the relevant task module.
- When running headless, some sites block automation. Try without `--headless` if elements are not found.
- Use `SCROLL_PAUSE_SECONDS` in `config.py` to slow down or speed up human-like scrolling between steps.
