import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key  = OPENAI_API_KEY,
)

def gpt_response_gen(problem:str, topic:str = "", model:str ="gpt-4o") -> str:
    """
    Generate the response from models like gpt-4o.
    :param problem: str: The problem statement.
    :param topic: str: The topic of the problem.
    :param model: str: The model to use for generating the response.
    """

    response = client.chat.completions.create(
            model=model,
            messages= [
                { "role": "system", "content": [
                    {
                        "type": "text",
                        "text": "You are an expert mathematician. You are asked to provide mathematically correct proof of a mathematical statement given to you from given topic. Write the proof in Latex and use `$` to enclose LaTeX formulas."
                    }
                    ]
                },
            {
                "role": "user", "content": [
                    {
                        "type": "text",
                        "text": "Number Theory: Product of consecutive natural numbers is even."
                    }
                ]
            },
            {
                "role": "assistant", "content": [
                    {
                        "type": "text",
                        "text": "Let the two consecutive natural numbers be $n$ and $n+1$. Since natural numbers alternate between odd and even, either $n$ or $n+1$ must be even. If $n$ is even, then $n = 2k$ for some integer $k$, and their product is $n(n+1) = 2k(n+1)$, which is even. If $n$ is odd, then $n+1 = 2k$ for some integer $k$, and their product is $n(n+1) = n \cdot 2k = 2(n \cdot k)$, which is also even. Thus, in all cases, the product of two consecutive natural numbers is even."
}
                ]
            },
            {
                "role": "user", "content": [
                    {
                        "type": "text",
                        "text": f"{topic}: {problem}"
                    }
                ]
            }
        ],
        temperature=0
    )

    if response.choices[0].message.content is None:
        return f"No response from {model}"

    return response.choices[0].message.content

def output_gen_parse(topic:str, problem:str):
    """
    Generate the outputs from model and parse them into a dictionary.
    :param topic: str: The topic of the problem.
    :param problem: str: The problem statement.
    """
    # Dummy function for future requirements for parsing, etc.
    gpt_proof = gpt_response_gen(problem, topic)
    return gpt_proof

if __name__ == "__main__":
    problem = "Product of 3 consecutive natural numbers is divisible by 6."
    topic = "Number Theory"
    gpt_proof = gpt_response_gen(problem, topic)
    print(output_gen_parse(topic, gpt_proof))

