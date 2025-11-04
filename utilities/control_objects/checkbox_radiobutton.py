"""
Represents checkable elements.
"""

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions

from utilities.control_objects.base_control import _BaseControl
from utilities.logger import get_logger


class _SelectOptionControl(_BaseControl):
    """
    Represents checkable elements for option selection.
    """

    @staticmethod
    def pre_action(func):
        """
        Decorator function for pre action.
        """

        def wrapper(self, *args, **kwargs):
            """
            Wait for the element to be present in order to perform actions.
            """
            self.logger.debug(f"Pre-action for {self}")
            self.logger.debug(f"Check '.element_to_be_clickable()' for {self}")
            if self.wait.until(expected_conditions.element_to_be_clickable(self.locator)):
                self.logger.debug("Pre-action: SUCCESS")
                return func(self, *args, **kwargs)
            raise AttributeError(f"{self} is not present")

        return wrapper

    def is_checked(self) -> bool:
        """
        Checks if element is checked.

        :return: True if element is checked, False otherwise.
        """
        self.logger.debug("Check '.is_selected()' for %s", self)
        return self.web_element.is_selected()

    @pre_action
    def select(self) -> None:
        """
        Selects element if not selected. Does nothing otherwise.

        :return: None
        """
        self.logger.debug("Select action for %s", self)
        if not self.is_checked():
            self.web_element.click()


class Radiobutton(_SelectOptionControl):
    """
    Represents radiobutton - element that allows to select only one option from a set.
    """

    def __init__(self, driver: WebDriver, locator: Tuple[str, str]) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        """
        super().__init__(driver, locator)
        self.logger = get_logger(__name__)


class Checkbox(_SelectOptionControl):
    """
    Represents checkbox - element that allows to select multiple options from a set.
    """

    def __init__(self, driver: WebDriver, locator: Tuple[str, str]) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        """
        super().__init__(driver, locator)
        self.logger = get_logger(__name__)

    @_SelectOptionControl.pre_action
    def deselect(self) -> None:
        """
        Deselects checkbox if selected. Does nothing otherwise.

        :return: None
        """
        self.logger.debug("Deselect action for %s", self)
        if self.is_checked():
            self.web_element.click()
