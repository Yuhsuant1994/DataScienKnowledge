# Course: Stanford CS336 Language Modeling from Scratch | Spring 2025

[course link](https://stanford-cs336.github.io/spring2025/)
, [youtube link](https://www.youtube.com/watch?v=SQ3fZ1sAqXI&list=PLoROMvodv4rOY23Y0BoGoBGgQ1zmU_MT_&index=2)

## Assignment 1: [github link](https://github.com/stanford-cs336/assignment1-basics/tree/main), [pdf](https://github.com/stanford-cs336/assignment1-basics/blob/main/cs336_spring2025_assignment1_basics.pdf)
1. implement BPE tokenizer
2. implement Transformer, cross-entropy loss, AdamW optimizer, training loop
3. Train on TinyStories and OpenWebText

## Assignment 2 [github link](https://github.com/stanford-cs336/assignment2-systems/tree/main)
    
1. Implement a fused RMSNorm kernel in Triton 
2. Implement distributed data parallel training    
3. Implement optimizer state sharding 
4. Benchmark and profile the implementations

## Assignment 3 [github link](https://github.com/stanford-cs336/assignment3-scaling/tree/main)
    
1. We define a training API (hyperparameters -> loss) based on previous runs  
2. Submit "training jobs" (under a FLOPs budget) and gather data points  
3. Fit a scaling law to the data points 
4. Submit predictions for scaled up hyperparameters
5. Leaderboard: minimize loss given FLOPs budget

## Assignment 4 [GitHub](https://github.com/stanford-cs336/assignment4-data/tree/main)
    
1. Convert Common Crawl HTML to text
2. Train classifiers to filter for quality and harmful content
3. Deduplication using MinHash
4. Leaderboard: minimize perplexity given token budget

## Assignment 5[GitHub](https://github.com/stanford-cs336/assignment5-alignment)
    
1. Implement supervised fine-tuning 
2. Implement Direct Preference Optimization (DPO) 
3. Implement Group Relative Preference Optimization (GRPO)