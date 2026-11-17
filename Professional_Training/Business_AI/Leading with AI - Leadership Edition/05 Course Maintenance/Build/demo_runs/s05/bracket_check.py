"""Check for Session 8 slide 'Your prompt is the start of that text' (11 November 2026).
Reuses the numpy GPT-2 forward pass of logits_s05.py (same weights) and prints the top 5 next tokens
after 'Please pay the invoice within thirty' and after the same text plus ' ('."""
import numpy as np
src = open('logits_s05.py').read()
exec(src[:src.index('prompts = [')])
for text in ['Please pay the invoice within thirty', 'Please pay the invoice within thirty (']:
    z = logits(encode(text)); z = z[-1] if z.ndim > 1 else z
    pr = softmax(z)
    top = np.argsort(-pr)[:5]
    print(repr(text), [(decode([int(k)]), round(float(pr[k]) * 100, 2)) for k in top])
