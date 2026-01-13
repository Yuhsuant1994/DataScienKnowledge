1. Character tokenizer
    * What: split into single characters
	* Problem: very long sequences + weak semantic units → slower/harder training

2. Byte tokenizer
	* What: split into bytes (0–255) (can represent any text)
	* Problem: even longer sequences + very low-level tokens → harder to learn meaning

3. Word tokenizer
	* What: split into words
	* Problem: huge vocab + OOV/<UNK> for unseen words (names, typos, slang)

4. What Byte Pair Encoding (BPE) solved
-> used in GPT-2
	* Removes OOV (<UNK>) by breaking unknown words into subwords
	* Shorter sequences than char/byte tokenizers → faster + easier for models
	* Smaller vocab than word-level → less memory + more scalable
	* Handles new words / names / typos better (can still tokenize them)