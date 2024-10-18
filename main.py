import json
import logging
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from clicker import YandexMapsClicker
from config import DRIVERS_DIR, DUMP_DATA_DIR, load_paths
from data_types import CompanyData
from parser import YandexMapsSeleniumParser
from utils import get_company_slug_ame_from_maps_url

logger = logging.getLogger(__name__)


def run(urls: list[str]):
    logging.basicConfig(
        level=logging.INFO,
        format=(
            u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - '
            u'%(name)s - %(message)s'
        )
    )
    logger.info('Starting... Initializing services')
    load_paths([DUMP_DATA_DIR])
    service = Service(executable_path=str(DRIVERS_DIR / 'chromedriver'))
    options = Options()
    # options.add_argument('--headless')
    browser = Chrome(service=service, options=options)
    parser = YandexMapsSeleniumParser(browser)
    clicker = YandexMapsClicker(browser, parser)
    logger.info('Clicker initialized')
    try:
        clicker.driver.get(urls[0])
        time.sleep(5)
        logger.info(f'Page loaded to set lang')
        clicker.set_language_to_ru()
        logger.info('LANGUAGE SET TO RU')
        for url in urls:
            clicker.driver.get(url)
            time.sleep(10)
            logger.info(f'Page loaded: {url}')
            company_name = parser.parse_company_name()
            clicker.driver.find_element(
                By.CSS_SELECTOR, '.orgpage-header-view__header'
            ).click()
            clicker.scroll_over_reviews()
            logger.info('Scrolled over reviews')
            review_objects = parser.get_review_elements()
            logger.info(f'Reviews count: {len(review_objects)}')
            time.sleep(3)
            reviews = parser.parse_reviews(review_objects)
            logger.info('Parsed reviews')
            parser.get_company_photos_tab_element().click()
            time.sleep(1)
            clicker.scroll_over_photos()
            logger.info('Scrolled over photos')
            photo_objects = parser.get_photo_elements()
            logger.info(f'Photos count: {len(photo_objects)}')
            photo_links = parser.parse_photo_links(photo_objects)
            logger.info('Parsed photos')
            company_reviews = CompanyData(
                company_name, photo_links, reviews
            )
            filename = get_company_slug_ame_from_maps_url(url)
            with open(
                DUMP_DATA_DIR / f'{filename}.json', 'w', encoding='utf-8'
            ) as f:
                json.dump(
                    company_reviews.json(), f, indent=4, ensure_ascii=False
                )
    except Exception as e:
        logger.error('UNEXPECTED EXCEPTION: {}'.format(e))
    finally:
        browser.quit()


if __name__ == '__main__':
    run([
        'https://yandex.ru/maps/org/psikhodemiya/211368448914/reviews/?ll=37.652283%2C55.759177&z=14', # example url
    ])
