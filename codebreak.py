#!/usr/bin/python


def getSamples():
    samples = []
    with open('30000_samples.txt', 'r') as f:
        l = f.readline()
        while l:
            l = l.strip().strip(';').split(', ')
            s = {
                'plain': [int(n) for n in l[0].split(' ')],
                'cipher': [int(n) for n in l[1].split(' ')],
                'leak': int(l[2])
            }
            samples.append(s)
            l = f.readline()
    return samples

def decideBit(key_so_far, samples):
    n = len(samples)
    t = 1408 - len(key_so_far)
    thresh = n * t / 8.0 - n / 4.0

    total = 0
    for s in samples:
        total += s['leak']

    print 'expected low ', n * t / 8.0 - 3 * n / 8.0
    print 'expected high', n * t / 8.0 - n / 8.0
    print 'thresh', thresh
    print 'actual', total

samples = getSamples()

key = []
for i in range(128):
    key.append(decideBit(key, samples))

'''
from aes import AES

key = bitsToBytes(key)
m = map(ord, samples[0]['plain'])
cipher = aes.encrypt(m, key, 16)
print cipher
print samples[0]['cipher']

'''