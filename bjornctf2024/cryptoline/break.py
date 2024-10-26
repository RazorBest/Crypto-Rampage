from pwn import *

SHIFT = 39
P = 128-SHIFT

"""
HOST = "line.ctf.flagbot.ch"
PORT = 1338 
p = remote(HOST, PORT)
"""
p = process("./server.py")

data = p.recvuntil(b"encrypt:")
print(data)

data = data.decode("utf8")
MESSAGE_SIZE = int(data[data.find("encrypt ")+8:].split()[0])
print(MESSAGE_SIZE)

def str_to_shifted_list(enc: str):
    ct_list = []
    for c in enc:
        ct_list.append(ord(c) - (SHIFT-1))

    return ct_list

sec = []

data = b""
def get_enc_m_remote(to_send):
    global data
    print(f"Sending {to_send}")
    p.sendline(to_send)
    data = p.recvline()
    data += p.recvline()
    data += p.recv(32)

    print(data)
    enc = data.split(b"\n")[1]
    print(f"Ciphertext: message {enc}")

    """
    # Don't read the flag yet
    if b"My flag is" in data:
        idx = data.find(b"My flag is")
        p.unrecv(data[idx:])
    """

    return str_to_shifted_list(enc.decode("utf8"))

def get_flag_remote():
    global data
    data += p.recvall(timeout=3)
    data = data.decode("utf8")
    index = data.find("My flag is: ") + len("My flag is: ")
    assert index != -1
    enc_flag = data[index:]
    end = enc_flag.find("\n")
    enc_flag = enc_flag[:end]

    return enc_flag

"""
# For running the server as a python module
import server
from server import Lines
lines = Lines()
def get_enc_m(to_send):
    enc = lines.encrypt(to_send.decode("utf8"))
    return str_to_shifted_list(enc)

def get_flag():
    return lines.encrypt(server.flag)
"""

for i in range(MESSAGE_SIZE):
    # Set the message to be made out of 0s, except for the i character
    # The message will be l-rotted by (SHIFT-1), which is 38.
    # So, "&" means 0 and "'" means 1.
    to_send = b"&" * (i) + b"'" + b"&" * (MESSAGE_SIZE - 1 - i) 
    ct_list = get_enc_m_remote(to_send)
    sec.append(ct_list)

enc_flag = get_flag_remote()

print(f"Enc flag: {enc_flag!r}")

# Phase 2
import numpy as np

print(enc_flag)
ct_flag = str_to_shifted_list(enc_flag)

sec = np.array(sec)
ct_flag = np.array(ct_flag)

def solve_the_system(A, b):
    # Assume A is a square matrix
    n = len(A)
    for i in range(n):
        # The only case this fails is when A[i][i] is 0
        # If this happens, just start the challenge again
        inv = pow(int(A[i][i]), -1, P)

        # Force A[i][i] to become 1
        A[i] = (A[i] * inv) % P
        b[i] = (b[i] * inv) % P
        for j in range(n):
            if j == i:
                continue

            ct = A[j][i]
            # Force A[j][i] to become 0
            A[j] = (A[j] - A[i] * ct) % P
            b[j] = (b[j] - b[i] * ct) % P

    return b

sec = np.transpose(sec)
ct_flag = np.transpose(ct_flag)
print(ct_flag)

print(f"Shape of SK: {np.shape(sec)}")
print(f"Shape of flag: {np.shape(ct_flag)}")

flag = solve_the_system(sec, ct_flag)
print(f"flag {flag}")
flag = [ chr(l+(SHIFT-1)) for l in flag]

print(f'Decoded: {"".join(flag)}')
