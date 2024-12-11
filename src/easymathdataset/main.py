import json
import os

from easymathdataset.proof_problems_gpt import data_gen
from easymathdataset.proof_response_gpt import output_gen_parse

MATH_TOPICS = [
    "Linear Algebra",
    "Geometry",
    "Algebra",
    "Calculus",
    "Number Theory",
    "Statistics",
    "Trigonometry",
    "Probability",
    "Combinatorics",
    "Logic",
    "Set Theory",
    "Graph Theory",
    "Topology",
    "Real Analysis",
    "Differential Equations",
    "Abstract Algebra",
    "Group Theory",
    "Number Theory",
    "Complex Analysis",
    "Vector Calculus",
    "Basic Group Properties",
    "Subgroups and Cosets",
    "Group Homomorphisms",
]

NO_OF_PROBLEMS = 10

class MathDatasetGenerator:
    def __init__(self, topics, num_problems, output_file):
        """
        Initialize the dataset generator.
        :param topics: List of math topics to generate problems for.
        :param num_problems: Number of problems to generate per topic.
        :param output_file: File path to save the dataset.
        """
        self.topics = topics
        self.num_problems = num_problems
        self.output_file = output_file
        self.dataset = self._load_existing_data()

    def _load_existing_data(self):
        """Load existing data from the output file if it exists."""
        if os.path.exists(self.output_file):
            with open(self.output_file, "r") as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):  # Ensure data is a list
                        return data
                except json.JSONDecodeError:
                    pass  # If JSON is invalid, fall back to returning an empty list
        return []

    def _save_data(self):
        """Save the dataset to the output file."""
        with open(self.output_file, "w") as file:
            json.dump(self.dataset, file, indent=4)

    def _generate_problem_id(self):
        """Generate a unique ID for a new problem."""
        return str(len(self.dataset) + 1)

    def generate_problems(self):
        """Generate problems for all topics and add them to the dataset."""
        existing_problems = {(item["topic"], item["problem"]) for item in self.dataset}

        for topic in self.topics:
            problems = data_gen(topic, self.num_problems)
            for problem in problems:
                problem = problem.strip()
                if not problem:
                    continue

                # Avoid duplicates
                if (topic, problem) in existing_problems:
                    continue

                # Add new problem to the dataset
                problem_entry = {
                    "id": self._generate_problem_id(),
                    "topic": topic,
                    "problem": problem,
                    "proof": output_gen_parse(topic, problem),
                }
                self.dataset.append(problem_entry)
                self._save_data()  # Save after adding each problem

    def save_dataset(self):
        """Public method to save the dataset."""
        self._save_data()

    def display_summary(self):
        """Display a summary of the dataset."""
        print(f"Dataset contains {len(self.dataset)} problems.")
        topics_summary = {topic: 0 for topic in self.topics}
        for item in self.dataset:
            if item["topic"] in topics_summary:
                topics_summary[item["topic"]] += 1

        for topic, count in topics_summary.items():
            print(f"  - {topic}: {count} problems")
def main():
    # Configuration
    base_dir = os.path.dirname(__file__)
    OUTPUT_FILE = os.path.join(base_dir, "..", "..", "EasyMathDataset.json")

    # Initialize and run the generator
    generator = MathDatasetGenerator(MATH_TOPICS[:2], NO_OF_PROBLEMS, OUTPUT_FILE)
    generator.generate_problems()
    generator.save_dataset()
    generator.display_summary()
