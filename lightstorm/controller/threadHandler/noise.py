import math


def rnd(x):
    x = (x << 13) ^ x
    return 1.0 - ((x * (x * x * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0


def cos_int(a, b, x):
    ft = x * 3.1415927
    f = (1 - math.cos(ft)) * 0.5
    return a * (1 - f) + b * f


def noise(x, octaves):
    t = x % 1
    p0 = rnd(math.floor(x))
    p1 = rnd(math.floor(x) + 1)
    val = cos_int(p0, p1, t)
    if octaves > 1:
        val += noise(x * 2 ** octaves, octaves - 1) / octaves
    return val
