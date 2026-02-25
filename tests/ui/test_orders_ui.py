"""UI tests for Order Board (Selenium)."""
import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.app import app as flask_app
from src.data_store import clear_orders

HOST = "127.0.0.1"
PORT = 5099


@pytest.fixture(scope="module")
def live_server():
    """Start Flask in a background thread for Selenium tests."""
    clear_orders()
    server = threading.Thread(
        target=lambda: flask_app.run(host=HOST, port=PORT, use_reloader=False),
        daemon=True,
    )
    server.start()
    time.sleep(1)
    yield f"http://{HOST}:{PORT}"
    clear_orders()


@pytest.fixture()
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(options=opts)
    yield drv
    drv.quit()


@pytest.mark.ui
def test_page_title(driver, live_server):
    driver.get(live_server)
    assert "Order Board" in driver.title


@pytest.mark.ui
def test_create_order_via_ui(driver, live_server):
    driver.get(live_server)
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "customer").send_keys("UIUser")
    driver.find_element(By.ID, "item").send_keys("Gadget")
    driver.find_element(By.ID, "quantity").send_keys("3")
    driver.find_element(By.ID, "price").send_keys("19.99")
    driver.find_element(By.ID, "add-btn").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "orders-body"), "UIUser"))
    rows = driver.find_elements(By.CSS_SELECTOR, "#orders-body tr")
    assert any("UIUser" in r.text for r in rows)


@pytest.mark.ui
def test_delete_order_via_ui(driver, live_server):
    driver.get(live_server)
    wait = WebDriverWait(driver, 10)
    # Create an order first
    driver.find_element(By.ID, "customer").send_keys("ToDelete")
    driver.find_element(By.ID, "item").send_keys("Thing")
    driver.find_element(By.ID, "quantity").send_keys("1")
    driver.find_element(By.ID, "price").send_keys("5.00")
    driver.find_element(By.ID, "add-btn").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "orders-body"), "ToDelete"))
    # Find and click the delete button in the "ToDelete" row specifically
    rows = driver.find_elements(By.CSS_SELECTOR, "#orders-body tr")
    for row in rows:
        if "ToDelete" in row.text:
            row.find_element(By.CSS_SELECTOR, ".del-btn").click()
            break
    # Wait for "ToDelete" to disappear from the table
    wait.until(lambda d: "ToDelete" not in d.find_element(By.ID, "orders-body").text)
    rows = driver.find_elements(By.CSS_SELECTOR, "#orders-body tr")
    assert all("ToDelete" not in r.text for r in rows)
