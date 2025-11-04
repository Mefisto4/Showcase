"""
Represents simple, clickable controls.
"""

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver

from utilities.control_objects.base_control import _BaseControl
from utilities.logger import get_logger


class Button(_BaseControl):
    """
    Represents button elements.
    """

    def __init__(self, driver: WebDriver, locator: Tuple[str, str]) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        """
        super().__init__(driver, locator)
        self.logger = get_logger(__name__)
