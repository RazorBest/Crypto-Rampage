from collections import defaultdict

data = ""
with open("text") as f:
    data = f.read()
    data = data.split()

freq = defaultdict(lambda: 0)
for d in data:
    freq[d] += 1

freq = defaultdict(lambda: 0)
for d in [''.join(data[i:i+2]) for i in range(0, len(data), 2)]:
    freq[d] += 1

freq = defaultdict(lambda: 0)
for d in [''.join(data[i:i+4]) for i in range(0, len(data), 4)]:
    freq[d] += 1

print(len(freq))
print(len(data))
print(freq)

print([''.join(data[i:i+4]) for i in range(0, len(data), 4)])

