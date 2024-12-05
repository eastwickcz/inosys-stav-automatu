from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import shutil
import smtplib
from email.mime.text import MIMEText

# Nastavení SMTP
SMTP_SERVER = "smtp.seznam.cz"
SMTP_PORT = 465
SMTP_USERNAME = "your_username@example.com"
SMTP_PASSWORD = "your_password"
SENDER_EMAIL = "your_sender_email@example.com"
RECIPIENT_EMAIL = "your_recipient_email@example.com"

# Nastavení přihlašovacích údajů pro webovou stránku
WEB_USERNAME = "your_web_username"
WEB_PASSWORD = "your_web_password"

# Funkce pro odeslání e-mailu
# Tato funkce využívá SMTP server pro odeslání upozornění na problém s automatem
def send_email(message):
    subject = "Automat stav upozornění"
    body = message

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECIPIENT_EMAIL], msg.as_string())
        server.quit()
        print("Email byl úspěšně odeslán.")
    except Exception as e:
        print(f"Chyba při odesílání emailu: {e}")

# Hlavní funkce pro automatizaci Selenium
# Tato funkce se připojuje na web, přihlašuje se a kontroluje stav automatu
def main():
    # Kontrola dostupnosti chromedriveru
    driver_path = shutil.which("chromedriver")
    if driver_path is None:
        print("Chyba: 'chromedriver' nebyl nalezen v PATH. Prosím ujistěte se, že je nainstalován a dostupný.")
        return

    # Nastavení možností prohlížeče (headless mód pro běh bez GUI)
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Přechod na stránku pro přihlášení
        driver.get("http://monitor.inosys.cz/")

        # Vyhledání a vyplnění pole pro login
        login_field = driver.find_element(By.ID, "login")
        login_field.send_keys(WEB_USERNAME)

        # Vyhledání a vyplnění pole pro heslo
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(WEB_PASSWORD)

        # Stisknutí tlačítka pro přihlášení
        submit_button = driver.find_element(By.CLASS_NAME, "submit")
        submit_button.click()

        # Přechod na stránku správce automatů po přihlášení
        driver.get("http://monitor.inosys.cz/spravce-automatu/")

        # Vyhledání tabulky s automaty a kontrola stavu automatů
        wait = WebDriverWait(driver, 10)
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='table table-hover tbl_uzivatelu']")))
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                # Kontrolujeme, jestli některý <td> má třídu 'red' nebo 'orange', což znamená problém
                status_cells = row.find_elements(By.XPATH, ".//td[@class='red' or @class='orange']")
                for cell in status_cells:
                    status_text = cell.text
                    message = f"Automat má problém: {status_text}"
                    send_email(message)
        except TimeoutException:
            print("Automaty jsou v pořádku nebo nebyla nalezena tabulka.")

    except Exception as e:
        print(f"Nastala chyba: {e}")
    finally:
        # Ukončení driveru
        driver.quit()

if __name__ == "__main__":
    main()
