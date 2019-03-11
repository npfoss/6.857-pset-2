#!/usr/bin/python
from random import randint

def getSamples(num=99999999):
    samples = []
    c = 0
    with open('30000_samples.txt', 'r') as f:
        l = f.readline()
        for i in range(randint(0, 30000-num)):
            l = f.readline()
        while l and (c < num):
            c += 1
            l = l.strip().strip(';').split(', ')
            s = {
                'plain': [int(n) for n in l[0].split(' ')],
                'cipher': [int(n) for n in l[1].split(' ')],
                'leak': int(l[2])
            }
            s['plain_bits'] = []
            for p in s['plain']:
                s['plain_bits'] += [bool(p & 2**x) for x in range(8)] #note: LSB first. don't get it backwards later
            samples.append(s)
            l = f.readline()
    return samples

def bitsToBytes(l):
    return [ int(''.join([str(l[i*8 + 7 - j]) for j in range(8)]), 2) for i in range(16)]

def decideBit(key_so_far, samples, i=0, kb=0):
    """
    if the current bit of the input is 0, high means key is 1
    if current bit is 1, high means key is 0
    """
    n = len(samples)
    t = 1407 - len(key_so_far)
    thresh = n * t / 8.0 - n / 4.0
    keybit = kb
    # print 'expected low ', n * t / 8.0 - 3 * n / 8.0
    # print 'expected high', n * t / 8.0 - n / 8.0
    # print 'thresh', thresh

    for keybit in range(1):
        total0 = 0
        c0 = 0
        t1 = 0
        c1 = 0
        for s in samples:
            if not s['plain_bits'][i]:
                total0 += s['leak']
                c0 += 1
            else:
                t1 += s['leak']
                c1 += 1
            # total += s['leak'] - (keybit ^ s['plain_bits'][i]) * 3.0 / 8

        # print 'actual', total #- n / 2.0 * 3 / 8
        # print 'actual', 1.0*total0/c0 #- n / 2.0 * 3 / 8
        # print 'actual', 1.0*t1/c1 #- n / 2.0 * 3 / 8
        return int(1.0*total0/c0 > 1.0*t1/c1)



samples = getSamples(15000)
print len(samples)

key = []
for i in range(128):
    key.append(decideBit(key, samples, i))
# for j in range(20):
#     decideBit(key, samples, i=j)
# from IPython import embed; embed()

# print key

from aes import AES
aes = AES()

key = bitsToBytes(key)
print key
m = samples[0]['plain']
cipher = aes.encrypt(m, key, 16)
print cipher
print samples[0]['cipher']

