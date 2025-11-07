"""
Represents hyperlink controls.
"""

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver

from utilities.control_objects.base_control import _BaseControl
from utilities.logger import get_logger


class Link(_BaseControl):
    """
    Represents hyperlink <a> elements.
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
        Gets text from hyperlink.

        :return: string text from label
        """
        self.logger.debug("Get text action for %s", self)
        return self.web_element.text

    def get_href(self) -> str:
        """
        Gets Hypertext Reference (HREF) attribute from hyperlink.

        :return: URL of the page the hyperlink goes to
        """
        self.logger.debug("Get HREF action for %s", self)
        value = self.web_element.get_attribute("href")
        if isinstance(value, str):
            return value
        raise AttributeError(f"Could not retrieve 'href' attribute for {self}")
