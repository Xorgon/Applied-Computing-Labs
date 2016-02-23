import aclabtools as tools
import aclab1 as lab1
import aclab2 as lab2
import numpy as np
import matplotlib.pyplot as plt
import os

plot = plt.plot
serialize_array = lab2.serialize_array


xfoil_path = "C:/Users/Elijah/Documents/XFoil/"


def parametric_aerofoil(w, file_path):
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
    if type(w) is float:
        l_bez = lab1.rational_bezier(lower, [1, 1, 1, 1])
        u_bez = lab1.rational_bezier(upper, [1, 1, w, 1])
    else:
        l_bez = lab1.rational_bezier(lower, [1, w[2], w[3], 1])
        u_bez = lab1.rational_bezier(upper, [1, w[0], w[1], 1])
    aero_spline = np.concatenate((l_bez, u_bez))
    aerofoil_file = open(file_path + "aerofoil.dat", "w")
    aerofoil_file.write("MyFoil\n" + serialize_array(aero_spline).strip())


def run_xfoil_wcl(w, cl, file_path, xfoil_path, mode="dl"):
    parametric_aerofoil(w, file_path)
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
              "cl " + str(cl) + "\n\n\n" + \
              "quit\n"
    commands_in = open(file_path + "commands.in", "w")
    commands_in.write(command)
    commands_in.close()
    command = xfoil_path + "xfoil.exe < " + file_path + "commands.in"
    os.system(command)
    polar = open(file_path + "polar.dat", "r")
    values = polar.readlines()[-1].split()
    polar.close()
    os.remove(file_path + "polar.dat")
    out = []
    try:
        if mode.count("d") > 0:
            out.append(float(values[2]))
        if mode.count("l") > 0:
            out.append(float(values[1]))
        if len(out) == 1:
            return out[0]
        else:
            return tuple(out)
    except ValueError:
        return False


def parameter_sweep(w_array, cl, file_path, xfoil_path):
    cd = []
    plt.figure(0)
    for w in w_array:
        xfoil_out = run_xfoil_wcl(w, cl, file_path, xfoil_path)
        if xfoil_out:
            cd.append(xfoil_out[0])
        else:
            w_array = np.delete(w_array, w)
            print("XFoil failed to solve at w=" + str(w))
    plt.figure(1)
    plot(w_array, cd, 'o')
    tools.mls_curve_fit(w_array, cd, np.linspace(1.15, 1.85, 101))
    return cd
