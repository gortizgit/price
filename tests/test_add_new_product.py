import sys
import os

# Asegura que el directorio raíz del proyecto esté en sys.path para que se puedan importar los módulos personalizados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.add_product_page import AddProductPage
from utils.json_reader import load_json
import uuid

@pytest.fixture(scope="function")
def driver():
    """Fixture que inicializa y cierra el navegador para cada test."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_new_product(driver):
    """Test principal: agrega un nuevo producto y verifica que fue creado correctamente."""

    # Cargar las credenciales de acceso desde un archivo JSON de configuración
    creds = load_json("config/credentials.json")
    url = creds["brand_url"]
    username = creds["credentials"]["username"]
    password = creds["credentials"]["password"]

    # Abrir la aplicación web
    driver.get(url)

    # Iniciar sesión
    login_page = LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    # Ir al módulo de productos y servicios
    dashboard_page = DashboardPage(driver)
    assert dashboard_page.click_productos_y_servicios(), "No se pudo abrir 'Productos y Servicios'"
    assert dashboard_page.click_nuevo_producto(), "No se pudo hacer clic en 'Nuevo producto'"

    # Instanciar la página de agregar producto
    add_product_page = AddProductPage(driver)

    # Buscar un producto base por nombre
    add_product_page.ingresar_nombre_producto("t")
    add_product_page.click_buscar()
    add_product_page.seleccionar_primer_checkbox()
    add_product_page.click_siguiente()

    # Generar datos únicos para el producto a agregar
    medida = f"Medida{uuid.uuid4().hex[:5]}"
    detalle = f"Detalle {uuid.uuid4().hex[:8]}"

    # Completar los campos del formulario del nuevo producto
    add_product_page.ingresar_medida_comercial(medida)
    add_product_page.ingresar_precio_unitario(100)
    add_product_page.seleccionar_medida_dropdown()
    add_product_page.ingresar_detalle(detalle)
    add_product_page.click_guardar()

    # Buscar el producto por su detalle y verificar que existe en los resultados
    dashboard_page.buscar_detalle_producto(detalle)
    assert dashboard_page.existe_detalle_en_resultados(detalle), "El detalle del producto no fue encontrado en los resultados"
