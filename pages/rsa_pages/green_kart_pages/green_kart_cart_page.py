"""
Contains GreenKart cart page objects.
"""

from __future__ import annotations

from typing import Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.rsa_pages.green_kart_pages import GREEN_KART_CART_PAGE
from pages.rsa_pages.green_kart_pages.green_kart_delivery_page import GreenKartDeliveryPage
from utilities.base_product import BaseProduct
from utilities.control_objects.button import Button
from utilities.control_objects.label import Label
from utilities.control_objects.textbox import Textbox
from utilities.logger import get_logger


class GreenKartCheckoutPage(BasePage):
    """
    Web page for Green Kart Shop checkout page.
    """

    URL = GREEN_KART_CART_PAGE

    def __init__(self, driver: WebDriver, url=URL) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param url: URL of webpage, i.e.: "https://www.google.com"
        """
        super().__init__(driver, url)
        self._locators = _GreenKartCheckoutPageLocators
        self.logger = get_logger(__name__)

    @property
    def dicount_code_textbox(self) -> Textbox:
        """Returns dicount code textbox."""
        return Textbox(self.driver, self._locators.DISCOUNT_CODE_TEXTBOX)

    @property
    def discount_code_apply_button(self) -> Button:
        """Returns discount code apply button."""
        return Button(self.driver, self._locators.DISCOUNT_CODE_APPLY_BUTTON)

    @property
    def place_order_button(self) -> Button:
        """Returns 'Place Order' button."""
        return Button(self.driver, self._locators.PLACE_ORDER_BUTTON)

    def get_number_of_items(self) -> float:
        """
        Returns 'No. of Items' value.

        :return: number of items in the cart
        """
        value = self.driver.find_element(*self._locators.NO_OF_ITEMS_LABEL).get_attribute("wholeText")
        if isinstance(value, str):
            return float(value.strip(" "))
        raise TypeError(f"Received unexpected value type:\n TYPE: {type(value)}\n EXPECTED: <class 'str'>\n")

    def get_total_amount(self) -> float:
        """
        Returns 'Total Amount' value.

        :return: total price of the cart
        """
        value = Label(self.driver, self._locators.TOTAL_AMOUNT_LABEL).get_text()
        return float(value)

    def get_discount_value(self) -> float:
        """
        Returns 'Discount' value.

        :return: percent value of the discount
        """
        value = Label(self.driver, self._locators.DISCOUNT_LABEL).get_text().strip("%")
        return float(value)

    def get_total_after_discount(self) -> float:
        """
        Returns 'Total After Discount' value.

        :return: total price of the cart after discount
        """
        value = Label(self.driver, self._locators.TOTAL_AFTER_DISCOUNT_LABEL).get_text()
        return float(value)

    def get_products(self) -> Dict[str, _CheckoutProduct]:
        """
        Returns all products presented in checkout table.

        :return: dict['product_name'] = _CheckoutProduct
        """
        elems = self.driver.find_element(*self._locators.PRODUCTS_TABLE).find_elements(By.CSS_SELECTOR, "tbody tr")
        products = [_CheckoutProduct(elem) for elem in elems]
        return {product.name: product for product in products}

    def place_order(self) -> GreenKartDeliveryPage:
        """
        Proceeds to the next purchase step.

        :return: GreenKartDeliveryPage
        """
        self.place_order_button.click()
        return GreenKartDeliveryPage(self.driver)


class _CheckoutProduct(BaseProduct):
    @property
    def name(self) -> str:
        return self.web_element.find_element(By.CSS_SELECTOR, "td:nth-child(2) .product-name").text

    @property
    def price(self) -> float:
        value = self.web_element.find_element(By.CSS_SELECTOR, "td:nth-child(4) .amount").text
        return float(value)

    @property
    def quantity(self) -> float:
        value = self.web_element.find_element(By.CSS_SELECTOR, "td:nth-child(3) .quantity").text
        return float(value)

    @property
    def total_price(self) -> float:
        value = self.web_element.find_element(By.CSS_SELECTOR, "td:nth-child(5) .amount").text
        return float(value)


class _GreenKartCheckoutPageLocators:
    """
    Contains locators for GreenKartCheckoutPage.
    """

    # pylint: disable=too-few-public-methods

    PRODUCTS_TABLE = (By.ID, "productCartTables")
    DISCOUNT_CODE_TEXTBOX = (By.CSS_SELECTOR, "")
    DISCOUNT_CODE_APPLY_BUTTON = (By.CSS_SELECTOR, "")
    NO_OF_ITEMS_LABEL = (By.XPATH, "//*[@id='root']/div/div/div/div/text()")
    TOTAL_AMOUNT_LABEL = (By.CSS_SELECTOR, ".totAmt")
    DISCOUNT_LABEL = (By.CSS_SELECTOR, ".discountPerc")
    TOTAL_AFTER_DISCOUNT_LABEL = (By.CSS_SELECTOR, ".discountAmt")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Place Order']")
