from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
# import transformers

model_id = "mistralai/Mistral-7B-Instruct-v0.2"
bnb_config = BitsAndBytesConfig(load_in_4bit=True, 
                                            bnb_4bit_quant_type='nf4',
                                            bnb_4bit_use_double_quant=True,
                                            bnb_4bit_compute_dtype=torch.bfloat16)

tokenizer = AutoTokenizer.from_pretrained(model_id)


device = "cuda:0"

model = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        # config=model_config,
        quantization_config=bnb_config,
        torch_dtype=torch.float16,
        load_in_8bit=True,
        device_map=device,
        # use_auth_token=hf_auth
    )

text = "Who are you ?"
inputs = tokenizer(text, return_tensors="pt").to(device)

outputs = model.generate(**inputs, max_new_tokens=512)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))