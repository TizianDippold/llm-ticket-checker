import json
import os

import requests

from AbstractApi import AbstractApi, Criteria, Feedback, ImprovedRequirement, AugmentedFeedback

OLLAMA_BASE_URL = os.getenv("ollama_base_url")
SEED = 42

def prompt_model_ollama_json(prompt, model):
    """Sends a request to the specified model via Ollama. The prompt must specify that the result should be valid json.
    :return: Json object created from the answer"""
    response = requests.post(OLLAMA_BASE_URL + 'api/generate/', json={
        'model': model,
        'prompt': prompt,
        'format': 'json',
        'stream': False,
        'seed': SEED
    })
    response.raise_for_status()
    content = json.loads(json.loads(response.content).get('response'))
    return content

class OllamaApi(AbstractApi):

    def __init__(self, model):
        super().__init__(model)

    def determine_criteria(self, unstructured_guideline: str) -> Criteria:
        system_prompt = (
            "You are responsible for the quality assurance of requirements for software projects. "
            "Your task is to generate a checklist from unstructured text that describes which criteria "
            "a singular requirements artifact should fulfill. The checklist is later used to check the quality "
            "of a requirement, so each item on the checklist should be independent and as narrow as possible.\n"
            "Example: \"Guideline: Title should identify the desired feature quickly, should be meaningful and unique, "
            "should be written from a user's point of view where applicable, context should be indicated by prefix, "
            "for example, Simulink: ..., SAP: ..., UI: ..., C++ Check: ...\"\n"
            "Expected checklist: \n"
            "1. The issue title should identify the desired feature quickly.\n"
            "2. The issue title should be meaningful and unique.\n"
            "3. The issue title should be written from a user's point of view where applicable.\n"
            "4. The issue title should have its context indicated by prefix, e.g., Simulink: ...\n"
            "Answer using JSON format."
        )
        user_prompt = f'Generate a checklist for the following guideline: "{unstructured_guideline}"'
        prompt = f"{system_prompt}\n{user_prompt}"
        result = prompt_model_ollama_json(prompt, self.model)
        return Criteria(criteria=result.get('criteria', []))

    def analyze_requirement(self, criteria: Criteria, requirement: str) -> AugmentedFeedback:
        system_prompt = (
            "You are responsible for the quality assurance of requirements for software projects. "
            "You will be given a software requirement and a check. You are supposed to determine "
            "how well the requirement fulfills the check. You can assign grades from A to F "
            "(A being the best, F the worst, everything below D is considered a failing grade). "
            "Furthermore, you should provide feedback that a human can use to increase the quality "
            "of the requirement if possible.\n"
            "Example: Requirement: \"As a user, I should be able to click a button to purchase my order\".\n"
            "Check: \"The user story should clearly articulate the benefit to the user, presenting "
            "the functionality from the user's viewpoint.\"\n"
            "Expected answer: Grade: \"E\", Suggestion: \"The benefit the user gains from the functionality "
            "is missing and should be present\"\n"
            "Answer using JSON format."
        )
        user_prompt = f"Determine how well the requirement fulfills the check and provide feedback if possible: {requirement}"
        prompt = f"{system_prompt}\n{user_prompt}\nCriterion: {criterion}"
        result = prompt_model_ollama_json(prompt, self.model)
        return Feedback(grade=result.get('grade', ''), suggestion=result.get('suggestion', ''))

    def refine_requirement(self, feedback: list[Feedback], requirement: str) -> ImprovedRequirement:
        pass