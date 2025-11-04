"""
Represents simple elements that allow to input and display text.
"""

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver

from utilities.control_objects.base_control import _BaseControl
from utilities.logger import get_logger


class Textbox(_BaseControl):
    """
    Represents textbox elements.
    """

    def __init__(self, driver: WebDriver, locator: Tuple[str, str]) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        """
        super().__init__(driver, locator)
        self.logger = get_logger(__name__)

    def get_text(self) -> str:
        """
        Gets text from textbox.

        :return: displayed text
        """
        self.logger.debug("Get text action for %s", self)
        value = self.web_element.get_attribute("value")
        if isinstance(value, str):
            return value
        raise AttributeError(f"Could not retrieve 'value' attribute for {self}")

    @_BaseControl.pre_action
    def set_text(self, value) -> None:
        """
        Sets text in textbox.

        :param value: text to be set
        :return: None
        """
        self.logger.debug("Set text '%s' action for %s", value, self)
        self.web_element.clear()
        self.web_element.send_keys(value)
        if (text := self.get_text()) != value:
            raise ValueError(f"Text was not set. Actual: {text}; Expected: {value}")
