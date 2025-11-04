"""
Contains _BaseControl class as a creator class for Base Controls factory pattern
"""

from abc import ABC
from typing import Tuple

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utilities.logger import get_logger


class _BaseControl(ABC):
    """
    _BaseControl class as a parent (factory) for all controls in the framework.
    """

    def __init__(self, driver: WebDriver, locator: Tuple[str, str]) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        """
        self.driver = driver
        self.locator = locator
        self.web_element: WebElement = self.driver.find_element(*self.locator)
        self.wait = WebDriverWait(self.driver, 5)
        self.logger = get_logger(__name__)

    def __str__(self) -> str:
        return f"<WebElement: {self.locator}>"

    def is_displayed(self) -> bool:
        """
        Checks if element is visible on the page.

        :return: True if element is displayed, False otherwise.
        """
        self.logger.debug("Check '.is_displayed()' for %s", self)
        return self.web_element.is_displayed()

    def is_enabled(self) -> bool:
        """
        Checks if element is active and interactive.

        :return: True if element is enabled, False otherwise.
        """
        self.logger.debug("Check '.is_enabled()' for %s", self)
        return self.web_element.is_enabled()

    def is_present(self) -> bool:
        """
        Checks if element is present in DOM (visible or not).

        :return: True if element is present, False otherwise.
        """
        self.logger.debug("Check '.is_present()' for %s", self)
        if self.wait.until(expected_conditions.presence_of_element_located(self.locator)):
            return True
        return False

    @staticmethod
    def pre_action(func):
        """
        Decorator function for pre-action.
        """

        def wrapper(self, *args, **kwargs):
            """
            Wait for the element to be present in order to perform actions.
            """
            self.logger.debug(f"Pre-action for {self}")
            if self.is_present():
                self.logger.debug("Pre-action: SUCCESS")
                return func(self, *args, **kwargs)
            raise AttributeError(f"{self} is not present")

        return wrapper

    @pre_action
    def click(self) -> None:
        """
        Clicks the element.

        :return: None
        """
        self.logger.debug("Click element %s", self)
        self.web_element.click()

    def hover_over(self) -> None:
        """
        Hovers mouse cursor over the element.

        :return: None
        """
        self.logger.debug("Hover over element %s", self)
        action = ActionChains(self.driver)
        action.move_to_element(self.web_element).perform()
