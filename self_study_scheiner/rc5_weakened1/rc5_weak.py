def add_uint32(a, b):
    return (a + b) % (2**32)

class RC5Weak:
    NROUNDS = 8

    def __init__(self):
        # Roundkey list of ints
        self.S = None

    def set_roundkey(self, k: bytes):
        assert len(k) == 2*(self.NROUNDS + 1) * 4

        blocks = (k[4*i:4*i+4] for i in range(len(k)//4))
        self.S = [int.from_bytes(block, byteorder="big") for block in blocks]

    
    def encrypt(self, data: bytes):
        assert len(data) == 8
        assert self.S is not None, "Key must be set before"
        A = int.from_bytes(data[:4], byteorder="big")
        B = int.from_bytes(data[4:], byteorder="big")

        S = self.S
        A = add_uint32(A, S[0])
        B = add_uint32(B, S[1])
        for i in range(1, self.NROUNDS + 1):
            A = add_uint32(A ^ B, S[2*i])
            B = add_uint32(B ^ A, S[2*i + 1])

        enc = int.to_bytes(A, 4, "big") + int.to_bytes(B, 4, "big")

        return enc

    def decrypt(self, data: bytes):
        assert len(data) == 8
        assert self.S is not None, "Key must be set before"
        A = int.from_bytes(data[:4], byteorder="big")
        B = int.from_bytes(data[4:], byteorder="big")

        S = self.S
        A = add_uint32(A, S[0])
        B = add_uint32(B, S[1])
        for i in range(1, self.NROUNDS + 1):
            A = add_uint32(A ^ B, S[2*i])
            B = add_uint32(B ^ A, S[2*i + 1])

        enc = int.to_bytes(A, 4, "big") + int.to_bytes(B, 4, "big")

        return enc


