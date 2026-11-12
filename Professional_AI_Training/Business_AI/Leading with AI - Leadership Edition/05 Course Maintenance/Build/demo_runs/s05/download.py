from transformers import AutoTokenizer, AutoModelForCausalLM
import sys
for name in sys.argv[1:]:
    AutoTokenizer.from_pretrained(name); AutoModelForCausalLM.from_pretrained(name)
    print('ok', name)
