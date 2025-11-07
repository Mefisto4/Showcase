"""
Contains GreenKart delivery page objects.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.rsa_pages.green_kart_pages import GREEN_KART_DELIVERY_PAGE
from utilities.control_objects.button import Button
from utilities.control_objects.checkbox_radiobutton import Checkbox
from utilities.control_objects.dropdown import DropdownStatic
from utilities.control_objects.label import Label
from utilities.control_objects.link import Link
from utilities.logger import get_logger


class GreenKartDeliveryPage(BasePage):
    """
    Web page for Green Kart Shop delivery page.
    """

    URL = GREEN_KART_DELIVERY_PAGE

    def __init__(self, driver: WebDriver, url=URL) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param url: URL of webpage, i.e.: "https://www.google.com"
        """
        super().__init__(driver, url)
        self._locators = _GreenKartDeliveryPageLocators
        self.confirmation_view = _ConfirmationViewPage(self.driver)
        self.logger = get_logger(__name__)

    @property
    def select_country_dropdown(self) -> DropdownStatic:
        """Returns 'Choose Country' dropdown."""
        return DropdownStatic(self.driver, self._locators.CHOOSE_COUNTRY_DROPDOWN)

    @property
    def terms_and_conditions_checkbox(self) -> Checkbox:
        """Returns 'Agree to the Terms and Conditions' checkbox."""
        return Checkbox(self.driver, self._locators.TERMS_AND_CONDITIONS_CHECKBOX)

    @property
    def terms_and_conditions_alert_label(self) -> Label:
        """Returns no consent to the Terms and Conditions alert label."""
        return Label(self.driver, self._locators.TERMS_AND_CONDITIONS_ALERT_LABEL)

    @property
    def proceed_button(self) -> Button:
        """Returns 'Proceed' button."""
        return Button(self.driver, self._locators.PROCEED_BUTTON)

    def proceed(self) -> None | _ConfirmationViewPage:
        """
        Proceeds to the next purchase step.

        :return: _ConfirmationViewPage object if terms and conditions checkbox is selected, None otherwise.
        """
        flag = False
        if self.terms_and_conditions_checkbox.is_checked():
            flag = True
        self.proceed_button.click()
        if flag:
            return self.confirmation_view
        return None


class _ConfirmationViewPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        """
        super().__init__(driver)
        self._locators = _ConfirmationViewPageLocators
        self.success_message_text = "Thank you, your order has been placed successfully"
        self.logger = get_logger(__name__)

    @property
    def success_message_label(self) -> Label:
        """Returns success message label."""
        return Label(self.driver, self._locators.SUCCESS_MSG_LABEL)

    @property
    def home_link(self) -> Link:
        """Returns home page link."""
        return Link(self.driver, self._locators.HOME_LINK)


class _GreenKartDeliveryPageLocators:
    """
    Contains locators for GreenKartDeliveryPage.
    """

    # pylint: disable=too-few-public-methods

    CHOOSE_COUNTRY_DROPDOWN = (By.CSS_SELECTOR, "select")
    TERMS_AND_CONDITIONS_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    TERMS_AND_CONDITIONS_ALERT_LABEL = (By.CSS_SELECTOR, ".errorAlert")
    PROCEED_BUTTON = (By.XPATH, "//button[text()='Proceed']")


class _ConfirmationViewPageLocators:
    """
    Contains locators for ConfirmationViewPage.
    """

    # pylint: disable=too-few-public-methods

    SUCCESS_MSG_LABEL = (By.CSS_SELECTOR, ".wrapperTwo span")
    HOME_LINK = (By.LINK_TEXT, "Home")
