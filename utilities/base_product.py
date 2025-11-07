"""
Contains BaseProduct class as a creator class for Shopping Products factory pattern
"""

from abc import ABC, abstractmethod
from unittest.mock import Mock

from selenium.webdriver.remote.webelement import WebElement

from utilities.logger import get_logger


class BaseProduct(ABC):
    """
    BaseProduct class as a parent (factory) for all shopping products in the framework.
    """

    def __init__(self, web_element: WebElement) -> None:
        """

        :param web_element: web element containing product details
        """
        self.web_element = web_element
        self.logger = get_logger(__name__)

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns product name."""

    @property
    @abstractmethod
    def price(self) -> float:
        """Returns product price."""

    @property
    @abstractmethod
    def quantity(self) -> float:
        """Returns product quantity."""

    @property
    @abstractmethod
    def total_price(self) -> float:
        """Returns product total_price price - should be equal to (quantity * price)."""


class EmptyProductPlaceholder(BaseProduct):
    """
    Empty product placeholder.
    """

    def __init__(self) -> None:
        super().__init__(Mock())

    @property
    def name(self) -> str:
        return "None"

    @property
    def price(self) -> float:
        return -9.99

    @property
    def quantity(self) -> float:
        return -9.99

    @property
    def total_price(self) -> float:
        return -9.99
