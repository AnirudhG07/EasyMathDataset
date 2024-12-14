# Easy Math Dataset

This repository contains easy set of problems from different field, with their proofs.

## How to get the problem in the dataset

I have made a simple cli(called `emad`) to auto extract the problem from the dataset and print it in the terminal. So you dont need to hunt for it inside the json file.

### How to use it?

You can run the below script in the terminal (I assume you have python)

```bash
git clone https://github.com/AnirudhG07/EasyMathDataset.git
cd EasyMathDataset
pip install .
```

This will install the cli in your system. Now you can run the below command to get the problem.

```bash
# For extracting the problem and proof.
eamd ex --[t]opic <topic> --[i]d <id>
# Example
emad ex -t "Linear Algebra" -i 1

# For summarisinf the dataset content.
emad summary
```

Please use the same name present in the summary in the `ex` command.
