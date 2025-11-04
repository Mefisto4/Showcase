"""
Contains BasePage class as a creator class for Page Objects factory pattern
"""

from selenium.webdriver.remote.webdriver import WebDriver

from utilities.logger import get_logger


class BasePage:
    """
    BasePage Object class as a parent (factory) for all page objects in the framework.
    """

    URL = ""

    def __init__(self, driver: WebDriver, url: str = URL) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param url: URL of webpage, i.e.: "https://www.google.com"
        """
        self.driver = driver
        self.url = url
        self.logger = get_logger(__name__)

    def go_to(self) -> None:
        """
        Open webpage in the browser.

        :return: None
        """
        self.logger.debug("Go to '%s'", self.url)
        self.driver.get(self.url)

    def get_title(self) -> str:
        """
        Gets title of current page.

        :return: page title
        """
        self.logger.debug("Get title for %s", self)
        return self.driver.title

    def get_height(self) -> int:
        """
        Gets height of current page.

        :return: page height in [px]
        """
        self.logger.debug("Get height for %s", self)
        height = self.driver.execute_script("return document.body.scrollHeight")
        if isinstance(height, int):
            return height
        raise TypeError(f"Received unexpected value type:\n TYPE: {type(height)}\n EXPECTED: <class 'int'>\n")

    def get_width(self) -> int:
        """
        Gets width of current page.

        :return: page width in [px]
        """
        self.logger.debug("Get width for %s", self)
        width = self.driver.execute_script("return document.body.scrollWidth")
        if isinstance(width, int):
            return width
        raise TypeError(f"Received unexpected value type:\n TYPE: {type(width)}\n EXPECTED: <class 'int'>\n")

    def scroll(self, x: int = 0, y: int = 0) -> None:
        """
        Scrolls current page. The origin of the coordinate system is in top-left corner of the page.

        :param x: horizontal value
        :param y: vertical value
        :return: None
        """
        self.logger.debug("Scroll to x:'%s', y:'%s' action for %s", x, y, self)
        self.driver.execute_script(f"window.scrollTo({x}, {y});")

    def scroll_to_bottom(self) -> None:
        """
        Scrolls to the bottom of the page.

        :return: None
        """
        self.logger.debug("Scroll to bottom action for %s", self)
        self.scroll(y=self.get_height())

    def scroll_to_top(self) -> None:
        """
        Scrolls to the top of the page.

        :return: None
        """
        self.logger.debug("Scroll to top action for %s", self)
        self.scroll()
