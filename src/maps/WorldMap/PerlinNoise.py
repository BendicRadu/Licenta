from random import randint

import numpy as np


def perlin_noise(size_x, size_y, frequency, seed):
    np.random.seed(seed)
    gradient = np.random.rand(512, 512, 2) * 2 - 1

    # linear space by frequency
    x = np.tile(
        np.linspace(0, frequency, size_x, endpoint=False),
        size_y
    )
    y = np.repeat(
        np.linspace(0, frequency, size_y, endpoint=False),
        size_x
    )
    # gradient coordinates
    x0 = x.astype(int)
    y0 = y.astype(int)
    # local coordinate
    x -= x0
    y -= y0
    # gradient projections
    g00 = gradient[x0, y0]
    g10 = gradient[x0 + 1, y0]
    g01 = gradient[x0, y0 + 1]
    g11 = gradient[x0 + 1, y0 + 1]
    # fade
    t = (3 - 2 * x) * x * x
    # linear interpolation
    r = g00[:, 0] * x + g00[:, 1] * y
    s = g10[:, 0] * (x - 1) + g10[:, 1] * y
    g0 = r + t * (s - r)
    # linear interpolation
    r = g01[:, 0] * x + g01[:, 1] * (y - 1)
    s = g11[:, 0] * (x - 1) + g11[:, 1] * (y - 1)
    g1 = r + t * (s - r)
    # fade
    t = (3 - 2 * y) * y * y
    # (bi)linear interpolation
    g = g0 + t * (g1 - g0)
    # reshape
    return g.reshape(size_y, size_x)


def banded_perlin_noise(size_x, size_y, frequencies, amplitudes):

    seed = randint(0, 1000)

    image = np.zeros((size_y, size_x))
    for f, a in zip(frequencies, amplitudes):
        image += perlin_noise(size_x, size_y, f, seed) * a
    image -= image.min()
    image /= image.max()
    return image

