from abc import ABC, abstractmethod
from typing import Optional

import typing_extensions as typing


class Feedback(typing.TypedDict):
    grade: str
    suggestion: Optional[str]


class Criterion(typing.TypedDict):
    title: str
    explanation: str


class Criteria(typing.TypedDict):
    criteria: list[Criterion]


class ImprovedRequirement(typing.TypedDict):
    improved_requirement: str


class AugmentedFeedback(typing.TypedDict):
    criterion: Criterion
    feedback: Feedback


class FeedbackCollection(typing.TypedDict):
    feedback_collection: list[AugmentedFeedback]


class AbstractApi(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def determine_criteria(self, unstructured_guideline: str) -> Criteria:
        pass

    @abstractmethod
    def analyze_requirement(self, criteria: Criteria, requirement: str) -> FeedbackCollection:
        pass

    @abstractmethod
    def refine_requirement(self, feedback: FeedbackCollection, requirement: str) -> ImprovedRequirement:
        pass
