
[video link](https://www.youtube.com/watch?v=6S59Y0ckTm4&list=PLZoTAELRMXVN9VbAx5I2VvloTtYmlApe3&index=1&ab_channel=KrishNaik)

# Qantization
conversion from higher memory format to a lower memory format. (with respect to weights -> matrix, so that we can download the model to do the inference)

## 1. Full precision / Half precision
there will be lost of information / accuracy, ex FP32 bit -> FP16bit (full precision -> half precision)
## 2. calibration: squeezing the length of weights
symmetric quantization: ex batch normalization
ex: unsigned int 8 quantization, min max scalar, [0...1000] -> [0....255],  zero point = 0, scale = 394
round(250/394)+0

asymmetric quantization
ex: uint 8  [-20.....1000]-> [0....255],  zero point = 5, scale = 394
round(-20/4)+5=0
## 3. mode of quantization: post training quantization, quantization aware training.

* Post training quantization (PTQ)

pretrained model -> calibration -> quantized model (loss accuracy) -> use cases

* quantization aware training (QAT)

pretrained model -> calibration / quantization -> (adding training data) fine tunning -> quantized model
in this case we do not loss much data accuracy

---

# LoRA, QLoRa
[video link](https://www.youtube.com/watch?v=l5a_uKnbEr4&list=PLZoTAELRMXVN9VbAx5I2VvloTtYmlApe3&index=2&ab_channel=KrishNaik)

## Lora: low rank adaptataion of LLM
```
gpt4 turbo -> full weight fine tunning -> app (ChatGPT) -> domain fine tunning
                                            -> specific task fine tunning
```
1. full parameter finetunning, challenge, update all the weights (175B), hardware resources constrain
LoRA instead of updateing all the weights, it would track the changes.

pre-trained weights + LoRA tracked weights = fine tuned weights

LoRA tracked weights: matrix decompsition, ex: 3*3 weights, we would get 3*1 X 1*3 (decompose to 2 array of matrix), then there's less figures, 9 to 6, and if it's a huge matrix, it would reduce even more.

`W0 + deltaW (tracked weights) = W0+BA` (B: 3*1, A: 1*3), so the high decrease of the trainable parameters is due to the matrix decomposition

## QLoRA: quantized LoRA
reduce the value of the weight, Lora already reduce the dimention
[example](https://www.youtube.com/watch?v=IZXNgu4dW70&ab_channel=KrishNaik), lora can find in package `keras-nlp`
```
# quantization

model_id = "google/gemma-2b"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
...
lora_config = LoraConfig(
    r=8,
    target_modules = ["q_proj"....."down_proj"],
    task_type = "CAUSAL_LM"
)
```


# additional info

* what is a rank? the rank of a matrix refers to the number of **linearly independent** rows or columns, for a 3*3 matrix if they are all independent then rank is 3, if the third row is sum of the first 2 then the rank is 2. 

#next 
--> how to validate and improve LLM / agent model?
