import json
import os

import click

__package__ = "emad"
__version__ = "0.1.0"

current_dir = os.path.dirname(os.path.realpath(__file__))
DATASET_PATH = os.path.join(current_dir, "EasyMathDataset.json")

def _latex_formatter(text: str) -> str:
    """
    The output code may contain `\\` instead of single backslash for latex syntaxes making it
    difficult to use in latex documents. This function replaces `\\` with single backslash.
    """
    return text.replace("\\\\", "\\")

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version=__version__)
def main():
    """
    Easy Math Dataset CLI - emad
    """
    pass

@main.command(short_help="Extract a problem and proof from the dataset")
@click.option("--topic", "-t", help="Topic of the dataset", required=True)
@click.option("--id", "-i", help="Output file name", required=True)
def ex(topic, id):
    """
    Get the problem and proof based on the topic and id
    """
    with open(DATASET_PATH, "r") as f:
        data = f.read()
        dataset = json.loads(data)

    if topic in dataset:
        problems = dataset[topic]
        for problem in problems:
            if problem["id"] == id:
                prob = _latex_formatter(problem["statement"])
                proof = _latex_formatter(problem["proof"])
                click.echo(f"Problem:\n{prob}")
                click.echo("\n--------------------------------\n")
                click.echo(f"Proof:\n{proof}")
                return
        click.echo(f"No problem found with id {id} in topic {topic}")
    else:
        click.echo(f"No topic found with name {topic}")

@main.command(short_help="List out summary about the dataset")
def summary():
    """
    List out the summary of the dataset. 
    This will print out the topic and the number of problems in each topic.
    """
    with open(DATASET_PATH, "r") as f:
        data = f.read()
        dataset = json.loads(data)
    
    for topic, problems in dataset.items():
        click.echo(f"{topic}: {len(problems)} problems")

