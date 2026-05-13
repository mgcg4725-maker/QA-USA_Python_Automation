from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class UrbanRoutesPage:

    # --- Locators ---

    # Address fields
    FROM_FIELD = (By.ID, 'from')
    TO_FIELD = (By.ID, 'to')

    # Call a Taxi button
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(),'Call a taxi')]")

    # Supportive tariff
    SUPPORTIVE_TARIFF = (By.XPATH, "//div[contains(@class,'tcard') and .//div[text()='Supportive']]")
    SUPPORTIVE_TARIFF_ACTIVE = (By.XPATH, "//div[contains(@class,'tcard active') and .//div[text()='Supportive']]")

    # Phone number
    PHONE_NUMBER_BUTTON = (By.CLASS_NAME, 'np-text')
    PHONE_INPUT = (By.ID, 'phone')
    PHONE_NEXT_BUTTON = (By.XPATH, "//button[text()='Next']")
    SMS_CODE_INPUT = (By.ID, 'code')
    SMS_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Confirm']")

    # Payment / Credit card
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, 'pp-value-text')
    ADD_CARD_BUTTON = (By.CLASS_NAME, "pp-plus")
    CARD_NUMBER_INPUT = (By.XPATH, "//input[@id='number']")
    CARD_CVV_INPUT = (By.CSS_SELECTOR, '#code.card-input')
    CARD_LINK_BUTTON = (By.XPATH, "//button[text()='Link']")
    CLOSE_PAYMENT_MODAL = (By.XPATH, "//div[contains(@class,'payment-picker')]//button[contains(@class,'close-button')]")

    # Driver comment
    DRIVER_COMMENT_INPUT = (By.ID, 'comment')

    # Blanket and handkerchiefs
    # One selector to click, one to assert state
    BLANKET_SWITCH_CLICKABLE = (By.XPATH, "//div[contains(text(),'Blanket and handkerchiefs')]"
                                          "/following-sibling::div//span[contains(@class,'slider')]")
    BLANKET_CHECKBOX = (By.XPATH, "//div[contains(text(),'Blanket and handkerchiefs')]"
                                  "/following-sibling::div//input[@type='checkbox']")

    # Ice cream
    ICE_CREAM_COUNTER_PLUS = (By.XPATH, "//div[contains(text(),'Ice cream')]"
                                        "/following-sibling::div//div[contains(@class,'counter-plus')]")
    ICE_CREAM_COUNT = (By.XPATH, "//div[contains(text(),'Ice cream')]"
                                 "/following-sibling::div//div[contains(@class,'counter-value')]")

    # Order taxi button
    ORDER_TAXI_BUTTON = (By.CLASS_NAME, 'smart-button')

    # Car search modal
    CAR_SEARCH_MODAL = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Methods ---

    def set_from(self, address_from):
        field = self.wait.until(EC.presence_of_element_located(self.FROM_FIELD))
        field.clear()
        field.send_keys(address_from)

    def set_to(self, address_to):
        field = self.wait.until(EC.presence_of_element_located(self.TO_FIELD))
        field.clear()
        field.send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.FROM_FIELD).get_attribute('value')

    def get_to(self):
        return self.driver.find_element(*self.TO_FIELD).get_attribute('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        # Only click if Supportive is not already active
        try:
            self.driver.find_element(*self.SUPPORTIVE_TARIFF_ACTIVE)
        except:
            self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF)).click()

    def get_supportive_plan_text(self):
        # Returns text of the active supportive tariff element
        element = self.wait.until(EC.presence_of_element_located(self.SUPPORTIVE_TARIFF_ACTIVE))
        return element.text

    def fill_phone_number(self, phone_number):
        from helpers import retrieve_phone_code
        self.wait.until(EC.element_to_be_clickable(self.PHONE_NUMBER_BUTTON)).click()
        self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT)).send_keys(phone_number)
        self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON)).click()
        code = retrieve_phone_code(self.driver)
        self.wait.until(EC.presence_of_element_located(self.SMS_CODE_INPUT)).send_keys(code)
        self.wait.until(EC.element_to_be_clickable(self.SMS_CONFIRM_BUTTON)).click()

    def get_phone_number_text(self):
        return self.driver.find_element(*self.PHONE_NUMBER_BUTTON).text

    def fill_card(self, card_number, card_code):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()
        self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_INPUT)).send_keys(card_number)
        cvv_field = self.wait.until(EC.presence_of_element_located(self.CARD_CVV_INPUT))
        cvv_field.send_keys(card_code)
        # TAB moves focus away from CVV so the Link button becomes clickable
        cvv_field.send_keys(Keys.TAB)
        self.wait.until(EC.element_to_be_clickable(self.CARD_LINK_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.CLOSE_PAYMENT_MODAL)).click()

    def get_payment_method_text(self):
        return self.driver.find_element(*self.PAYMENT_METHOD_BUTTON).text

    def write_comment_for_driver(self, comment):
        field = self.wait.until(EC.presence_of_element_located(self.DRIVER_COMMENT_INPUT))
        field.send_keys(comment)

    def get_comment_for_driver(self):
        return self.driver.find_element(*self.DRIVER_COMMENT_INPUT).get_attribute('value')

    def order_blanket_and_handkerchiefs(self):
        # Click the slider to toggle on
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_SWITCH_CLICKABLE)).click()

    def is_blanket_selected(self):
        # Assert using get_property('checked') per project hints
        checkbox = self.wait.until(EC.presence_of_element_located(self.BLANKET_CHECKBOX))
        return checkbox.get_property('checked')

    def order_ice_creams(self, count=2):
        # Loop lives in pages.py per POM guidelines
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_COUNTER_PLUS)).click()

    def get_ice_cream_count(self):
        return int(self.wait.until(EC.presence_of_element_located(self.ICE_CREAM_COUNT)).text)

    def click_order_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_TAXI_BUTTON)).click()

    def is_car_search_modal_visible(self):
        modal = self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
        return modal.is_displayed()