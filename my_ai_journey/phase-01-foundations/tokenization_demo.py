import tiktoken

# Load the tokenizer used by GPT-4o / GPT-3.5
enc = tiktoken.encoding_for_model("gpt-4o")

texts = [
    "hello",
    "Hello, world!",
    "tokenization",
    "سلام دنیا",  # Persian text
    "The quick brown fox jumps over the lazy dog",
]

for text in texts:
    tokens = enc.encode(text)
    print(f"Text: {text!r}")
    print(f"  Token count: {len(tokens)}")
    print(f"  Token IDs: {tokens}")
    print(f"  Decoded back: {enc.decode(tokens)!r}")
    print()
