"""Arithmetic behind the Session 9 explain-before-use slides (11 November 2026). Pure Python, no model needed."""
import math
# cosine recall (Session 4 vectors) and what a score means as an angle
ana, ben, chloe = (3, 4), (6, 8), (4, 3)
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
ln = lambda a: math.sqrt(dot(a, a))
print('Ana.Chloe', dot(ana, chloe), '|Ana|', ln(ana), '|Chloe|', ln(chloe), 'cos', dot(ana, chloe) / (ln(ana) * ln(chloe)), 'angle', round(math.degrees(math.acos(0.96))))
for c in (1.0, 0.96, 0.73, 0.6, 0.47, 0.0):
    print('cos', c, 'angle', round(math.degrees(math.acos(c)), 1))
# small LoRA picture
W = [[2, 0, 1, 3], [1, 1, 0, 2], [0, 2, 1, 1], [3, 1, 2, 0]]
B = [1, 0, 2, 0]
A = [1, 0, 0, 1]
BA = [[b * a for a in A] for b in B]
Wp = [[W[i][j] + BA[i][j] for j in range(4)] for i in range(4)]
print('BA', BA)
print("W'", Wp)
print('times table 4x4', [[i * j for j in range(1, 5)] for i in range(1, 5)])
print('counts 4x4: W', 4 * 4, 'B+A at r=1', 1 * (4 + 4))
# GPT-2 numbers (shapes as stored in GPT-2: c_attn weight 768 x 2,304)
d, k, r, blocks, total = 768, 2304, 8, 12, 124_439_808
print('W', d * k, 'B (d x r)', d * r, 'A (r x k)', r * k, 'B+A', d * r + r * k, 'r(d+k)', r * (d + k))
print('all blocks', blocks * r * (d + k), 'share', blocks * r * (d + k) / total)
print('handbook tokens per word', 1074 / 829)
