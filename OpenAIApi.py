from AbstractApi import AbstractApi, Criteria, Feedback, ImprovedRequirement, AugmentedFeedback
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("openai-api-key")
SEED = int(os.getenv("seed"))
MODEL = os.getenv("openai-model")


def prompt_model_openai_json(messages, model, structured_format):
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.beta.chat.completions.parse(model=model, messages=messages,
                                                    response_format=structured_format, seed=SEED)
    response = completion.choices[0].message.parsed
    return response.json()

class OpenAIApi(AbstractApi):

    def __init__(self, model):
        super().__init__(model)

    def determine_criteria(self, unstructured_guideline: str) -> Criteria:
        system_prompt = """You are responsible for the quality assurance of requirements for software projects. Your task is to generate a checklist from unstructured text that describes which criteria a singular requirements artifact should fulfil. The checklist is later used to check the quality of a requirement, so each item on the checklist should be independent and as narrow as possible.
        Example: "Guideline: "Title
        Should identify the desired feature quickly
        Should be meaningful and unique
        Should be written from a user's point of view where applicable
        Context should be indicated by prefix, for example, Simulink: ..., SAP: ..., UI: ..., C++ Check: ..."
        Expected checklist: 
        ""The issue title should identify the desired feature quickly"
        "The issue title should be meaningful and unique"
        "The issue title should be written from a user's point of view where applicable"
        "The issue title should have its context indicated by prefix, for example, Simulink: ..."""""
        user_prompt = f"""Generate a checklist for the following guideline: "{unstructured_guideline}\""""
        messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}]
        return prompt_model_openai_json(messages, self.model, Criteria)

    def analyze_requirement(self, criteria: Criteria, requirement: str) -> AugmentedFeedback:
        system_prompt = """You are responsible for the quality assurance of requirements for software projects. You will be given a software requirement and a check. You are supposed to determine how well the requirement fulfils the check. You can assign grades from A to F (A being the best, F the worst, everything below D is considered a failing grade).
       Furthermore, you should provide feedback that a human can use to increase the quality of the requirement if possible.
       Example: "Requirement: "As a user, I should be able to click a button to purchase my order".
       Check: "The user story should clearly articulate the benefit to the user, presenting the functionality from the user's viewpoint."
       Expected answer:
       "Grade: "E", Suggestion: "The benefit the user gains from the functionality is missing and should be present"""""
        user_prompt = f"""Determine how well the requirement fulfills the check and provide feedback if possible:
        {requirement}"""
        messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt},
                    {'role': 'user', 'content': user_prompt}, {'role': 'user', 'content': criterion}]
        return prompt_model_openai_json(messages, self.model, Criteria)

    def refine_requirement(self, feedback: list[Feedback], requirement: str) -> ImprovedRequirement:
        """"""
