from scipy import optimize as opt
import aclab3 as lab3


xfoil_path = "C:/Users/Elijah/Documents/XFoil/"


def one_dim_opt(x0, cl, file_path, xfoil_path):
    bs = [0.6, 0.9, 1.2]
    opt_out = opt.minimize_scalar(lab3.run_xfoil_wcl,
                                  args=(cl, file_path, xfoil_path),
                                  method="brent", bracket=bs)
    return opt_out
