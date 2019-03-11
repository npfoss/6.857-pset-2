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
            s['plain_bits'] = []
            for p in s['plain']:
                s['plain_bits'] += [bool(p & 2**x) for x in range(8)] #note: LSB first. don't get it backwards later
            samples.append(s)
            l = f.readline()
    return samples

def decideBit(key_so_far, samples, i=0, kb=0):
    """
    if the current bit of the input is 0, high means key is 1
    if current bit is 1, high means key is 0
    """
    n = len(samples)
    t = 1407 - len(key_so_far)
    thresh = n * t / 8.0 - n / 4.0
    keybit = kb
    print 'expected low ', n * t / 8.0 - 3 * n / 8.0
    print 'expected high', n * t / 8.0 - n / 8.0
    print 'thresh', thresh

    for keybit in range(1):
        total = 0
        for s in samples:
            total += s['leak'] - (keybit ^ s['plain_bits'][i]) * 3.0 / 8

        print 'actual', total


samples = getSamples()

key = []
# for i in range(128):
key.append(decideBit(key, samples))
from IPython import embed; embed()

'''
from aes import AES

key = bitsToBytes(key)
m = map(ord, samples[0]['plain'])
cipher = aes.encrypt(m, key, 16)
print cipher
print samples[0]['cipher']

'''