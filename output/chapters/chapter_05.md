# Chapter 5: Embeddings

**Learning Objective:** By the end of this chapter, readers will understand token embeddings and positional embeddings and why they are essential.

---

**Chapter 5: Embeddings**

**Introduction**

In the previous chapters, we have covered the basics of building large language models from scratch. In this chapter, we will delve into the concept of token embeddings and positional embeddings, which are essential components in building these models.

**What are Token Embeddings?**

Token embeddings, also known as vector embeddings or word embeddings, are a way to represent words as vectors that capture their semantic meaning. This is crucial because computers cannot understand words directly; they need numerical representations to process language inputs. In this chapter, we will explore why token embeddings are necessary and how they can be created.

**Why Do We Need Token Embeddings?**

As the lecturer explained, assigning random numbers or one-hot encoding to each word does not capture the semantic relationship between words. For example, cat and kitten are related words, but their assigned numbers do not reflect this relationship. Similarly, dog and puppy are related, but their assigned numbers do not capture this similarity.

Token embeddings solve this problem by representing words as vectors that capture their semantic meaning. This allows us to group similar words together and see which words are farther apart from each other.

**How Are Token Embeddings Created?**

The lecturer showed a simple example of how token embeddings can be constructed using features such as "has a tail," "is eatable," "has four legs," "makes sound," and "is a pet." By assigning high values to the features that are true for a particular word, we can create vectors that capture its semantic meaning.

For instance, the vector representation of dog would have high values for "has a tail," "has four legs," "makes sound," and "is a pet." Similarly, the vector representation of cat would also have high values for these features. This allows us to see that dog and cat are similar words because they share many common features.

**Training Neural Networks for Token Embeddings**

The lecturer explained that creating token embeddings is not easy because it requires training a neural network to construct vectors that capture semantic meaning. The training data comes from text, where we know which words are closer to each other based on their context and relationships.

In the next part of this lecture, we will explore how to train a neural network to create vector embeddings for large language models like GPT.

**Key Takeaways**

1. Token embeddings represent words as vectors that capture their semantic meaning.
2. Assigning random numbers or one-hot encoding does not capture the semantic relationship between words.
3. Vector embeddings can group similar words together and show which words are farther apart from each other.
4. Creating token embeddings requires training a neural network to construct vectors that capture semantic meaning.

In the next chapter, we will explore how to train a neural network to create vector embeddings for large language models like GPT.