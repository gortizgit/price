import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.add_product_page import AddProductPage
from utils.json_reader import load_json
import uuid

@pytest.fixture(scope="function")
def driver():
    # Setup del navegador para cada test
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_new_product(driver):
    # Carga las credenciales desde archivo
    creds = load_json("config/credentials.json")
    url = creds["brand_url"]
    username = creds["credentials"]["username"]
    password = creds["credentials"]["password"]

    # Inicia sesión en la aplicación
    driver.get(url)
    login_page = LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    # Navega al área de productos
    dashboard_page = DashboardPage(driver)
    assert dashboard_page.click_productos_y_servicios()
    assert dashboard_page.click_nuevo_producto()

    # Agrega un nuevo producto
    add_product_page = AddProductPage(driver)
    add_product_page.ingresar_nombre_producto("t")
    add_product_page.click_buscar()
    add_product_page.seleccionar_primer_checkbox()
    add_product_page.click_siguiente()

    # Datos únicos para el producto
    medida = f"Medida{uuid.uuid4().hex[:5]}"
    detalle = f"Detalle {uuid.uuid4().hex[:8]}"
    add_product_page.ingresar_medida_comercial(medida)
    add_product_page.ingresar_precio_unitario(100)
    add_product_page.seleccionar_medida_dropdown()
    add_product_page.ingresar_detalle(detalle)
    add_product_page.click_guardar()

    # Verifica que el producto fue creado
    dashboard_page.buscar_detalle_producto(detalle)
    assert dashboard_page.existe_detalle_en_resultados(detalle)
