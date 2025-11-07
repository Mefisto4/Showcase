"""
End-to-end tests of GreenKart Shop page.
"""

import json

import pytest

from pages.rsa_pages.green_kart_pages.green_kart_cart_page import GreenKartCheckoutPage
from pages.rsa_pages.green_kart_pages.green_kart_delivery_page import GreenKartDeliveryPage
from pages.rsa_pages.green_kart_pages.green_kart_main_page import GreenKartMainPage
from utilities.base_product import EmptyProductPlaceholder
from utilities.data_class import DataClass

TEST_DATA_PATH = "./test_data/test_green_kart_shop_e2e.json"
with open(file=TEST_DATA_PATH, encoding="utf-8") as json_file:
    data = json.load(json_file)


@pytest.fixture(scope="class")
def class_fixture(request, test_fixture):
    """
    Setup test specific fixture.
    """
    request.cls.tools = test_fixture
    request.cls.driver = request.cls.tools.driver
    request.cls.page = GreenKartMainPage(request.cls.driver)


@pytest.mark.e2e
@pytest.mark.usefixtures("class_fixture")
@pytest.mark.parametrize("test_data_set", data.get("order_basic"), scope="class")
class TestGreenKartShopOrderBasic:
    """
    Test basic order scenario.
    """

    # pylint: disable=no-member

    @pytest.fixture
    def test_data(self, test_data_set):
        """
        Test data fixture.

        :param test_data_set: dict
        :return: DataClass()
                        .product_name
                        .delivery_country
                        .type_len
        """
        return DataClass(test_data_set)

    def test_go_to_page(self, test_data):
        """Start test."""
        self.tools.logger.info("Start basic order scenario test for GreenKart Shop page.")
        self.tools.logger.info("Test product name: %s", test_data.product_name)
        self.page.go_to()

        assert self.page.get_title() == test_data.page_title

    def test_add_product_to_cart(self, test_data):
        """Test if product is added to cart."""
        self.tools.logger.info("Add product to cart and verify if cart info is correct.")
        self.page.add_product_to_cart(test_data.product_name, test_data.product_quantity)

        assert self.page.get_cart_items_number() == test_data.product_quantity
        assert self.page.get_cart_total_price() == test_data.product_price

    def test_cart_preview(self, test_data):
        """Test if cart preview works correctly."""
        self.tools.logger.info("Verify if cart preview shows correct data.")
        self.page.cart_preview_button.click()
        preview = self.page.get_cart_preview()
        products = preview.get_products()

        assert test_data.product_name in ", ".join(p for p in products.keys())

        product = EmptyProductPlaceholder()
        for key in products.keys():
            if test_data.product_name in key:
                product = products[key]

        assert product.quantity == test_data.product_quantity
        assert product.price == test_data.product_price
        assert product.total_price == test_data.product_price

    def test_checkout_page(self, test_data):
        """Test if checkout page works correctly."""
        self.tools.logger.info("Verify if checkout page shows correct data.")
        checkout_page = self.page.cart_preview_view.proceed_to_checkout()
        products = checkout_page.get_products()

        assert test_data.product_name in ", ".join(p for p in products.keys())

        product = EmptyProductPlaceholder()
        for key in products.keys():
            if test_data.product_name in key:
                product = products[key]

        assert product.quantity == test_data.product_quantity
        assert product.price == test_data.product_price
        assert product.total_price == test_data.product_price

    def test_delivery_page_country_selection(self, test_data):
        """Test if delivery page country selection works correctly."""
        self.tools.logger.info("Verify if delivery page country selection works correctly.")
        checkout_page = GreenKartCheckoutPage(self.driver)
        delivery_page = checkout_page.place_order()
        delivery_page.select_country_dropdown.select(test_data.delivery_country)

        assert delivery_page.select_country_dropdown.get_text() == test_data.delivery_country

    def test_delivery_page_proceed_without_consent(self, test_data):  # pylint: disable=unused-argument
        """Test if delivery page proceed without consent works correctly."""
        self.tools.logger.info("Verify if delivery page does not proceed without consent.")
        delivery_page = GreenKartDeliveryPage(self.driver)
        next_page = delivery_page.proceed()

        assert next_page is None
        assert delivery_page.terms_and_conditions_alert_label.is_displayed()

    def test_delivery_page_proceed_with_consent(self, test_data):  # pylint: disable=unused-argument
        """Test if delivery page proceed with consent works correctly."""
        self.tools.logger.info("Verify if delivery page proceed with consent.")
        delivery_page = GreenKartDeliveryPage(self.driver)
        delivery_page.terms_and_conditions_checkbox.select()

        assert not delivery_page.terms_and_conditions_alert_label.is_displayed()

    def test_order_confirmation_page(self, test_data):  # pylint: disable=unused-argument
        """Test if order confirmation page works correctly."""
        self.tools.logger.info("Verify if order confirmation page works correctly.")
        delivery_page = GreenKartDeliveryPage(self.driver)
        confirmation_page = delivery_page.proceed()

        assert confirmation_page.success_message_label.is_displayed()
        assert confirmation_page.success_message_text in confirmation_page.success_message_label.get_text()
        assert confirmation_page.home_link.is_displayed()

    def test_redirection(self, test_data):  # pylint: disable=unused-argument
        """Test if redirection works correctly."""
        self.tools.logger.info("Verify if user is being redirected to home page after successful purchase.")

        assert self.tools.wait.until(self.tools.ec.url_to_be(GreenKartMainPage.URL))

    def test_main_page_after_order(self, test_data):  # pylint: disable=unused-argument
        """Test if main page after purchase works correctly."""
        self.tools.logger.info("Verify if user's cart is reset after successful purchase.")

        assert self.page.get_cart_items_number() == 0
        assert self.page.get_cart_total_price() == 0


