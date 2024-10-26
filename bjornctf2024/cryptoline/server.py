#!/usr/bin/env python3
import secrets
import os

flag = os.environ.get("FLAG", "flagbot{test_flagshsgsssfuf}")
SHIFT = 39
P = 128-SHIFT
MESSAGE_SIZE = len(flag)

class Lines:
    def __init__(self):
        # Random array of ints below P
        self.sk = [secrets.randbelow(P) for _ in range(MESSAGE_SIZE**2)]

    def encrypt(self,message):
        # Rots the whole message by (SHIFT-1) to the left
        message_list = [ ord(l)-(SHIFT-1) for l in message]
        assert(len(message_list)**2==len(self.sk))

        ct_list = []
        for j in range (len(message_list)):
            s = 0
            for i in range(len(message_list)):
                """
                if "flag" in message and j == 0:
                    print(self.sk[j+len(message_list)*i], end=" ")
                """
                    
                s += message_list[i]*self.sk[j+len(message_list)*i]

            # s is m0 * s0 + m1 * s1 + m2 * s2 + ... + mk*sk

            ct_list.append(s%P)

        #ct_list = [sum([message_list[i]*self.sk[j+len(message_list)*i] for i in range (len(message_list))])%P for j in range (len(message_list))]
        ct= "".join([chr(c+(SHIFT-1)) for c in ct_list])
        return(ct)

def reverse(m, enc):
    message_list = [ ord(l)-(SHIFT-1) for l in message]
    ct_list = []
    for c in enc:
        ct_list.append(ord(c) - (SHIFT-1))

    print(ct_list)
    
    
if __name__ == "__main__":
    L = Lines()
    #print(L.sk)
    print("Welcome to my new encryption machine. It can encrypt " + str(MESSAGE_SIZE) + " character text messages")
    for i in range (MESSAGE_SIZE):
        message = input(str(MESSAGE_SIZE) + " character message to encrypt:\n")
        try:
            enc = L.encrypt(message)
            print(enc)
            #reverse(enc)
        except Exception as exc: 
            print("Bad message")
    print("My flag is: " + L.encrypt(flag))


