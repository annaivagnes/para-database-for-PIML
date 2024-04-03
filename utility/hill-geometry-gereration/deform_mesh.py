import numpy as np
import os
import shutil
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
from smithers.io.openfoam import OpenFoamHandler as OFH

def rbf_deformation(undef_pts, def_pts, undef_mesh):
    '''
    Apply RBF interpolation on the underformed mesh, starting from the
    knowledge of the undeformed and deformed control points.
    '''
    undef_pts, uindexes = np.unique(undef_pts, return_index=True, axis=0)
    def_pts = def_pts[uindexes]
    rbf = RBFInterpolator(undef_pts, def_pts)
    def_mesh = rbf(undef_mesh)
    return def_mesh

def write_mesh(undef_folder, def_folder, def_mesh):
    if not os.path.exists(def_folder):
        shutil.copytree(undef_folder, def_folder)
        os.remove(os.path.join(def_folder, 'constant/polyMesh/points'))
    OFH().write_points(def_mesh,
            os.path.join(def_folder, "constant/polyMesh/points"),
            os.path.join(undef_folder, "constant/polyMesh/points"))
    os.system("module use /opt/contrib/mathlab/modules")
    os.system("module load openfoam/2012")
    os.system(f"cd {def_folder}")
    os.system("checkMesh > log.checkMesh")


if __name__ == "__main__":
    # Import control points (undeformed and deformed hills)
    pts = np.load("data/def_hills.npy")
    params = np.load("data/params.npy")
    print("Parameters (alpha, Lx, Ly): ", params)
    def_par = params[1, :]

    # Distinguish undeformed and deformed shapes (we have the undeformed mesh,
    # of course)
    undef_pts = pts[4, :, :]
    def_pts = pts[1, :, :]

    # Import undeformed mesh
    undef_folder_mesh = "../../pehill-5-cases-OpenFOAM/case_0p5"
    undef_mesh_all = OFH().read(undef_folder_mesh)["0"]["points"]

    # Select only points on a plane (we have 3D mesh)
    print(undef_mesh_all[:20, :], undef_mesh_all[15000:15020, :])
    undef_mesh = undef_mesh_all[undef_mesh_all[:, 2] < 0.01][:, :2]
    print("Number of points of the mesh: ", undef_mesh.shape[0])

    # Apply RBF interpolation to deform the mesh
    def_mesh = rbf_deformation(undef_pts, def_pts, undef_mesh)

    # Plot undeformed and deformed mesh points
    fig = plt.figure(figsize=(10, 5))
    #plt.scatter(undef_mesh[:, 0], undef_mesh[:, 1], s=1, label="undef")
    #plt.scatter(def_mesh[:, 0], def_mesh[:, 1], s=1, label="def")
    #fig.savefig("img/mesh_deformation_example.png", dpi=300)
    #plt.show()

    # Save the new mesh in a different folder
    def_mesh_all = np.vstack((np.tile(def_mesh, (2, 1)).T,
        undef_mesh_all[:, 2].reshape(1, undef_mesh_all.shape[0]))).T
    def_folder_mesh = f"../../pehill-5-cases-OpenFOAM/{def_par[0]}_{def_par[1]}_{def_par[2]}"
    write_mesh(undef_folder_mesh, def_folder_mesh, def_mesh_all)






