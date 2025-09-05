from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="./fine_tuned_bert_imdb",
    tokenizer="./fine_tuned_bert_imdb"
)

result = classifier("I love this movie! It was amazing.")
print(result)  # {'label': 'POSITIVE', 'score': 0.999}
