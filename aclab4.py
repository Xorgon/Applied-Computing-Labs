from scipy import optimize as opt
import aclab3 as lab3


xfoil_path = "C:/Users/Elijah/Documents/XFoil/"


def one_dim_opt(cl, file_path, xfoil_path):
    """
    Performs a one dimensional optimization using minimize_scalar. This
    function optimizes for point u(2) between 0.6 and 1.3.

    cl -- target coefficient of lift for XFoil
    file_path -- path containing aerofoil.dat [NO SPACES ALLOWED]
    xfoil_path -- path containing xfoil.exe

    returns output from minimize_scalar
    """
    bs = [0.6, 0.9, 1.3]
    opt_out = opt.minimize_scalar(lab3.run_xfoil_wcl,
                                  args=(cl, file_path, xfoil_path, "d"),
                                  method="brent", bracket=bs)
    return opt_out


def four_dim_opt(x0, weight_limits, cl, file_path, xfoil_path, step_size=0.1):
    """
    Performs a four dimensional optimization using fmin_l_bfgs_b. This
    function optimizes for points u(1), u(2), l(1), l(2) between the defined
    weight limits.

    x0 -- array of starting points for the optimization
    weight_limits -- weight limits for u(1), u(2), l(1), l(2) respectively
    cl -- target coefficient of lift for XFoil
    file_path -- path containing aerofoil.dat [NO SPACES ALLOWED]
    xfoil_path -- path containing xfoil.exe
    step_size -- the step size for the optimization, default=0.1

    returns output from fmin_l_bfgs_b
    """
    opt_out = opt.fmin_l_bfgs_b(lab3.run_xfoil_wcl, x0,
                                args=(cl, file_path, xfoil_path, "d"),
                                bounds=weight_limits, epsilon=step_size,
                                approx_grad=True)
    return opt_out
