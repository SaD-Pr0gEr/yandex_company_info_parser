from dataclasses import dataclass


@dataclass
class UserReview:
    full_name: str
    rating: int
    review: str
    review_link: str
    review_date: str

    def json(self) -> dict[str, str | int]:
        return {
            'full_name': self.full_name,
            'rating': self.rating,
            'review': self.review,
            'review_link': self.review_link,
            'review_date': self.review_date,
        }


@dataclass
class CompanyData:
    name: str
    photos: list[str]
    reviews: list[UserReview]

    def json(self) -> dict[str, str | int | list[dict[str, str | int]]]:
        return {
            'name': self.name,
            'photos': self.photos,
            'reviews': [review.json() for review in self.reviews],
        }
