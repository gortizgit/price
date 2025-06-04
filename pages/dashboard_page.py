from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.json_reader import load_json
from selenium.common.exceptions import TimeoutException

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # Espera explícita de hasta 15 segundos
        locators = load_json("locators/dashboard_locators.json")["dashboard_page"]
        self.dashboard_xpath = locators["dashboard"]
        self.productos_xpath = locators["productos_servicios"]
        self.nuevo_producto_xpath = locators["nuevo_producto"]
        self.informacion_xpath = locators["informacion"]
        self.buscar_detalle_xpath = locators["buscar_detalle"]
        self.resultado_detalle_xpath = locators["resultado_detalle"]

    def wait_for_visible(self, xpath, timeout=15):
        # Espera a que el elemento sea visible
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            return None

    def click_dashboard(self):
        # Hace clic en el botón del dashboard
        element = self.wait_for_visible(self.dashboard_xpath)
        if not element:
            return False
        element.click()
        return self.wait_for_visible(self.productos_xpath, 10) is not None

    def click_productos_y_servicios(self):
        # Hace clic en "Productos y Servicios" y maneja posibles errores de plan
        element = self.wait_for_visible(self.productos_xpath)
        if not element:
            return False
        element.click()

        nuevo_producto = self.wait_for_visible(self.nuevo_producto_xpath, 10)
        aviso = self.wait_for_visible("//span[contains(@class,'title-warning-error-plan')]", 2)

        if aviso:
            # Si hay aviso, intenta resolverlo
            info_btn = self.wait_for_visible(self.informacion_xpath, 5)
            if info_btn:
                info_btn.click()
            element = self.wait_for_visible(self.productos_xpath, 10)
            if not element:
                return False
            element.click()

            # Revalida condiciones después del segundo clic
            nuevo_producto = self.wait_for_visible(self.nuevo_producto_xpath, 10)
            aviso = self.wait_for_visible("//span[contains(@class,'title-warning-error-plan')]", 2)
            if aviso:
                return False

        return nuevo_producto is not None

    def click_nuevo_producto(self):
        # Hace clic en el botón para crear nuevo producto
        element = self.wait_for_visible(self.nuevo_producto_xpath)
        if not element:
            return False
        element.click()
        return True

    def buscar_detalle_producto(self, detalle):
        # Busca un producto ingresando su detalle
        input_field = self.wait_for_visible(self.buscar_detalle_xpath, 10)
        if not input_field:
            raise Exception("Campo de búsqueda no encontrado.")
        input_field.clear()
        input_field.send_keys(detalle)

    def existe_detalle_en_resultados(self, detalle):
        # Verifica si el detalle aparece en los resultados
        try:
            return WebDriverWait(self.driver, 10).until(lambda d: any(
                span.text.strip().lower() == detalle.lower()
                for span in d.find_elements(By.XPATH, self.resultado_detalle_xpath)
            ))
        except TimeoutException:
            return False
