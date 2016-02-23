from scipy import optimize as opt
import aclab3 as lab3


xfoil_path = "C:/Users/Elijah/Documents/XFoil/"


def one_dim_opt(x0, cl, file_path, xfoil_path):
    bs = [0.6, 0.9, 1.3]
    opt_out = opt.minimize_scalar(lab3.run_xfoil_wcl,
                                  args=(cl, file_path, xfoil_path, "d"),
                                  method="brent", bracket=bs)
    return opt_out


def four_dim_opt(x0, weight_limits, cl, file_path, xfoil_path, step_size=0.1):
    opt_out = opt.fmin_l_bfgs_b(lab3.run_xfoil_wcl, x0,
                                args=(cl, file_path, xfoil_path, "d"),
                                bounds=weight_limits, epsilon=step_size,
                                approx_grad=True)
    return opt_out
