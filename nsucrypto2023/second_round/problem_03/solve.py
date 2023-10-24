from hashlib import sha256
from os import walk, makedirs
from os.path import join, getsize, exists

ENCRYPTED_FILES_PATH = "encrypted_files"
DECRYPTED_FILES_PATH = "decrypted_files"

if not exists(DECRYPTED_FILES_PATH):
    makedirs(DECRYPTED_FILES_PATH)

values = [
"602a4a8fff652291fdc0e049e3900dae608af64e5e4d2c5d4332603c9938171d",
"f40e838809ddaa770428a4b2adc1fff0c38a84abe496940d534af1232c2467d5",
"aa105295e25e11c8c42e4393c008428d965d42c6cb1b906e30be99f94f473bb5",
"70f87d0b880efcdbe159011126db397a1231966991ae9252b278623aeb9c0450",
"77a39d581d3d469084686c90ba08a5fb6ce621a552155730019f6c02cb4c0cb6",
"456ae6a020aa2d54c0c00a71d63033f6c7ca6cbc1424507668cf54b80325dc01",
"bd0fd461d87fba0d5e61bed6a399acdfc92b12769f9b3178f9752e30f1aeb81d",
"372df01b994c2b14969592fd2e78d27e7ee472a07c7ac3dfdf41d345b2f8e305",
]

sols = []
for i in range(800):
    for j in range(800):
        m = sha256(b"P6 " + str(i).encode() + b" " + str(j).encode() + b" 255")
        digest = m.hexdigest()

        if digest in values:
            header = b"P6\n" + str(i).encode() + b" " + str(j).encode() + b"\n255\n"
            sols.append((i*j, header, i, j))

sols = sorted(sols)
for product, header, *_ in sols:
    digest = sha256(header).hexdigest()
    print(f"{header} - {digest}. Product: {product}")

def get_enc_files():
    enc_files = [files for _, _, files in walk(ENCRYPTED_FILES_PATH)]
    # Flatten
    enc_files = [join(ENCRYPTED_FILES_PATH, f) for files in enc_files for f in files]
    return enc_files

enc_files = get_enc_files()
enc_files = zip([getsize(file) for file in enc_files], enc_files)
enc_files = sorted(enc_files)

for sol, enc_file in zip(sols, enc_files):
    print(sol)
    print(enc_file)
    _, header, width, height = sol
    _, path = enc_file

    initial_size = width * height * 3 + len(header)
    print(initial_size)

    data = None
    with open(path, 'rb') as file:
        data = file.read()
    data_with_real_header = header + data
    data_with_real_header = data_with_real_header[:initial_size]

    new_path = path.replace(ENCRYPTED_FILES_PATH, DECRYPTED_FILES_PATH)

    with open(new_path, 'wb') as file:
        file.write(data_with_real_header)


