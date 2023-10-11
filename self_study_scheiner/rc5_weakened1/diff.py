import itertools
import random
import secrets
from copy import deepcopy

from rc5_weak import RC5Weak

def xor_bytes(a, b):
    return bytes([x^y for x, y in zip(a, b)])

def and_bytes(a, b):
    return bytes([x&y for x, y in zip(a, b)])

def bits(a: bytes):
    return ''.join([bin(byte)[2:].zfill(8) for byte in a])

cipher = RC5Weak()
SECRET_K = secrets.token_bytes(2*(cipher.NROUNDS+1)*4)
cipher.set_roundkey(SECRET_K)

M = secrets.token_bytes(8)
ENC = cipher.encrypt(M)

def break_cipher2(ENC, cipher):
    dummy_cipher = RC5Weak()
    k = secrets.token_bytes(2*(cipher.NROUNDS+1)*4)
    n_blocks = len(k) // 4
    #blocks (k[i:i+4] for i in range(len(k)//4))
    #S = [int.from_bytes(block, byteorder="big") for block in blocks]


    m_list = [secrets.token_bytes(8) for _ in range(12)]
    enc_list = [cipher.encrypt(m) for m in m_list]

    for bit in range(32):
        byte_pos = bit // 8
        bit_pos = bit % 8
        mask = 1 << bit_pos

        plaintext_mask = [0]*8
        plaintext_mask[7 - byte_pos] = 1 << bit_pos
        plaintext_mask[3 - byte_pos] = 1 << bit_pos
        plaintext_mask = bytes(plaintext_mask)
        ciphertext_mask = bytes(plaintext_mask)

        print(bit)

        count = 0
        for i in range(2**n_blocks):
            final_diff = [0]*len(k)
            coeff = [int(x) for x in list(bin(i)[2:].zfill(n_blocks))]
            for j, c in enumerate(coeff):
                if not c:
                    continue
                final_diff[j*4 + byte_pos] = final_diff[j*4 + byte_pos] ^ mask
            final_diff = bytes(reversed(final_diff))

            k2 = xor_bytes(k, final_diff)
            dummy_cipher = RC5Weak()
            dummy_cipher.set_roundkey(k2)

            is_ok = True
            for m, enc in zip(m_list, enc_list):
                enc_test = dummy_cipher.encrypt(m)

                if and_bytes(enc, ciphertext_mask) != and_bytes(enc_test, ciphertext_mask):
                    is_ok = False
                    break

            if is_ok:
                k = k2
                break
        else:
            print("problem")

    return k

def break_cipher(ENC, cipher):
    m1 = secrets.token_bytes(8)
    for bit in range(4*8):
        byte_pos = bit // 8
        bit_pos = bit % 8

        # List of bytes, little endian
        diff1 = [b"\x00"] * 8
        diff1[byte_pos] = int.to_bytes(1 << bit_pos, length=1, byteorder="big")
        # Merge into bytes, big endian
        diff1 = b''.join(reversed(diff1))
        m2 = xor_bytes(m1, diff1) 

        # List of bytes, little endian
        diff2 = [b"\x00"] * 8
        diff2[byte_pos + 4] = int.to_bytes(1 << bit_pos, length=1, byteorder="big")
        # Merge into bytes, big endian
        diff2 = b''.join(reversed(diff2))
        m3 = xor_bytes(m1, diff2) 

        m4 = xor_bytes(m2, diff2) 

        enc1 = cipher.encrypt(m1)
        enc2 = cipher.encrypt(m2)
        enc3 = cipher.encrypt(m3)
        enc4 = cipher.encrypt(m4)

        # Mask for two bits
        diff = xor_bytes(diff1, diff2)

        if and_bytes(enc2, diff) == and_bytes(ENC, diff):
            m1 = m2
        if and_bytes(enc3, diff) == and_bytes(ENC, diff):
            m1 = m3
        if and_bytes(enc4, diff) == and_bytes(ENC, diff):
            m1 = m4

    return m1

m_found = break_cipher(ENC, cipher)
k_found = break_cipher2(ENC, cipher)

print(f"Found message: {m_found}")
print(f"Expected message: {M}")

cipher.set_roundkey(k_found)
print(f"Found enc: {cipher.encrypt(M)}")
print(f"Expected enc: {ENC}")
