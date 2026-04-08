import csv
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def scrape_national_league():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")   # optional: run invisibly
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )

    # NOTE: No chromedriver path needed – Selenium Manager resolves it.
    driver = webdriver.Chrome(options=chrome_options)

    try:
        out_dir = "National_League"
        os.makedirs(out_dir, exist_ok=True)

        for year in range(1876, 2026):
            url = f"https://www.baseball-almanac.com/yearly/yr{year}n.shtml"  # NL uses 'n'
            driver.get(url)
            logging.info(f"Opened {url}")

            # Wait for at least one table to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "table")))
            except TimeoutException:
                logging.error(f"No table found for {year}. Skipping.")
                continue

            tables = driver.find_elements(By.TAG_NAME, "table")
            logging.info(f"{len(tables)} table(s) detected for {year}")

            for idx, table in enumerate(tables, start=1):
                try:
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    if len(rows) < 2:
                        continue  # skip decorative tables

                    # Header
                    header_cells = rows[0].find_elements(By.TAG_NAME, "th") or \
                                   rows[0].find_elements(By.TAG_NAME, "td")
                    headers = [cell.text for cell in header_cells]

                    # Data rows
                    data = [
                        [cell.text for cell in r.find_elements(By.TAG_NAME, "td")]
                        for r in rows[1:]
                        if any(c.text.strip() for c in r.find_elements(By.TAG_NAME, "td"))
                    ]
                    if not data:
                        continue  # skip empty tables

                    # Save CSV
                    file_path = os.path.join(out_dir, f"{year}_Table_{idx}.csv")
                    with open(file_path, "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(headers)
                        writer.writerows(data)
                    logging.info(f"Saved {file_path}")

                except Exception as e:
                    logging.error(f"Error on {year} table {idx}: {e}")

    finally:
        driver.quit()
        logging.info("Chrome driver closed")

if __name__ == "__main__":
    scrape_national_league()
