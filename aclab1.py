import aclabtools
import numpy as np
import pylab as pl

choose = aclabtools.choose


def bernstein(i, n, t):
    """ Returns the bernstein polynomial for i, n and t """
    return choose(n, i) * (t ** i) * ((1 - t) ** (n - i))


def bezier(points):
    """ Returns bezier curve coordinates from points """

    def b(t):
        out = np.array([0, 0])
        n = len(points) - 1
        for i in range(n + 1):
            point = np.multiply(points[i], bernstein(i, n, t))
            out = np.add(out, point)
        return out

    b_points = np.empty((0, 2))
    for t in np.linspace(0, 1, 101):
        b_points = np.append(b_points, np.array([b(t)]), axis=0)
    return b_points


def rational_bezier(points, weights):
    """ Draws a bezier curve from points with weights and returns coords """

    def b(t):
        numer = np.array([0, 0])
        denom = np.array([0, 0])
        n = len(points) - 1
        for i in range(n + 1):
            wbi = weights[i] * bernstein(i, n, t)
            numer = np.add(numer, np.multiply(points[i], wbi))
            denom = np.add(denom, wbi)
        return np.divide(numer, denom)

    bez = np.empty((0, 2))
    for t in np.linspace(0, 1, 101):
        bez = np.append(bez, np.array([b(t)]), axis=0)
    pl.plot(p[:, 0], p[:, 1], 'ko')
    pl.plot(p[:, 0], p[:, 1], 'g')
    pl.plot(bez[:, 0], bez[:, 1], 'r')
    return bez


# Points and weights
p = np.array([[0, 0], [.5, .05], [1, 0], [.8, .2], [.65, .25], [0, 0]])
w = np.array([1, 15, 50, 15, 5, 1])

# Plotting
bez = rational_bezier(p, w)
pl.axis([0, 1, -0.5, 0.5])
# pl.plot(p[:, 0], p[:, 1], 'ko')
# pl.plot(p[:, 0], p[:, 1], 'g')
# pl.plot(bez[:, 0], bez[:, 1], 'r')
