import numpy as np
from hillShape import profile, para_profile
from itertools import product
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
from pygem import FFD, RBF

def Lx_collection(alpha):
    '''
    Values of Lx depending on alpha.
    '''
    return [3.858*alpha + 2.142, 3.858*alpha + 5.142,
        3.858*alpha + 8.142]

def get_parameters(alphas, Lx_func, Ly):
    '''
    Build vector of parameters of shape (N, 3).
    Parameters are alpha (scaling of the hill width, Lx/H=Lx, the length along x,
    Ly/H=Ly, the length along y). H is constant and =1.
    '''
    params = []
    for alpha in alphas:
        for elx in Lx_func(alpha):
            for ely in Ly:
                params.append([alpha, elx, ely])
    return np.array(params) #(N, 3)

def plot_hills(arr, figsize=(15, 5), draw=True, ax=None, labels=None, name=None,
        linestyles=None):
    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()

    for idx,a in enumerate(arr):
        if labels is not None:
            ax.plot(*a.T, label=labels[idx], linestyle=linestyles[idx])
        else:
            ax.plot(*a.T, linestyles=linestyle[ids])
    ax.axis("equal")

    if draw:
        if labels is not None:
            plt.legend(loc='best')
        plt.show()
    else:
        return ax
    if name is not None:
        fig.savefig(name, dpi=300)

if __name__ == "__main__":

    # 1. Build UNDEFORMED control points of periodic hill
    x_step = 0.01
    x_coords = np.arange(0, 9, x_step)

    ## All the parameters considered in DNS simulations
    alphas = np.array([0.5, 1, 1.5])
    Ly = np.array([2.024, 3.036, 4.048])
    params = get_parameters(alphas, Lx_collection, Ly)

    ## At first build deformed hills for Lx=9 (only way to let their code work):
    coords_all = []
    labels = []
    linestyles = []
    for i in range(params.shape[0]):
        xa, ya = para_profile(x_coords, params[i, 0], params[i, 1])
        xa = np.append(xa, np.array([0, 0, xa[-1], xa[-1]]))
        ya = np.append(ya, np.array([1, params[i, 2], params[i, 2], 1]))
        coords = np.vstack((xa, ya)).T
        coords_all.append(coords)
        labels.append(f"{params[i, :]}")
        if params[i, 0]==0.5:
            linestyles.append('-')
        if params[i, 0]==1:
            linestyles.append('--')
        if params[i, 0]==1.5:
            linestyles.append('-.')

    plot_hills(coords_all, draw=True, labels=labels, name='img/all_shapes',
            linestyles=linestyles)
    np.save("data/params.npy", params)
    np.save("data/def_hills.npy", np.array(coords_all))

