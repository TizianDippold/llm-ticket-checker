from AbstractApi import AbstractApi, Feedback, ImprovedRequirement, Criteria, Criterion, AugmentedFeedback, \
    FeedbackCollection


class MockApi(AbstractApi):
    def __init__(self, model):
        super().__init__(model)


    def determine_criteria(self, unstructured_guideline: str) -> Criteria:
        print("MockApi determine_criteria was called")
        criterion: Criterion = {'title' : 'TestCriterion', 'explanation' : "TestExplanation"}
        criteria: Criteria = {'criteria' : [criterion]}
        return criteria

    def analyze_requirement(self, criteria: Criteria, requirement: str) -> FeedbackCollection:
        print("MockApi analyze_requirement was called")
        feedback: Feedback = {'grade': 'B', 'suggestion': 'This is a mock suggestion.'}
        augmented_feedback: AugmentedFeedback = {'feedback': feedback, 'criterion': criteria['criteria'][0]}
        feedback_collection: FeedbackCollection = {'feedback_collection': [augmented_feedback]}
        return feedback_collection

    def refine_requirement(self, feedback: list[AugmentedFeedback], requirement: str) -> ImprovedRequirement:
        print("MockApi refine_requirement was called")
        improved_requirement: ImprovedRequirement = {'improved_requirement': requirement + ' (Refined)'}
        return improved_requirement

