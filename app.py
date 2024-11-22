import json
from os import DirEntry
from typing import LiteralString, TypedDict, Type, List, T, Dict, Any, TypeVar, get_type_hints
from pathlib import Path
from dotenv import load_dotenv
import os
from AbstractApi import AbstractApi, Criterion, Criteria, AugmentedFeedback, FeedbackCollection, ImprovedRequirement
from MockApi import MockApi
from OllamaApi import OllamaApi
from OpenAIApi import OpenAIApi
from VertexAIApi import VertexAIApi
from itertools import product


# Function generated using GPT-4o
def unique_combinations(list1, list2):
    """Generate all unique combinations of elements from two lists."""
    # Use itertools.product to generate Cartesian product of the two lists
    all_combinations = product(list1, list2)

    # Convert to a set to ensure uniqueness
    unique_combinations_set = set(all_combinations)

    # Convert back to a list or sorted list if specific order is needed
    result = sorted(unique_combinations_set)

    return result


# Class generated using GPT-4o
class ApiFactory:
    _api_cache = {}

    @staticmethod
    def get_api(model: str) -> AbstractApi:
        """Returns the corresponding API for the model, reusing existing instances."""
        # Check if the instance already exists
        if model in ApiFactory._api_cache:
            return ApiFactory._api_cache[model]

        # Determine which API to use based on the model name
        api_instance = None
        if model.startswith("gpt"):
            api_instance = OpenAIApi(model)
        elif model.startswith("llama"):
            api_instance = OllamaApi(model)
        elif model.startswith("meta"):
            api_instance = VertexAIApi(model)
        elif model.startswith("mock"):
            api_instance = MockApi(model)
        else:
            raise ValueError(f"Unsupported model: {model}")

        # Cache the new instance
        ApiFactory._api_cache[model] = api_instance
        return api_instance


def generate_criteria(model: str, subject: str, subjects_folder: str):
    """Generates a new file in which the deducted criteria are stored as json if it does not exist yet."""
    subject_path = os.path.join(subjects_folder, subject)
    criteria_path = os.path.join(subject_path, model + "_criteria.json")
    guideline_path = os.path.join(subject_path, "guideline")
    if not os.path.isfile(criteria_path):
        with open(guideline_path, "r", encoding='utf-8') as guideline_file:
            guideline_text = guideline_file.read()

            # Get the API using the provided model
            api: AbstractApi = ApiFactory.get_api(model)
            criteria: Criteria = api.determine_criteria(guideline_text)

            write_typed_dict_to_json(criteria, criteria_path)


# Function generated using GPT-4o
def write_typed_dict_to_json(typed_dict_instance: Dict[str, Any], file_path: str) -> None:
    """
    Writes a dictionary (TypedDict instance) to a JSON file.

    :param typed_dict_instance: A dictionary or TypedDict instance to be serialized.
    :param file_path: The path where the JSON file will be saved.
    """
    # Write the dictionary to the specified file
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(typed_dict_instance, file, ensure_ascii=False, indent=4)


# Function generated using GPT-4o
def load_json_as_typed_dict(path: str, cls: Type[TypedDict]) -> TypedDict:
    def parse_value(value: Any, expected_type: Any) -> Any:
        if isinstance(expected_type, type) and issubclass(expected_type, TypedDict):
            # Recursively handle nested TypedDict
            return parse_dict(value, expected_type)
        elif isinstance(expected_type, list) and len(expected_type) == 1:
            # Handle lists with a single expected item type
            item_type = expected_type[0]
            return [parse_value(item, item_type) for item in value]
        elif isinstance(expected_type, dict):
            # Handle dicts with specified key and value types
            key_type, val_type = list(expected_type.items())[0]
            return {parse_value(k, key_type): parse_value(v, val_type) for k, v in value.items()}
        else:
            # For basic types, just return the value
            return value

    def parse_dict(data: Dict[str, Any], expected_cls: Type[TypedDict]) -> TypedDict:
        result = {}
        for key, expected_type in expected_cls.__annotations__.items():
            if key in data:
                result[key] = parse_value(data[key], expected_type)
        return expected_cls(**result)

    # Load JSON data from the file
    with open(path, 'r') as file:
        json_data = json.load(file)

    # Parse the JSON data and return the constructed TypedDict object
    return parse_dict(json_data, cls)


