from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utils.json_reader import load_json

class AddProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Espera explícita de hasta 10 segundos
        locators = load_json("locators/dashboard_locators.json")["add_product_page"]  # Carga los XPaths desde el JSON
        self.nombre_producto = locators["nombre_producto"]
        self.buscar_btn = locators["buscar_btn"]
        self.primer_checkbox = locators["primer_checkbox"]
        self.siguiente_btn = locators["siguiente_btn"]
        self.medida_comercial = locators["medida_comercial"]
        self.precio_unitario = locators["precio_unitario"]
        self.dropdown_medida = locators["dropdown_medida"]
        self.detalle = locators["detalle"]
        self.guardar_btn = locators["guardar_btn"]
        self.detalle_ingresado = ""  # Almacena el detalle ingresado

    def wait_for_element(self, xpath, timeout=10):
        # Espera a que el elemento esté presente en el DOM
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def ingresar_nombre_producto(self, nombre):
        # Ingresa el nombre del producto en el campo correspondiente
        input_field = self.wait_for_element(self.nombre_producto)
        input_field.clear()
        input_field.send_keys(nombre)

    def click_buscar(self):
        # Hace clic en el botón "Buscar"
        self.wait_for_element(self.buscar_btn).click()

    def seleccionar_primer_checkbox(self):
        # Selecciona el primer checkbox si no está ya seleccionado
        checkbox = self.wait_for_element(self.primer_checkbox)
        if not checkbox.is_selected():
            checkbox.click()

    def click_siguiente(self):
        # Hace clic en el botón "Siguiente"
        self.wait_for_element(self.siguiente_btn).click()

    def ingresar_medida_comercial(self, medida):
        # Ingresa la medida comercial del producto
        input_field = self.wait_for_element(self.medida_comercial)
        input_field.clear()
        input_field.send_keys(medida)

    def ingresar_precio_unitario(self, precio):
        # Ingresa el precio unitario del producto
        input_field = self.wait_for_element(self.precio_unitario)
        input_field.clear()
        input_field.send_keys(str(precio))

    def seleccionar_medida_dropdown(self, index=1):
        # Selecciona una opción del dropdown de medidas por índice
        select_element = self.wait_for_element(self.dropdown_medida)
        select = Select(select_element)
        if len(select.options) > index:
            select.select_by_index(index)

    def ingresar_detalle(self, detalle):
        # Ingresa el detalle del producto
        input_field = self.wait_for_element(self.detalle)
        input_field.clear()
        input_field.send_keys(detalle)
        self.detalle_ingresado = detalle

    def click_guardar(self):
        # Hace clic en el botón "Guardar"
        self.wait_for_element(self.guardar_btn).click()