@pytest.mark.e2e
@pytest.mark.usefixtures("class_fixture")
@pytest.mark.parametrize("test_data_set", data.get("page_search_box"), scope="class")
@pytest.mark.skip(reason="to be implemented")
class TestGreenKartShopSearchBox:
    """
    Test search box scenario.
    """

    # pylint: disable=no-member

    @pytest.fixture
    def test_data(self, test_data_set):
        """
        Test data fixture.

        :param test_data_set: dict
        :return: DataClass()
                        .product_name
                        .delivery_country
                        .type_len
        """
        return DataClass(test_data_set)

    def test_go_to_page(self, test_data):
        """Start test."""
        self.tools.logger.info("Start search box scenario test for GreenKart Shop page.")
        self.page.go_to()

        assert self.page.get_title() == test_data.page_title


@pytest.mark.e2e
@pytest.mark.usefixtures("class_fixture")
@pytest.mark.parametrize("test_data_set", data.get("products_removal"), scope="class")
@pytest.mark.skip(reason="to be implemented")
class TestGreenKartShopOrderWithRemovals:
    """
    Test order with products removal scenario.
    """

    # pylint: disable=no-member

    @pytest.fixture
    def test_data(self, test_data_set):
        """
        Test data fixture.

        :param test_data_set: dict
        :return: DataClass()
                        .product_name
                        .delivery_country
                        .type_len
        """
        return DataClass(test_data_set)

    def test_go_to_page(self, test_data):
        """Start test."""
        self.tools.logger.info("Start order with products removal scenario test for GreenKart Shop page.")
        self.page.go_to()

        assert self.page.get_title() == test_data.page_title


@pytest.mark.e2e
@pytest.mark.usefixtures("class_fixture")
@pytest.mark.parametrize("test_data_set", data.get("discount_code"), scope="class")
@pytest.mark.skip(reason="to be implemented")
class TestGreenKartShopOrderWithDiscountCode:
    """
    Test order with discount code application scenario.
    """

    # pylint: disable=no-member

    @pytest.fixture
    def test_data(self, test_data_set):
        """
        Test data fixture.

        :param test_data_set: dict
        :return: DataClass()
                        .product_name
                        .delivery_country
                        .type_len
        """
        return DataClass(test_data_set)

    def test_go_to_page(self, test_data):
        """Start test."""
        self.tools.logger.info("Start order with discount code application scenario test for GreenKart Shop page.")
        self.page.go_to()

        assert self.page.get_title() == test_data.page_title
