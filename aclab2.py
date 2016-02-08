import aclab1 as lab1
import numpy as np
import matplotlib

plot = matplotlib.pyplot.plot


def serialize_array(array):
    """ Returns a string with array values in columns """
    string = ""
    for val in array:
        string += str(val[0]) + " " + str(val[1]) + "\n"
    return string


def bezier_spline_aerofoil(file_path):
    lower = np.array([[1.0, 0.0],
                      [0.5, 0.08],
                      [0.0, -0.05]])
    n = float(len(lower))
    upper = np.array([[0.0, 0.1],
                      [0.4, 0.2],
                      [1.0, 0.0]])
    m = float(len(upper))
    connect = np.add(np.multiply(upper[0], m / (m + n)),
                     np.multiply(lower[n - 1], n / (m + n)))
    lower = np.concatenate((lower, [connect]))
    upper = np.concatenate(([connect], upper))
    l_bez = lab1.rational_bezier(lower, [1, 1, 1, 1])
    u_bez = lab1.rational_bezier(upper, [1, 1, 1, 1])
    u_bez = np.delete(u_bez, len(u_bez) - 1, axis=0)
    aero_spline = np.concatenate((l_bez, u_bez))
    aerofoil_file = open(file_path + "aerofoil.dat", "w")
    aerofoil_file.write("MyFoil\n" + serialize_array(aero_spline).strip())
