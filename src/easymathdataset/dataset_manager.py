import json
import logging
import os
from typing import Dict, List

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
                    "statement": problem,
                    "proof": proof,
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
    
    def add_proof_manually(self, topic: str, statement: str, check_proof: bool = False):
        """
        Manually add a proof problem to a specific topic generated by LLM. The id is generated automatically.
        
        :param topic: Mathematical topic
        :param statement: Problem statement
        """
        if topic not in self.dataset:
            self.dataset[topic] = []
        
        # Generate ID if not provided
        custom_id = None
        if custom_id is None:
            custom_id = f"{len(self.dataset[topic]) + 1}"
        
        new_proof = {
            "id": custom_id,
            "statement": statement,
            "proof": output_gen_parse(topic, statement),
        }
        
        if check_proof:
            print("Statement:\n", statement)
            print("\n--------------------------------\n")
            print("Proof:\n", new_proof["proof"])

            if input("Do you want to add this proof to the dataset? (y/n): ").lower() != "y":
                return
            else:
                self.dataset[topic].append(new_proof)
                self._save_dataset()
                print(f"Proof added to {topic} with ID {custom_id}")
        else:
            try:
                self.dataset[topic].append(new_proof)
                self._save_dataset()
                print(f"Proof added to {topic} with ID {custom_id}")
            except Exception as e:
                logging.error(f"Error adding proof to {topic}: {e}")

    def remove_proof(self, topic: str, proof_ids: List[int]):
        """
        Remove a proof problem from a specific topic in the dataset and adjust the IDs of the remaining proofs.
        
        :param topic: Mathematical topic
        :param proof_ids: List of IDs of the proof problems to remove
        """
        if topic not in self.dataset:
            print(f"No proofs found for topic {topic}")
            return
        
        # Filter out the proof problems to remove
        try:
            self.dataset[topic] = [proof for proof in self.dataset[topic] if int(proof["id"]) not in proof_ids]
            
            # Adjust the IDs of the remaining proofs
            for i, proof in enumerate(self.dataset[topic], 1):
                proof["id"] = str(i)
            
            self._save_dataset()
            print(f"Proofs removed from {topic}: {proof_ids}")

        except Exception as e:
            logging.error(f"Error removing proofs from {topic}: {e}")

    
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
        List all topics in the dataset, along with the number of proof problems for each topic.
        
        :return: List of topics
        """
        return [f"{topic}: {len(self.dataset[topic])} proofs" for topic in self.dataset]

# Example usage
def main():
    # Initialize the dataset manager
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "..", "..", 'EasyMathDataset.json')
    dataset_manager = MathProofDatasetManager(dataset_path = dataset_path)
    
    # Generate proofs for multiple topics
    #for topic in MATH_TOPICS:  # Limiting to first 5 topics for demonstration
    #    dataset_manager.add_topic_proofs(topic, num_problems=NO_OF_PROBLEMS)

    # Add a proof manually
    ps = [
        "If A is subset of B, and B is subset of C, then A is subset of C.",
    ]
    for p in ps:
        dataset_manager.add_proof_manually("Set Theory", p, check_proof=True)

    # Remove a proof
    #dataset_manager.remove_proof("Set Theory", [10])

    # Summary of the dataset
    print("\n".join(dataset_manager.summary_dataset()))


if __name__ == "__main__":
    main()
