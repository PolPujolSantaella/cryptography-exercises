############################################
# Exercise 7: Implement an algorithm to produce candidate plaintext ranked by likelihood
############################################

import math
import random
from collections import Counter, defaultdict

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

sample_corpus = """
This is a sample corpus of English text. It is used to generate frequency statistics for letters and letter pairs. The quick brown fox jumps over the lazy dog. The rain in Spain stays mainly in the plain. To be or not to be, that is the question.
""".upper()

def build_trigrams(text):
    text = ''.join(ch if ch.isalpha() or ch.isspace() else ' ' for ch in text)
    text = ' '.join(text.split())
    padded = '  ' + text
    C = Counter()
    total = 0
    for i in range(len(padded) - 2):
        tri = padded[i:i+3]
        C[tri] += 1
        total += 1

    V = len(C)
    probs = {tri: math.log((cnt + 1) / (total + V)) for tri, cnt in C.items()}
    default = math.log(1 / (total + V))
    return probs, default

TRI_PROBS, TRI_DEFAULT = build_trigrams(sample_corpus)

def trigram_score(text):
    text = ''.join(ch if ch.isalpha() or ch.isspace() else ' ' for ch in text)
    text = ' '.join(text.split())
    padded = '  ' + text
    s = 0.0
    for i in range(len(padded) - 2):
        tri = padded[i:i+3]
        s += TRI_PROBS.get(tri, TRI_DEFAULT)

    return s

def decrypt_with_key(ciphertext, key_map):
    out = []
    for ch in ciphertext:
        if ch in alphabet:
            out.append(key_map[ch])
        else:
            out.append(ch)

    return ''.join(out)

def random_key():
    perm = list(alphabet)
    random.shuffle(perm)
    return {alphabet[i]: perm[i] for i in range(len(alphabet))}

def initial_key_by_freq(ciphertext):
    eng_rank = list("ETAOINSHRDLCUMWFGYPBVKJXQZ")
    cnt = Counter(ch for ch in ciphertext if ch.isalpha())
    cipher_rank = [x for x, _ in cnt.most_common()] + [c for c in alphabet if c not in cnt]
    mapping = {}
    for i, c in enumerate(cipher_rank):
        mapping[c] = eng_rank[i]
    return mapping

def hill_climbing(ciphertext, restarts=500, iter_per_restart=10000):
    best_plain = None
    best_score = -1e9

    for r in range(restarts):
        if r == 0:
            key = initial_key_by_freq(ciphertext)
        else:
            key = random_key()

        current_plain = decrypt_with_key(ciphertext, key)
        current_score = trigram_score(current_plain)

        improved = True
        it = 0
        while it < iter_per_restart and improved:
            improved = False
            it += 1
            for _ in range(200):
                a, b = random.sample(alphabet, 2)
                key2 = key.copy()
                key2[a], key2[b] = key2[b], key2[a]
                plain2 = decrypt_with_key(ciphertext, key2)
                s2 = trigram_score(plain2)
                if s2 > current_score:
                    key = key2
                    current_plain = plain2
                    current_score = s2
                    improved = True
                    break
        if current_score > best_score:
            best_score = current_score
            best_plain = current_plain

    return best_plain, best_score

if __name__ == "__main__":
    ciphertext = "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ."
    plaintext, score = hill_climbing(ciphertext)
    print("Decrypted Text:", plaintext)
    print("Score:", score)