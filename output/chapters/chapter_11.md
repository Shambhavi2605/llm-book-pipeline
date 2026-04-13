# Chapter 11: Model Saving and Loading

**Learning Objective:** By the end of this chapter, readers will understand how to save and load model weights and use pretrained OpenAI GPT-2 weights.

---

**Chapter 11: Model Saving and Loading**

In this chapter, we will explore how to save and load model weights in PyTorch. This is an essential skill for any machine learning engineer, especially when dealing with large language models like the ones we have been building throughout this series.

**Introduction**

Before we dive into the details of saving and loading model weights, let's quickly recap what we have done so far in this series on pre-training large language models. We initially looked at evaluating the loss function for an LL (Large Language) model, saw how cross-entropy loss comes into play, and ran a pre-training loop to generate new text from input text. However, we encountered issues with overfitting, which led us to explore text generation strategies like temperature scaling and top-K sampling.

**Saving Model Weights**

To save the parameters of our GPT model, we use the `torch.save` command. This command takes two arguments: the first is the model state dictionary, and the second is the file name where we want to store the model parameters. The model state dictionary is a dictionary mapping each layer to its parameters, which is available by default for any PyTorch model.

Here's an example of how we can save our GPT model:
```python
model = GPTModel()  # assume this is our GPT model class
torch.save(model.state_dict(), 'model.pth')
```
**Loading Model Weights**

To load the saved model weights, we use the `torch.load` command. This command takes a file name as an argument and returns the loaded model state dictionary.

Here's an example of how we can load our GPT model:
```python
checkpoint = torch.load('model.pth')
model = GPTModel()
model.load_state_dict(checkpoint)
```
**Saving Optimizer State**

In addition to saving the model weights, it's also important to save the optimizer state. This is because optimizers like Adam maintain a history of gradients and squared gradients, which are needed for the optimization process.

Here's an example of how we can save the optimizer state:
```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
torch.save(optimizer.state_dict(), 'optimizer.pth')
```
**Loading Optimizer State**

To load the saved optimizer state, we use the `torch.load` command again.

Here's an example of how we can load our GPT model and its optimizer:
```python
checkpoint = torch.load('model.pth')
model = GPTModel()
model.load_state_dict(checkpoint)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
optimizer.load_state_dict(torch.load('optimizer.pth'))
```
**Key Takeaways**

In this chapter, we learned how to save and load model weights in PyTorch using the `torch.save` and `torch.load` commands. We also explored how to save and load optimizer state, which is essential for maintaining the optimization process.

By mastering these skills, you will be able to efficiently train and test your large language models, making it easier to achieve coherent text generation results. In the next chapter, we will explore how to load pre-trained weights from OpenAI's GPT-2 model and integrate them with our own GPT architecture.