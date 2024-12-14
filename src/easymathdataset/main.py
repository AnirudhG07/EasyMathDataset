import json
import logging
import os
from typing import Dict, List, Optional

from easymathdataset.proof_problems_gpt import data_gen
from easymathdataset.proof_response_gpt import output_gen_parse

MATH_TOPICS = [
    "Linear Algebra",
    "Algebra",
    "Geometry",
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
]

NO_OF_PROBLEMS = 15


class MathProofDatasetManager:
    def __init__(self, dataset_path: str = 'EasyMathDataset.json'):
        """
        Initialize the dataset manager with a specified JSON file path.
        
        :param dataset_path: Path to the JSON file storing the math proof dataset
        """
        self.dataset_path = dataset_path
        self.dataset = self._load_dataset()
    
    def _load_dataset(self) -> Dict[str, List[Dict]]:
        """
        Load existing dataset from JSON file or create a new one if not exists.
        
        :return: Dictionary of topics and their proof problems
        """
        if os.path.exists(self.dataset_path):
            with open(self.dataset_path, 'r') as f:
                return json.load(f)
        return {}

    def _latex_formatter(self, text: str) -> str:
        """
        The output code may contain `\\` instead of single backslash for latex syntaxes making it
        difficult to use in latex documents. This function replaces `\\` with single backslash.
        """
        return text.replace("\\\\", "\\")
    
    def generate_proofs(self, topic: str, num_problems: int = 10, model: str = "gpt-4o") -> List[Dict]:
        """
        Generate proof problems for a specific topic using data_gen function.
        
        :param topic: Mathematical topic to generate proofs for
        :param num_problems: Number of problems to generate
        :param model: Model to use for generation
        :return: List of generated proof problems
        """
        try:
            problems = data_gen(topic, quant=num_problems, model=model)
            # Determine the starting ID based on existing problems
            existing_problems = self.dataset.get(topic, [])
            if existing_problems:
                last_id = max(int(problem["id"]) for problem in existing_problems)
            else:
                last_id = 0

            new_problems = []
            
            for i, problem in enumerate(problems, 1):
                proof = output_gen_parse(topic, problem)
                problem_unit = {
                    "id": f"{last_id + i}",
                    "statement": self._latex_formatter(problem),
                    "proof": self._latex_formatter(proof)
                }
                # Save the new problem individually
                new_problems.append(problem_unit)
                print(f"Generated and saved proof {last_id + i} for {topic}")
            
            return new_problems
        except Exception as e:
            logging.error(f"Error generating proofs for {topic}: {e}")
            return []
    
    def add_topic_proofs(self, topic: str, num_problems: int = 10, model: str = "gpt-4o"):
        """
        Add generated proof problems to a specific topic in the dataset.
        
        :param topic: Mathematical topic to add proofs for
        :param num_problems: Number of problems to generate
        :param model: Model to use for generation
        """
        # Ensure topic exists in dataset
        if topic not in self.dataset:
            self.dataset[topic] = []
        
        # Generate new problems
        new_problems = self.generate_proofs(topic, num_problems, model)
        
        # Extend existing problems for the topic
        self.dataset[topic].extend(new_problems)
        
        # Save updated dataset
        self._save_dataset()
    
    def add_proof_manually(self, topic: str, statement: str, proof: str, custom_id: Optional[str] = None):
        """
        Manually add a proof problem to a specific topic.
        
        :param topic: Mathematical topic
        :param statement: Problem statement
        :param proof: Proof for the problem
        :param custom_id: Optional custom ID, otherwise auto-generated
        """
        if topic not in self.dataset:
            self.dataset[topic] = []
        
        # Generate ID if not provided
        if custom_id is None:
            custom_id = f"{len(self.dataset[topic]) + 1}"
        
        new_proof = {
            "id": custom_id,
            "statement": self._latex_formatter(statement),
            "proof": self._latex_formatter(proof)
        }
        
        self.dataset[topic].append(new_proof)
        self._save_dataset()
    
    def _save_dataset(self):
        """
        Save the current dataset to the JSON file.
        """
        with open(self.dataset_path, 'w') as f:
            json.dump(self.dataset, f, indent=2)
    
    def get_topic_proofs(self, topic: str) -> List[Dict]:
        """
        Retrieve proof problems for a specific topic.
        
        :param topic: Mathematical topic
        :return: List of proof problems for the topic
        """
        return self.dataset.get(topic, [])
    
    def summary_dataset(self) -> List[str]:
        """
        List all topics in the dataset.
        
        :return: List of topics
        """
        return list(self.dataset.keys())
# Example usage
def main():
    # Initialize the dataset manager
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "..", "..", 'EasyMathDataset.json')
    dataset_manager = MathProofDatasetManager(dataset_path = dataset_path)
    
    # Generate proofs for multiple topics
    for topic in MATH_TOPICS:  # Limiting to first 5 topics for demonstration
        dataset_manager.add_topic_proofs(topic, num_problems=NO_OF_PROBLEMS)
    
    # List available topics
    print("Available Topics:", dataset_manager.summary_dataset())

if __name__ == "__main__":
    main()
