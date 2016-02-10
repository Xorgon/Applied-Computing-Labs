import aclab1 as lab1
import numpy as np
import matplotlib
import os

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


def run_xfoil(file_path, xfoil_path):
    command = "load " + file_path + "aerofoil.dat" + "\n" + \
              "panel\n" + \
              "oper\n" + \
              "visc 1397535\n" + \
              "M 0.1\n" + \
              "type 1\n" + \
              "pacc\n" + \
              file_path + "polar.dat" + "\n\n" + \
              "iter\n" + \
              "5000\n" + \
              "cl 1.2\n\n\n" + \
              "quit\n"
    commands_in = open(file_path + "commands.in", "w")
    commands_in.write(command)
    commands_in.close()
    command = xfoil_path + "xfoil.exe" + " < " + file_path + "commands.in"
    os.system(command)
    polar = open(file_path + "polar.dat", "r")
    values = polar.readlines()[12].split()
    polar.close()
    os.remove(file_path + "polar.dat")
    return values[1], values[2]
