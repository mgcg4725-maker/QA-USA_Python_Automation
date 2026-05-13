from selenium import webdriver
from pages import UrbanRoutesPage
import data
from helpers import is_url_reachable


class TestUrbanRoutes:


    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.get(data.URBAN_ROUTES_URL)
        cls.routes_page = UrbanRoutesPage(cls.driver)
        if is_url_reachable(data.URBAN_ROUTES_URL):
            print("Urban Routes is reachable, starting tests...")
        else:
            print("Urban Routes is not reachable, aborting starting tests...")

    def test_set_route(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.routes_page.get_from() == data.ADDRESS_FROM
        assert self.routes_page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi()
        self.routes_page.select_supportive_plan()
        assert 'Supportive' in self.routes_page.get_supportive_plan_text()

    def test_fill_phone_number(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi()
        self.routes_page.select_supportive_plan()
        self.routes_page.fill_phone_number(data.PHONE_NUMBER)
        assert data.PHONE_NUMBER in self.routes_page.get_phone_number_text()

    def test_fill_card(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi()
        self.routes_page.select_supportive_plan()
        self.routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.routes_page.get_payment_method_text() == 'Card'

    def test_comment_for_driver(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi()
        self.routes_page.select_supportive_plan()
        self.routes_page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        assert self.routes_page.get_comment_for_driver() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi()
        self.routes_page.select_supportive_plan()
        self.routes_page.order_blanket_and_handkerchiefs()
        assert self.routes_page.is_blanket_selected() == True

    def test_order_2_ice_creams(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi()
        self.routes_page.select_supportive_plan()
        self.routes_page.order_ice_creams(count=2)
        assert self.routes_page.get_ice_cream_count() == 2

    def test_car_search_model_appears(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi()
        self.routes_page.select_supportive_plan()
        self.routes_page.fill_phone_number(data.PHONE_NUMBER)
        self.routes_page.write_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        self.routes_page.click_order_taxi()
        assert self.routes_page.is_car_search_modal_visible() == True
    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

