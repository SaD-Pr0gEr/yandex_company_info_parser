import logging
import time

from selenium.webdriver import Keys, Chrome
from selenium.webdriver.common.by import By

from parser import YandexMapsSeleniumParser

logger = logging.getLogger(__name__)


class Clicker:

    def __init__(self, driver: Chrome):
        self.driver = driver

    def scroll(self, scroll: int, selector: str, up: bool = False) -> None:
        for _ in range(scroll):
            self.driver.find_element(
                By.CSS_SELECTOR, selector
            ).send_keys(Keys.UP if up else Keys.DOWN)

    def scroll_down(self, scroll: int, selector: str = 'html') -> None:
        self.scroll(scroll, selector)

    def scroll_up(self, scroll: int, selector: str = 'html') -> None:
        self.scroll(scroll, selector, True)

    def scroll_over(self, count: int, per_page: int, scroll_count: int):
        scroll_range = round(count / per_page)
        logger.info('Scroll range: {}'.format(scroll_range))
        for i in range(scroll_range):
            logger.info(f'Scrolling: {i}')
            self.scroll_down(scroll_count)
            time.sleep(1)


class YandexMapsClicker(Clicker):

    def __init__(self, driver: Chrome, parser: YandexMapsSeleniumParser):
        super().__init__(driver)
        self.parser= parser

    def scroll_over_reviews(self) -> None:
        reviews_count = self.parser.parse_companies_expected_count()
        logger.info('Expected reviews count: {}'.format(reviews_count))
        per_page = 50
        self.scroll_over(reviews_count, per_page, 350)

    def scroll_over_photos(self) -> None:
        photos_count = self.parser.parse_photos_expected_count()
        logger.info('Expected photos count: {}'.format(photos_count))
        per_page = 6
        self.scroll_over(photos_count, per_page, 50)

    def set_language_to_ru(self):
        self.driver.find_element(
            By.CSS_SELECTOR, '.user-menu-control button'
        ).click()
        logger.info('Clicked menu btn')
        time.sleep(2)
        self.driver.find_element(
            By.CSS_SELECTOR, '.main-user-view__settings'
        ).click()
        logger.info('Clicked settings btn')
        self.driver.switch_to.window(self.driver.window_handles[1])
        logger.info('Switched to settings window')
        time.sleep(3)
        self.driver.find_elements(
            By.CSS_SELECTOR,
            'div.option > div > div > button'
        )[-1].click()
        logger.info('Clicked languages form')
        time.sleep(1)
        self.driver.find_elements(
            By.CSS_SELECTOR, '.popup__content .select__list span'
        )[0].click()
        logger.info('Clicked russian lang btn')
        time.sleep(1)
        self.driver.find_element(
            By.CSS_SELECTOR, '.form__controls button'
        ).click()
        logger.info('Clicked save btn')
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[0])
        logger.info('Switched to main window')
