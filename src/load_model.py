import transformers
import torch
from peft import LoraConfig, get_peft_model
import os

def load_model():
    model_id = 'meta-llama/Llama-2-7b-chat-hf'

    device = "cuda:0"

    bnb_config = transformers.BitsAndBytesConfig(load_in_4bit=True, 
                                                bnb_4bit_quant_type='nf4',
                                                bnb_4bit_use_double_quant=True,
                                                bnb_4bit_compute_dtype=torch.bfloat16)

    hf_auth = os.getenv('HF_AUTH')
    model_config =  transformers.AutoConfig.from_pretrained(
        model_id,
        use_auth_token=hf_auth
    )

    print("Loading the model...")
    model = transformers.AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        config=model_config,
        quantization_config=bnb_config,
        torch_dtype=torch.float16,
        load_in_8bit=True,
        device_map=device,
        use_auth_token=hf_auth
    )
    print("Successfully loaded the model !!!!")

    print("Loading the tokenizer ...")
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        model_id,
        use_auth_token=hf_auth,
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    print("Successfully loaded the tokenizer !!!")

    print("Updating the model using Lora ...")
    ##voicexd/llama2-13b-chat-sharegpt
    lora_config = LoraConfig.from_pretrained("jaswanth04/llama2-7b-chat-sharegpt", token=hf_auth)
    model = get_peft_model(model, lora_config)
    model = model.to(device)
    print("Successfully updated the model using LORA !!!")

    return model, tokenizer