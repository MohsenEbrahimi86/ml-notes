from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import evaluate
import torch


def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=-1)
    return metric.compute(predictions=predictions, references=labels)


if __name__ == "__main__":
    dataset = load_dataset("imdb")
    print(dataset["train"][0])
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Apply tokenization
    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=2)

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

    metric = evaluate.load("accuracy")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"].select(
            range(1000)),  # Use small subset for demo
        eval_dataset=tokenized_datasets["test"].select(range(500)),
        compute_metrics=compute_metrics,
    )

    # Training
    trainer.train()

    results = trainer.evaluate()
    print(results)

    # Save the Fine-Tuned Model
    trainer.save_model("./fine_tuned_bert_imdb")
    tokenizer.save_pretrained("./fine_tuned_bert_imdb")
