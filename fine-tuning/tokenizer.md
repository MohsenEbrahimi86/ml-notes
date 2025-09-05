# 🧠 What is a Tokenizer?

A **tokenizer** is a fundamental component in **Natural Language Processing (NLP)** and **Large Language Models (LLMs)** that **splits raw text into smaller meaningful units called _tokens_**.

---

## 🔍 Simple Definition

> A **tokenizer** converts a string of text (like a sentence) into a list of tokens — which can be words, subwords, characters, or even symbols — that a machine learning model can understand and process.

---

## 🧩 Why Do We Need Tokenizers?

Computers don’t understand human language directly. Models like GPT, BERT, Llama, etc., work with **numbers**, not text.

So we need to:

1. **Break text into pieces** → tokens
2. **Map tokens to numbers** → token IDs
3. Feed those numbers into the model

---

## 🧪 Example

```python
Text: "Hello, world! How are you?"

Tokens (simplified word-level):
["Hello", ",", "world", "!", "How", "are", "you", "?"]

Token IDs (example):
[31287, 11, 1984, 0, 842, 481, 652, 30]
```

---

## 📚 Types of Tokenizers

### 1. ✅ **Word Tokenizer**

- Splits text by spaces/punctuation.
- Simple, but doesn’t handle unknown or rare words well.

```python
"ChatGPT is awesome" → ["ChatGPT", "is", "awesome"]
```

> ❌ Fails with: `"ChatGPTization"` → unknown word!

---

### 2. ✅ **Subword Tokenizer** _(Most Common in Modern LLMs)_

Splits words into frequently used sub-parts. Great for handling unknown words and reducing vocabulary size.

#### Popular Algorithms:

- **Byte Pair Encoding (BPE)** → Used in GPT, Llama
- **WordPiece** → Used in BERT
- **SentencePiece** → Used in T5, Llama 2/3, Mistral

#### Example (BPE-style):

```python
"tokenization" → ["token", "iz", "ation"]
"ChatGPTization" → ["Chat", "G", "PT", "ization"]
```

✅ Handles new/rare words by breaking them into known subwords.

---

### 3. ✅ **Character Tokenizer**

- Each character is a token.
- Very large sequence lengths → inefficient.
- Rarely used in modern LLMs.

```python
"Hi!" → ["H", "i", "!"]
```

---

### 4. ✅ **Byte Tokenizer**

- Tokenizes at the byte level (0–255).
- Used in models like **GPT-4**, **Llama 3** (via tiktoken or SentencePiece).
- Guarantees no “unknown token” — everything can be represented as bytes.

---

## 🔄 Tokenizer Workflow

```
Text → [Tokenization] → Tokens → [Vocabulary Lookup] → Token IDs → [Model Input]
                             ↓
                      (Also: Attention Masks, Position IDs, etc.)
```

And for output:

```
Model Output IDs → [Detokenization] → Human-readable Text
```

---

## 🧑‍💻 Example with Hugging Face `transformers`

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

text = "Hello, how are you doing today?"
tokens = tokenizer.tokenize(text)
ids = tokenizer.encode(text)

print("Tokens:", tokens)
# ➤ ['Hello', ',', 'Ġhow', 'Ġare', 'Ġyou', 'Ġdoing', 'Ġtoday', '?']

print("Token IDs:", ids)
# ➤ [15496, 11, 1105, 389, 345, 1310, 8976, 0]

# Convert back
decoded = tokenizer.decode(ids)
print("Decoded:", decoded)
# ➤ "Hello, how are you doing today?"
```

> 💡 `Ġ` represents a space in GPT-2’s tokenizer (since it uses BPE).

---

## ⚙️ What’s Inside a Tokenizer?

- **Vocabulary**: Mapping of tokens ↔ IDs (e.g., `{"Hello": 15496, ",": 11, ...}`)
- **Tokenizer Algorithm**: BPE, WordPiece, etc.
- **Special Tokens**: `[CLS]`, `[SEP]`, `<|endoftext|>`, `<PAD>`, etc.
- **Preprocessing Rules**: Lowercase? Handle accents? Strip whitespace?

---

## 🚀 Why Tokenizers Matter

- Affects **model performance**, **speed**, and **memory usage**.
- Influences how well the model handles **rare words**, **typos**, **multilingual text**.
- Poor tokenization → garbage in, garbage out.

---

## 🔬 Advanced: Tokenizer Training

You can even **train your own tokenizer** on custom data:

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
tokenizer.pre_tokenizer = Whitespace()

files = ["data/text1.txt", "data/text2.txt"]
tokenizer.train(files, trainer)
```

Used in custom NLP pipelines or domain-specific models.

---

## 📊 Tokenizer Comparison (Popular Models)

| Model         | Tokenizer Type      | Vocab Size     | Notes                              |
| ------------- | ------------------- | -------------- | ---------------------------------- |
| **GPT-2/3**   | BPE                 | 50,257         | `Ġ` = space                        |
| **BERT**      | WordPiece           | 30,522         | ## for subwords                    |
| **Llama 2/3** | SentencePiece (BPE) | 32,000–128,000 | Byte fallback                      |
| **T5**        | SentencePiece       | 32,100         | No space marking                   |
| **GPT-4**     | tiktoken (BPE)      | ~100,000       | Optimized for speed & multilingual |

---

## ✅ Summary

> A **tokenizer** turns **text → tokens → numbers** so models can process language.

- It’s the **first step** in any NLP pipeline.
- Choice of tokenizer affects model behavior and efficiency.
- Modern LLMs mostly use **subword tokenizers** (BPE, WordPiece, SentencePiece).
- You can use, customize, or even train tokenizers for your needs.

---

🧠 **Fun Fact**: The word “tokenizer” itself might be tokenized as `["token", "izer"]` — depending on the model’s vocabulary!

---
