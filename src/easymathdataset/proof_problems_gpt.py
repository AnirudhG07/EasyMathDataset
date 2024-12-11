import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key  = OPENAI_API_KEY,
)

def generate_problems_gpt(topic: str, quant:int = 10, model:str = "gpt-4o"):
    """
    Generate Trivial Proof Problems using gpt, given a topic.
    :param topic: str: The topic of the problem.
    :param quant: int: The number of problems to generate.
    :param model: str: The model to use for generating the response.
    """


    response = client.chat.completions.create(
            model=model,
            messages= [
                { "role": "system", "content": [
                    {
                        "type": "text",
                        "text": "You are an expert mathematician. Your task is to create trivial, easy and obvious mathematical statements based on given topics. From the given topic, give a variety of statements covering different aspects of the topic. Do not write the proof, just the problem statement. Enclose each problem statement in <p> and </p> tags."
                    }
                ]
                },
                {
                    "role": "user", "content": [
                        {
                            "type": "text",
                            "text": "Create 5 problems on Number Theory."
                        }
                    ]
                },
                {
                    "role": "assistant", "content": [
                        {
                            "type": "text",
                            "text": "<p>The product of two consecutive natural numbers is even.</p><p>The sum of two odd numbers is even.</p><p>A prime number has exactly two distinct positive divisors: 1 and itself.</p><p>Every natural number is either odd or even.</p><p>A number is divisible by 10 if and only if its last digit is 0.</p>"
                        }
                    ]
                },
                {
                    "role": "user", "content": [
                        {
                            "type": "text",
                            "text": f"Create {quant} problems on {topic}"
                        }
                    ]
                },
        ]
    )

    if response.choices[0].message.content is None:
        return f"No response from {model}"

    return response.choices[0].message.content

def data_gen(topic: str, quant: int = 10, model: str = "gpt-4o"):
    """
    Create the JSON data for the problems.
    :param topic: str: The topic of the problem.
    :param quant: int: The number of problems to generate.
    :param model: str: The model to use for generating the response.
    """
    gpt_problems = generate_problems_gpt(topic, quant, model).split("<p>")
    problems = []

    for problem in gpt_problems:
        clean_problem = problem.replace("</p>", "").strip()
        if clean_problem:
            problems.append(clean_problem)

    return problems


if __name__ == "__main__":
    print(data_gen("Number Theory", 10))