# Partly generated using GPT-4o
def filter_criteria(model: str, subject: str, subjects_folder: str):
    """Generates a new file in which the filtered criteria are stored as JSON if it does not exist yet."""
    subject_path = os.path.join(subjects_folder, subject)
    criteria_path = os.path.join(subject_path, model + "_criteria.json")
    filtered_criteria_path = os.path.join(subject_path, model + "_criteria_filtered.json")

    if not os.path.isfile(criteria_path):
        raise RuntimeError("Called filter_criteria without criteria existing")

    if not os.path.isfile(filtered_criteria_path):
        with open(criteria_path, "r", encoding='utf-8') as criteria_file:
            # Load the JSON and access the list of criteria
            data = json.load(criteria_file)
            criteria = data.get("criteria", [])

            print(
                f"Please select if the following criteria should be included in the next step for model {model} and subject {subject}`(y/n).")
            filtered_criteria = []

            for criterion in criteria:
                title = criterion.get("title", "No Title")
                explanation = criterion.get("explanation", "No Explanation")

                i = input(f"{title}: {explanation} (y/n): ")
                while i.lower() not in {'y', 'n'}:
                    i = input("Please enter either 'y' or 'n' to select if the criterion should be included: ")
                if i.lower() == 'y':
                    filtered_criteria.append(criterion)
            # Save the filtered criteria into a new JSON file
            with open(filtered_criteria_path, "w", encoding='utf-8') as filtered_criteria_file:
                json.dump({"criteria": filtered_criteria}, filtered_criteria_file, ensure_ascii=False, indent=4)


def analyze_requirement(model: str, subject: str, subjects_folder: str, requirement_name: DirEntry[str]):
    # Read content from file and check if the criteria are fulfilled

    subject_path = os.path.join(subjects_folder, subject)
    filtered_criteria_path = os.path.join(subject_path, model + "_criteria_filtered.json")

    # Create folder for the model analysis if it does not exist yet
    analysis_path = Path(f"{subjects_folder}/{subject}/analysis/{model}")
    analysis_path.mkdir(parents=True, exist_ok=True)

    api: AbstractApi = ApiFactory.get_api(model)

    criteria: Criteria = load_json_as_typed_dict(filtered_criteria_path, Criteria)
    with open(requirement_name.path, "r", encoding='utf-8') as requirement_file:
        requirement = requirement_file.read()

    feedback_collection: FeedbackCollection = api.analyze_requirement(criteria, requirement)

    # Save feedback to data/subjects/{subject}/analysis/{model}/{requirement_name.name}_feedback.json
    write_typed_dict_to_json(feedback_collection, os.path.join(analysis_path, f"{requirement_name.name}_feedback.json"))


def refine_requirement(model: str, subject: str, subjects_folder: str, requirement_name: DirEntry[str]):
    subject_path = os.path.join(subjects_folder, subject)

    # Load feedback
    analysis_path = Path(f"{subjects_folder}/{subject}/analysis/{model}")
    feedback_path = os.path.join(analysis_path, f"{requirement_name.name}_feedback.json")

    feedback_collection: FeedbackCollection = load_json_as_typed_dict(feedback_path, FeedbackCollection)

    with open(requirement_name.path, "r", encoding='utf-8') as requirement_file:
        requirement = requirement_file.read()

    api: AbstractApi = ApiFactory.get_api(model)
    refined_requirement: ImprovedRequirement = api.refine_requirement(feedback_collection, requirement)

    improved_path = os.path.join(analysis_path, f"{requirement_name.name}_improved")
    with open(improved_path, "w", encoding='utf-8') as requirement_file:
        requirement_file.write(str(refined_requirement))


def main():
    # Load environment variables from a .env file
    load_dotenv()

    current_path = os.getcwd()
    subject_folder = os.path.join(current_path, "data/subjects")

    subjects = json.loads(os.getenv('subjects'))
    required_models = json.loads(os.getenv('models'))

    combinations = unique_combinations(subjects, required_models)

    for (subject, model) in combinations:
        # Generate new criteria if they do not exist yet
        generate_criteria(model, subject, subject_folder)

        # Let the user select a list of filtered generated criteria
        filter_criteria(model, subject, subject_folder)

        # Run the filtered criteria against each requirement
        for requirement in os.scandir(os.path.join(subject_folder, subject, "requirements")):
            requirement_analysis_path = os.path.join(subject_folder, subject, "analysis", model, requirement.name,
                                                     "feedback.json")
            # Create analysis if corresponding file does not exist yet.
            if requirement.is_file() and not Path(requirement_analysis_path).is_file():
                analyze_requirement(model, subject, subject_folder, requirement)

                # Provide an improved version of the requirement
                refine_requirement(model, subject, subject_folder, requirement)


if __name__ == '__main__':
    main()
