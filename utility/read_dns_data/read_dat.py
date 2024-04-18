import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import vtk
from vtk.numpy_interface import dataset_adapter as dsa


def dat_to_coords(file_path):
    # Read file in .dat format
    data = np.loadtxt(file_path, skiprows=0)
    return data[:, 0], data[:, 1]

def vtr_to_dict(file_path):
    # Read file in .vtr format
    reader = vtk.vtkXMLRectilinearGridReader()
    reader.SetFileName(file_path)
    reader.Update()
    # Get the output grid
    grid = reader.GetOutput()

    # Get the point data
    point_data = grid.GetPointData()

    # Get the number of arrays
    num_arrays = point_data.GetNumberOfArrays()

    dict = {}
    # Loop through each array
    for i in range(num_arrays):
        array_name = point_data.GetArrayName(i)
        array = point_data.GetArray(array_name)

        # Get the number of tuples (points)
        num_tuples = array.GetNumberOfTuples()

        # Extract array values
        values = []
        for j in range(num_tuples):
            # Extract value for each tuple (point)
            value = array.GetValue(j)
            values.append(value)

        # Store array values in dictionary
        dict[array_name] = np.array(values)

    # Release memory
    reader.ReleaseDataFlagOn()

    # Clean up the reader
    reader.Update()
    reader = None  # Set reader to None to release memory
    return dict


if __name__=="__main__":

    # paths to the files
    folder = "../../pehill-29-cases-DNS/alph10-9-3036"
    dat_file_path = os.path.join(folder, 'mean_files.dat')
    file_path_vtr = os.path.join(folder, 'mean.vtr')

    # extract data and put into a dictionary
    dict_data = vtr_to_dict(file_path_vtr)
    dict_data['X'], dict_data['Y'] = dat_to_coords(dat_file_path)
    umean = dict_data['VMEAN']

    plt.figure()
    plt.scatter(dict_data['X'], dict_data['Y'], c=umean)
    plt.colorbar()
    plt.show()

