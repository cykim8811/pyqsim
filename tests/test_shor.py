
import pyqsim
import math
import random
from tqdm import tqdm
from fractions import Fraction

from pyqsim.gates import h, apply, qft
from pyqsim.types import qint

N = 21
T = math.ceil(math.log2(N ** 2))
n = math.ceil(math.log2(N))
a = 2

print(f"Running Shor's algorithm for N = {N}, a = {a} (T = {2**T}, n = {n})")

def ftn(x: int) -> int:
    return (a ** x) % N

res = {}
for i in tqdm(range(5)):
    argreg = h(qint(0, size=T))
    ftnreg = apply(argreg, ftn, output_size=n)
    argreg = qft(argreg)

    v = int(argreg)
    if v in res:
        res[v] += 1
    else:
        res[v] = 1

res_sorted = sorted(res.items(), key=lambda x: x[1], reverse=True)
res_selected = [t[0] / (2**T) for t in res_sorted[:5] if t[0] > 0]

def continued_fraction(x, max_depth=10):
    a = []
    for _ in range(max_depth):
        a.append(math.floor(x))
        if abs(x - a[-1]) < 1e-6:
            break
        x = 1 / (x - a[-1])
    return a

def convergents(a):
    p = [0, 1]
    q = [1, 0]
    convergents = []
    for i in range(len(a)):
        p.append(a[i] * p[-1] + p[-2])
        q.append(a[i] * q[-1] + q[-2])
        convergents.append((p[-1], q[-1]))
    return convergents

def get_period_candidates(qr_values, max_depth=10):
    candidates = set()
    for qr in qr_values:
        frac = Fraction(qr).limit_denominator()
        a = continued_fraction(frac.numerator / frac.denominator, max_depth)
        conv = convergents(a)
        candidates.update(q for _, q in conv[1:])  # Skip the first convergent (0/1)
    return sorted(candidates)

def check_period_candidates(candidates, a, N):
    for q in candidates:
        if a ** q % N == 1:
            return q
    return None

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def find_factor(N, r, a):
    if r % 2 != 0:
        return None
    
    factor1 = gcd(mod_exp(a, r // 2, N) - 1, N)
    factor2 = gcd(mod_exp(a, r // 2, N) + 1, N)
    
    if 1 < factor1 < N:
        return factor1
    elif 1 < factor2 < N:
        return factor2
    else:
        return None

def shor_factorization(N, r):
    if N % 2 == 0:
        return 2
    
    for _ in range(100):  # 충분한 시도 횟수
        a = random.randint(2, N - 1)
        if gcd(a, N) != 1:
            return gcd(a, N)
        
        factor = find_factor(N, r, a)
        if factor:
            return factor
    
    return None

candidates = get_period_candidates(res_selected, max_depth=10)
period = check_period_candidates(candidates, a, N)
factor = shor_factorization(N, period)

if factor is None:
    print(f"Failed to find factors of {N}")
else:
    print(f"Factors of {N}: {factor}, {N // factor}")
    
