Here's a **step-by-step guide** to fine-tuning a pre-trained model using **PyTorch** and **Hugging Face Transformers** (a popular library built on top of PyTorch). We'll fine-tune a pre-trained **BERT** model for a **text classification task** (e.g., sentiment analysis) using the **IMDB movie reviews dataset**.

---

### ✅ Prerequisites

Install required packages:

```bash
pip install torch transformers datasets evaluate
```

---

## 🔁 Step-by-Step Guide to Fine-Tune a Model in PyTorch

---

### ✅ Step 1: Import Libraries

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import evaluate
import torch
```

---

### ✅ Step 2: Load Dataset

We’ll use the IMDB dataset (binary sentiment classification).

```python
dataset = load_dataset("imdb")
print(dataset["train"][0])
```

Output:

```python
{'text': 'I really loved this movie!', 'label': 1}
```

---

### ✅ Step 3: Load Tokenizer and Preprocess Data

Choose a pre-trained model and its tokenizer (e.g., `bert-base-uncased`).

```python
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

# Apply tokenization
tokenized_datasets = dataset.map(tokenize_function, batched=True)
```

> ⚠️ Note: `max_length=512` is BERT’s max input size.

---

### ✅ Step 4: Load Pre-trained Model

Load a BERT model for sequence classification with 2 labels (positive/negative).

```python
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
```

---

### ✅ Step 5: Define Training Arguments

Set hyperparameters like learning rate, batch size, epochs, etc.

```python
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    report_to="none",  # Set to "wandb" if using Weights & Biases
)
```

---

### ✅ Step 6: Define Evaluation Metric

Use `evaluate` to compute accuracy.

```python
metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=-1)
    return metric.compute(predictions=predictions, references=labels)
```

---

### ✅ Step 7: Initialize Trainer

The `Trainer` class handles training and evaluation.

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"].select(range(1000)),  # Use small subset for demo
    eval_dataset=tokenized_datasets["test"].select(range(500)),
    compute_metrics=compute_metrics,
)
```

> 💡 Tip: Use `.select(range(N))` to speed up testing. Remove in full training.

---

### ✅ Step 8: Train the Model

```python
trainer.train()
```

This will:

- Load batches
- Compute loss
- Backpropagate
- Update weights
- Evaluate at the end of each epoch

---

### ✅ Step 9: Evaluate the Model

```python
results = trainer.evaluate()
print(results)
```

Output:

```python
{'eval_loss': 0.45, 'eval_accuracy': 0.87, ...}
```

---

### ✅ Step 10: Save the Fine-Tuned Model

```python
trainer.save_model("./fine_tuned_bert_imdb")
tokenizer.save_pretrained("./fine_tuned_bert_imdb")
```

---

### ✅ Step 11: Use the Model for Inference

```python
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="./fine_tuned_bert_imdb",
    tokenizer="./fine_tuned_bert_imdb"
)

result = classifier("I love this movie! It was amazing.")
print(result)  # {'label': 'POSITIVE', 'score': 0.999}
```

---

## 🧠 Key Concepts Explained

| Step                | Purpose                                      |
| ------------------- | -------------------------------------------- |
| Tokenization        | Convert text to model-readable input IDs     |
| `Trainer`           | Handles training loop, optimization, logging |
| `TrainingArguments` | Hyperparameters and training settings        |
| `compute_metrics`   | Custom evaluation (accuracy, F1, etc.)       |
| Fine-tuning         | Update pre-trained weights on your task      |

---

## 🛠 Tips for Better Results

- Use **learning rate scheduling** (e.g., linear warmup).
- Try **different models**: `distilbert-base-uncased`, `roberta-base`.
- Use **larger datasets** for full training.
- Enable **GPU** (ensure `torch.cuda.is_available()`).
- Monitor **overfitting** with validation loss.

---

## ✅ Bonus: Use GPU (if available)

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
```

The `Trainer` automatically uses GPU if available.

---

## 📚 Resources

- Hugging Face Docs: [https://huggingface.co/docs](https://huggingface.co/docs)
- PyTorch Tutorials: [https://pytorch.org/tutorials](https://pytorch.org/tutorials)

---
