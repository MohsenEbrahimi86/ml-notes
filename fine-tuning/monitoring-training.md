Monitoring training and validation loss in Hugging Face Transformers is essential for understanding model performance and avoiding overfitting. There are several ways to do this, depending on whether you're using the high-level `Trainer` API or writing a custom training loop.

---

## ✅ Method 1: Using `Trainer` (Recommended for most users)

The `Trainer` class automatically logs training and evaluation loss if you configure logging and evaluation properly.

### Step-by-step:

```python
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer
from datasets import load_dataset

# Load model and tokenizer
model_name = "bert-base-uncased"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load and preprocess dataset
dataset = load_dataset("glue", "mrpc")
def tokenize_function(examples):
    return tokenizer(examples["sentence1"], examples["sentence2"], truncation=True, padding="max_length")

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",        # Evaluate every epoch
    save_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    logging_dir="./logs",               # TensorBoard logs
    logging_strategy="steps",
    logging_steps=10,                   # Log every 10 steps
    report_to="tensorboard",            # or "wandb", "mlflow", etc.
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
)

# Define compute_metrics if needed (optional for loss monitoring)
from sklearn.metrics import accuracy_score
import numpy as np

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return {"accuracy": accuracy_score(labels, predictions)}

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,    # Optional: for extra metrics
)

# Start training
trainer.train()
```

### What gets logged automatically:

- `loss`: Training loss at each logging step.
- `eval_loss`: Validation loss at each evaluation (e.g., every epoch).
- Other metrics if `compute_metrics` is provided.

---

## 📊 View Logs

### Option A: TensorBoard

After training, run:

```bash
tensorboard --logdir ./logs
```

Then open `http://localhost:6006` in your browser.

### Option B: Console Output

You’ll see logs like:

```
Step 10 | Loss: 0.693
Step 20 | Loss: 0.541
...
***** Eval results *****
eval_loss = 0.452
eval_accuracy = 0.82
```

---

## ✅ Method 2: Custom Training Loop (Advanced)

If you’re writing your own training loop, you need to manually compute and log losses.

```python
from torch.utils.data import DataLoader
from transformers import AdamW
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

train_loader = DataLoader(tokenized_datasets["train"], batch_size=16, shuffle=True)
val_loader = DataLoader(tokenized_datasets["validation"], batch_size=16)

optimizer = AdamW(model.parameters(), lr=5e-5)

for epoch in range(3):
    # Training
    model.train()
    total_train_loss = 0
    for batch in train_loader:
        batch = {k: v.to(device) for k, v in batch.items() if k in ["input_ids", "attention_mask", "labels"]}
        outputs = model(**batch)
        loss = outputs.loss
        total_train_loss += loss.item()

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    avg_train_loss = total_train_loss / len(train_loader)
    print(f"Epoch {epoch+1} | Train Loss: {avg_train_loss:.4f}")

    # Validation
    model.eval()
    total_val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            batch = {k: v.to(device) for k, v in batch.items() if k in ["input_ids", "attention_mask", "labels"]}
            outputs = model(**batch)
            total_val_loss += outputs.loss.item()

    avg_val_loss = total_val_loss / len(val_loader)
    print(f"Epoch {epoch+1} | Val Loss: {avg_val_loss:.4f}")
```

You can also integrate with **TensorBoard** or **Weights & Biases** manually:

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter(log_dir="./logs")

# Inside epoch loop:
writer.add_scalar("Loss/train", avg_train_loss, epoch)
writer.add_scalar("Loss/val", avg_val_loss, epoch)

# Don't forget to close:
writer.close()
```

---

## ✅ Method 3: Using Callbacks (with `Trainer`)

You can create a custom callback to log or react to loss values:

```python
from transformers import TrainerCallback

class LossLoggingCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None:
            if "loss" in logs:
                print(f"Step {state.global_step}: Training Loss = {logs['loss']:.4f}")
            if "eval_loss" in logs:
                print(f"Step {state.global_step}: Validation Loss = {logs['eval_loss']:.4f}")

trainer.add_callback(LossLoggingCallback())
```

---

## 🧭 Tips

- Use `evaluation_strategy="steps"` and `eval_steps=500` to evaluate more frequently.
- Set `logging_steps=10` to monitor training loss more granularly.
- Use `load_best_model_at_end=True` with `metric_for_best_model="eval_loss"` to automatically load the best checkpoint.
- Integrate with **Weights & Biases** by setting `report_to="wandb"` and installing `wandb`.

---

## 🚀 Bonus: Using Weights & Biases (wandb)

Install wandb:

```bash
pip install wandb
wandb login
```

Then in `TrainingArguments`:

```python
report_to="wandb",
run_name="my-bert-experiment",  # optional
```

All losses and metrics will be tracked live at https://wandb.ai.

---

## ✅ Summary

| Method              | Ease of Use | Flexibility | Logging Tools Supported    |
| ------------------- | ----------- | ----------- | -------------------------- |
| `Trainer`           | ⭐⭐⭐⭐⭐  | ⭐⭐        | TensorBoard, WandB, MLflow |
| Custom Loop         | ⭐⭐        | ⭐⭐⭐⭐⭐  | Manual (TensorBoard, etc.) |
| Callbacks + Trainer | ⭐⭐⭐⭐    | ⭐⭐⭐      | Same as Trainer            |

---

✅ **Recommendation**: Use `Trainer` unless you need full control. It handles logging, evaluation, saving, and device management automatically.
