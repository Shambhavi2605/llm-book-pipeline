# Chapter 10: Inference and Sampling

**Learning Objective:** By the end of this chapter, readers will understand temperature scaling and top-k sampling for controlling text generation.

---

**Chapter 10: Inference and Sampling**

In this chapter, we will explore techniques to control the randomness in text generation. Specifically, we will learn about temperature scaling, a method that helps reduce the randomness in generated text by sampling from a probability distribution.

**Introduction**

In the previous lecture, we trained a large language model completely from scratch. We saw how the model predicted the next tokens based on the input sentence and the vocabulary size. However, this process led to a lot of randomness and diversity in the generated text. In this chapter, we will learn techniques to control this randomness and make the generated text more coherent.

**Temperature Scaling**

The main idea behind temperature scaling is to replace the maximum probability with a probability distribution. Instead of choosing the token ID with the highest probability, we sample from a multinomial probability distribution. This allows us to introduce some randomness in the selection process while still maintaining the most likely token as the default choice.

To illustrate this concept, let's revisit the `generate_text` function and replace the `argmax` operation with a multinomial function. We will apply this function to the probabilities tensor and sample from it to get the next token ID. This is where temperature scaling comes in – we can control the distribution of probabilities by dividing the logits tensor by a number greater than zero, which is called the temperature value.

**Key Takeaways**

* Temperature scaling is a technique that helps reduce randomness in text generation by sampling from a probability distribution.
* The multinomial function samples the next token proportional to its probability score, allowing for some randomness in the selection process.
* By introducing temperature scaling, we can control the distribution of probabilities and make the generated text more coherent.

**Conclusion**

In this chapter, we learned about temperature scaling, a technique that helps reduce randomness in text generation. We saw how replacing the `argmax` operation with a multinomial function allows for some randomness in the selection process while still maintaining the most likely token as the default choice. By controlling the distribution of probabilities through temperature scaling, we can make the generated text more coherent and creative. In the next chapter, we will explore another technique called top-k sampling to further control the randomness in text generation.