from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.json_reader import load_json

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Espera explícita de hasta 10 segundos
        locators = load_json("locators/login_locators.json")["login_page"]
        self.username_xpath = locators["username"]
        self.password_xpath = locators["password"]
        self.login_button_xpath = locators["login_button"]

    def enter_username(self, username):
        # Ingresa el nombre de usuario
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.username_xpath)))
        element.clear()
        element.send_keys(username)

    def enter_password(self, password):
        # Ingresa la contraseña
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.password_xpath)))
        element.clear()
        element.send_keys(password)

    def click_login(self):
        # Hace clic en el botón "Iniciar sesión"
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.login_button_xpath)))
        button.click()
