"""
Contains GreenKart main page objects.
"""

from __future__ import annotations

from typing import Dict, Tuple

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from pages.rsa_pages.green_kart_pages import GREEN_KART_MAIN_PAGE
from pages.rsa_pages.green_kart_pages.green_kart_cart_page import GreenKartCheckoutPage
from utilities.base_product import BaseProduct
from utilities.control_objects.button import Button
from utilities.control_objects.label import Label
from utilities.control_objects.textbox import Textbox
from utilities.logger import get_logger


class GreenKartMainPage(BasePage):
    """
    Web page for Green Kart Shop main page.
    """

    URL = GREEN_KART_MAIN_PAGE

    def __init__(self, driver: WebDriver, url=URL) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param url: URL of webpage, i.e.: "https://www.google.com"
        """
        super().__init__(driver, url)
        self._locators = _GreenKartMainPageLocators
        self.cart_preview_view = _CartPreviewView(self.driver)
        self.logger = get_logger(__name__)

    @property
    def search_form_textbox(self) -> Textbox:
        """Returns search form textbox."""
        return Textbox(self.driver, self._locators.SEARCH_FORM_TEXTBOX)

    @property
    def search_form_button(self) -> Button:
        """Returns search button."""
        return Button(self.driver, self._locators.SEARCH_FORM_BUTTON)

    @property
    def cart_preview_button(self) -> Button:
        """Returns cart preview button."""
        return Button(self.driver, self._locators.CART_ICON)

    def _get_cart_info(self, locator: Tuple[str, str]) -> float:
        label = Label(self.driver, locator)
        return float(label.get_text())

    def get_cart_items_number(self) -> float:
        """
        Returns 'Items' value.

        :return: number of items in cart.
        """
        return self._get_cart_info(self._locators.CART_INFO_ITEMS_LABEL)

    def get_cart_total_price(self) -> float:
        """
        Returns 'Price' value.

        :return: total price of cart.
        """
        return self._get_cart_info(self._locators.CART_INFO_PRICE_LABEL)

    def get_product(self, product_name: str) -> _MainPageProduct:
        """
        Returns product object if displayed on the page.

        :param product_name: partial product name.
        :return: _MainPageProduct object
        """
        products = self.driver.find_elements(*self._locators.PRODUCTS)
        for product in products:
            if product_name in product.find_element(By.CSS_SELECTOR, ".product-name").text:
                return _MainPageProduct(self.driver, product)
        raise ValueError(f"Product {product_name} not found")

    def search_for_product(self, product_name: str) -> _MainPageProduct:
        """
        Searches for the product using search form and returns product object if found.

        :param product_name: partial product name.
        :return: _MainPageProduct object
        """
        self.search_form_textbox.set_text(product_name)
        self.search_form_button.click()
        return self.get_product(product_name)

    def add_product_to_cart(self, product_name: str, quantity: float = 1.0) -> None:
        """
        Adds product to cart.

        :param product_name: partial product name.
        :param quantity: amount of product to be added.
        :return: None
        """
        product = self.get_product(product_name)
        if quantity != 1.0:
            product.set_quantity(quantity)
        product.add_to_cart()

    def get_cart_preview(self) -> _CartPreviewView:
        """
        Activates and returns cart preview view.

        :return: _CartPreviewView
        """
        elem = self.driver.find_elements(*self._locators.CART_PREVIEW_ACTIVE)
        is_active = len(elem) > 0
        if not is_active:
            self.cart_preview_button.click()
        return self.cart_preview_view


class _MainPageProduct(BaseProduct):
    def __init__(self, driver: WebDriver, web_element: WebElement) -> None:
        """

        :param web_element: web element of <div class='product'>
        """
        super().__init__(web_element)
        self._driver = driver
        self.wait = WebDriverWait(self._driver, 5)
        self.logger = get_logger(__name__)

    @property
    def name(self) -> str:
        return self.web_element.find_element(By.CSS_SELECTOR, ".product-name").text

    @property
    def price(self) -> float:
        value = self.web_element.find_element(By.CSS_SELECTOR, ".product-price").text
        return float(value)

    @property
    def quantity(self) -> float:
        value = self.web_element.find_element(By.CSS_SELECTOR, ".quantity").get_attribute("valueAsNumber")
        if isinstance(value, str):
            return float(value)
        raise TypeError(f"Received unexpected value type:\n TYPE: {type(value)}\n EXPECTED: <class 'str'>\n")

    @property
    def total_price(self) -> float:
        return self.price

    def add_to_cart(self) -> None:
        """
        Adds product to cart.

        :return: None
        """
        self.web_element.find_element(By.CSS_SELECTOR, ".product-action button[type='button']").click()

    def set_quantity(self, quantity: float) -> None:
        """
        Sets product quantity.

        :param quantity: amount to be set
        :return: None
        """
        obj = self.web_element.find_element(By.CSS_SELECTOR, ".quantity")
        obj.clear()
        obj.send_keys(str(quantity))
        obj.send_keys(Keys.RETURN)

    def increase_quantity(self, by_value: int = 1) -> None:
        """
        Increases product quantity by clicking '+' button.

        :param by_value: how many times to click '+' button
        :return: None
        """
        quantity = self.quantity
        for _ in range(by_value):
            self.web_element.find_element(By.CSS_SELECTOR, ".increment").click()
            self.wait.until(lambda x: self.quantity == quantity + 1.0)

    def decrease_quantity(self, by_value: int = 1) -> None:
        """
        Decreases product quantity by clicking '-' button.

        :param by_value: how many times to click '-' button
        :return: None
        """
        quantity = self.quantity
        for _ in range(by_value):
            self.web_element.find_element(By.CSS_SELECTOR, ".decrement").click()
            self.wait.until(lambda x: self.quantity == quantity - 1.0)


class _CartPreviewView:
    def __init__(self, driver: WebDriver) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        """
        self.driver = driver
        self._locators = _CartPreviewViewLocators
        self.logger = get_logger(__name__)

    @property
    def proceed_to_checkout_button(self) -> Button:
        """Returns 'PROCEED TO CHECKOUT' button."""
        return Button(self.driver, self._locators.PROCEED_TO_CHECKOUT_BUTTON)

    def get_products(self) -> Dict[str, _CartPreviewProduct]:
        """
        Returns all products presented in cart preview view.

        :return: dict['product_name'] = _CheckoutProduct
        """
        elems = self.driver.find_element(*self._locators.PRODUCTS_LIST).find_elements(*self._locators.PRODUCTS)
        products = [_CartPreviewProduct(elem) for elem in elems]
        return {product.name: product for product in products}

    def proceed_to_checkout(self) -> GreenKartCheckoutPage:
        """
        Proceeds to the next purchase step.

        :return: GreenKartCheckoutPage
        """
        self.proceed_to_checkout_button.click()
        return GreenKartCheckoutPage(self.driver)


