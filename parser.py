from datetime import datetime

from selenium.common import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from data_types import UserReview


class YandexMapsSeleniumParser:

    def __init__(self, driver: Chrome):
        self.driver = driver

    def get_map_company_tabs_elements(self) -> list[WebElement]:
        return self.driver.find_elements(
            By.CSS_SELECTOR,
            '.carousel__item .tabs-select-view__title'
        )

    def get_company_photos_tab_element(self) -> WebElement:
        return self.get_map_company_tabs_elements()[1]

    def parse_companies_expected_count(self) -> int:
        companies_count_text = self.driver.find_element(
            By.CSS_SELECTOR, '.card-section-header__title'
        )
        return int(companies_count_text.text.split()[0])

    def parse_photos_expected_count(self) -> int:
        return int(self.driver.find_element(
            By.CSS_SELECTOR,
            '.tabs-select-view__title .tabs-select-view__counter'
        ).text)

    def get_photo_elements(self) -> list[WebElement]:
        return self.driver.find_elements(
            By.CSS_SELECTOR, 'img.media-wrapper__media'
        )

    def parse_photo_links(
        self, photo_elements: list[WebElement] | None = None
    ) -> list[str]:
        photo_elements = photo_elements or self.get_photo_elements()
        return [
            photo.get_attribute('src')
            for photo in photo_elements
        ]

    def parse_company_name(self) -> str:
        return self.driver.find_element(
            By.CSS_SELECTOR, 'h1.orgpage-header-view__header'
        ).text

    def get_review_elements(self) -> list[WebElement]:
        return self.driver.find_elements(
            By.CSS_SELECTOR, '.business-reviews-card-view__review'
        )

    def parse_reviews(
        self, review_elements: list[WebElement] | None = None
    ) -> list[UserReview]:
        review_elements = review_elements or self.get_review_elements()
        obj_list: list[UserReview] = []
        for element in review_elements:
            try:
                full_name = element.find_element(
                    By.CSS_SELECTOR,
                    '.business-review-view__author-container '
                    '.business-review-view__author-name a span'
                ).text
            except NoSuchElementException:
                full_name = 'Неизвестно'
            try:
                rating = len(element.find_elements(
                    By.CSS_SELECTOR,
                    '.business-review-view__rating span._full'
                ))
            except NoSuchElementException:
                rating = 1
            try:
                review = element.find_element(
                    By.CSS_SELECTOR,
                    '.business-review-view__body '
                    'span.business-review-view__body-text'
                ).text
            except NoSuchElementException:
                review = 'Неизвестно'
            try:
                user_id = element.find_element(
                    By.CSS_SELECTOR,
                    '.business-review-view__user-icon[href]'
                ).get_attribute('href').split('/')[-1]
            except NoSuchElementException:
                user_id = ''
            map_id = self.driver.current_url.split('/')[-3]
            review_link = (
                f'https://yandex.ru/maps/org/{map_id}/reviews?'
                f'reviews[publicId]={user_id}&utm_source=review'
            )
            try:
                review_date = element.find_element(
                    By.CSS_SELECTOR, '.business-review-view__date span'
                ).text
            except NoSuchElementException:
                review_date = datetime.now().strftime("%m/%d/%Y")
            obj = UserReview(
                full_name, rating, review, review_link, review_date
            )
            obj_list.append(obj)
        return obj_list
