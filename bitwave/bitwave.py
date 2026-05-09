MASK10 = 0b1111111111
SIN = 0b1010101010

def sign(atom):
    return (atom >> 15) & 1

def exponent(atom):
    return (atom >> 10) & 0b11111

def pattern(atom):
    return atom & MASK10

def entropy(p):
    return bin(p).count("1")

def difference(a, b):
    return pattern(a) ^ pattern(b)

def x_wave(a, b):
    return difference(a, b) ^ SIN

def y_wave(a, b):
    return x_wave(a, b) ^ MASK10

def velocity(prev_beta, beta):
    return prev_beta ^ beta

def acceleration(prev_v, v):
    return prev_v ^ v

def stable(prev_v, v):
    return acceleration(prev_v, v) == 0

a = 0b0_00001_1010101010
b = 0b0_00001_1111000000

x = x_wave(a, b)
y = y_wave(a, b)

print("a pattern:", bin(pattern(a)))
print("b pattern:", bin(pattern(b)))
print("difference:", bin(difference(a, b)))
print("x_wave:", bin(x), "entropy:", entropy(x))
print("y_wave:", bin(y), "entropy:", entropy(y))
