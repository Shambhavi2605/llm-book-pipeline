# Chapter 4: Data Preparation and Input Pipeline

**Learning Objective:** By the end of this chapter, readers will understand how to create input-target pairs and build efficient data pipelines.

---

**Chapter 4: Data Preparation and Input Pipeline**

In this chapter, we will delve into the process of creating input-target pairs, a crucial step in preparing our data for training large language models. We will explore how to create these pairs using a specific technique that is essential for large language models.

**Introduction**

Before we dive into the details, let's take a step back and understand what we are trying to achieve. In the previous chapter, we discussed tokenization, which is the process of breaking down text into smaller units called tokens. Now, we need to create input-target pairs that will serve as the foundation for our large language model training.

**Main Section: Creating Input-Target Pairs**

To create input-target pairs, we will use a technique called auto-regressive modeling. This means that in each iteration, the output of the previous iteration becomes the input for the next iteration. Let's illustrate this with an example:

Suppose we have a sentence "LLMs learn to predict one word at a time." We can break down this sentence into input-target pairs as follows:

* Input: LLMs
* Target: learn

In the first iteration, the input is "LLMs" and the target is "learn". In the second iteration, the input becomes "learn" (which was the output of the previous iteration), and the target is "to".

This process continues until we reach the end of the sentence. By creating these input-target pairs, we are essentially mimicking how humans learn language - by predicting the next word based on the context.

**Key Takeaways**

1. **Auto-regressive modeling**: In each iteration, the output of the previous iteration becomes the input for the next iteration.
2. **Input-Target Pairs**: We create these pairs by breaking down text into smaller units called tokens and using them as inputs and targets for our model.
3. **Context Size**: The context size determines how many words we want to give as input for the model to make its prediction.

**Coding Section: Creating Input-Target Pairs**

In this section, we will implement a data loader that fetches the input-target pairs using a sliding window approach. We will use the bite pair encoding tokenizer to encode our text and then create the input-target pairs.

Here is the code:
```python
import pandas as pd

# Load the encoded text
encoded_text = pd.read_csv('encoded_text.csv')

# Define the context size (number of words to give as input)
context_size = 4

# Create the input-target pairs
input_target_pairs = []
for i in range(len(encoded_text) - context_size):
    input_tokens = encoded_text[i:i+context_size]
    target_token = encoded_text[i+context_size]
    input_target_pairs.append((input_tokens, target_token))

# Print the first few input-target pairs
print(input_target_pairs[:5])
```
In this code, we load the encoded text and define the context size. We then create the input-target pairs by iterating over the encoded text and extracting the input tokens (context_size words) and the target token (the next word). Finally, we print the first few input-target pairs to see how they look.

**Conclusion**

In this chapter, we learned how to create input-target pairs using auto-regressive modeling. We implemented a data loader that fetches these pairs using a sliding window approach and used the bite pair encoding tokenizer to encode our text. By creating these input-target pairs, we are preparing our data for training large language models. In the next chapter, we will explore how to create vector embeddings from our input-target pairs.