class _CartPreviewProduct(BaseProduct):
    def __init__(self, web_element: WebElement) -> None:
        """

        :param web_element: web element of <div class='product'>
        """
        super().__init__(web_element)
        self.logger = get_logger(__name__)

    @property
    def name(self) -> str:
        return self.web_element.find_element(By.CSS_SELECTOR, ".product-info .product-name").text

    @property
    def price(self) -> float:
        value = self.web_element.find_element(By.CSS_SELECTOR, ".product-info .product-price").text
        return float(value)

    @property
    def quantity(self) -> float:
        value = self.web_element.find_element(By.CSS_SELECTOR, ".product-total .quantity").text
        return float(value.split(" ")[0])

    @property
    def total_price(self) -> float:
        value = self.web_element.find_element(By.CSS_SELECTOR, ".product-total .amount").text
        return float(value)

    def remove_from_cart(self) -> None:
        """
        Removes product from cart.

        :return: None
        """
        self.web_element.find_element(By.CSS_SELECTOR, ".product-remove").click()


class _GreenKartMainPageLocators:
    """
    Contains locators for GreenKartMainPage
    """

    # pylint: disable=too-few-public-methods

    PRODUCTS = (By.CSS_SELECTOR, ".product")
    SEARCH_FORM_TEXTBOX = (By.CSS_SELECTOR, ".search-keyword")
    SEARCH_FORM_BUTTON = (By.CSS_SELECTOR, ".search-button")
    CART_INFO_ITEMS_LABEL = (By.CSS_SELECTOR, ".cart-info tr:nth-child(1) td:nth-child(3)")
    CART_INFO_PRICE_LABEL = (By.CSS_SELECTOR, ".cart-info tr:nth-child(2) td:nth-child(3)")
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon")
    CART_PREVIEW_ACTIVE = (By.CSS_SELECTOR, "div[class='cart-preview active']")


class _CartPreviewViewLocators:
    """
    Contains locators for CartPreviewView
    """

    # pylint: disable=too-few-public-methods

    PRODUCTS_LIST = (By.CSS_SELECTOR, "ul[class='cart-items']")
    PRODUCTS = (By.CSS_SELECTOR, ".cart-item")
    PROCEED_TO_CHECKOUT_BUTTON = (By.XPATH, "//button[text()='PROCEED TO CHECKOUT']")
