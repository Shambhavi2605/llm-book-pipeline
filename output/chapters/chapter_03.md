# Chapter 3: Tokenization

**Learning Objective:** By the end of this chapter, readers will understand how to build a tokenizer from scratch and implement Byte Pair Encoding.

---

**Chapter 3: Tokenization**

In this chapter, we will delve into the process of tokenization, which is the first step in preparing input text for training large language models. Tokenization involves breaking down a sentence or document into individual words or tokens, and then converting these tokens into token IDs.

**Introduction**

Tokenization is a crucial step in building large language models from scratch. It allows us to process and analyze large amounts of text data, which is essential for training accurate language models. In this chapter, we will explore the concept of tokenization, its importance, and how to implement it using Python.

**Main Sections**

### Tokenization: Breaking Down Text into Individual Words

Tokenization can be broadly broken down into three steps:

1. **Splitting text into individual words**: This involves breaking down a sentence or document into individual words or tokens.
2. **Converting tokens into token IDs**: Each token is assigned a unique ID, which will be used to represent the token in our model.

In this chapter, we will focus on the first step of tokenization: splitting text into individual words.

### Using Regular Expressions (re) for Tokenization

To split text into individual words, we can use Python's regular expression module (re). The re module provides regular expression matching operations. We can use the `re.split()` function to split a given text based on white spaces or other characters.

For example, let's say we have a text that looks like this: "hello world this is a test". We can use the following code to split this text into individual tokens:
```python
import re

text = "hello world this is a test"
tokens = re.split(r'\s+', text)
print(tokens)  # Output: ['hello', 'world', 'this', 'is', 'a', 'test']
```
In this example, we use the `re.split()` function to split the text based on white spaces (`\s+`). The resulting tokens are stored in a list called `tokens`.

### Tokenization Example

Let's apply tokenization to our example text:
```python
import re

text = "The Verdict by Edith Warton"
tokens = re.split(r'\s+', text)
print(tokens)  # Output: ['The', 'Verdict', 'by', 'Edith', 'Warton']
```
In this example, we split the text into individual tokens using the `re.split()` function. The resulting tokens are stored in a list called `tokens`.

**Key Takeaways**

* Tokenization is the process of breaking down a sentence or document into individual words or tokens.
* We can use Python's regular expression module (re) to implement tokenization.
* Tokenization involves two main steps: splitting text into individual words and converting tokens into token IDs.

By the end of this chapter, you should have a good understanding of how to tokenize text using Python. In the next chapter, we will explore the second step of tokenization: converting tokens into token IDs.