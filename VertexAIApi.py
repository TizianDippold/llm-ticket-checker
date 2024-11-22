from AbstractApi import AbstractApi, Feedback, ImprovedRequirement, Criteria


class VertexAIApi(AbstractApi):

    def determine_criteria(self, unstructured_guideline: str) -> Criteria:
        pass

    def analyze_requirement(self, criterion: str, requirement: str) -> Feedback:
        pass

    def refine_requirement(self, feedback: list[Feedback], requirement: str) -> ImprovedRequirement:
        pass

    def __init__(self, model):
        super().__init__(model)