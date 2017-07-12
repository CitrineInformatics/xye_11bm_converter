from pypif.obj import *
from pypif import pif


def convert(files=[], chemical_formula=None, temperature_kelvin=None):
    """
    Get list of chemical systems by parsing a Pandat output CSV file

    Args:
        files: (list) of string .xye filenames to parse, including the (relative)path to the file.
        chemical_formula: (str) chemical formula of sample material
        temperature_kelvin: (str) measurement temperature in Kelvin

    Returns: a pif chemical system from a single .xye file

    """
    # only expecting 1 file
    assert len(files) == 1

    if not chemical_formula:
        raise ValueError("chemical_formula is a required argument")
    if not temperature_kelvin:
        raise ValueError("temperature is a required argument")

    chem_sys = ChemicalSystem()
    chem_sys.properties = []
    chem_sys.chemical_formula = chemical_formula

    # Read in the whole database
    with open(files[0], 'r') as f:
        lines = f.readlines()

    # Remove metadata lines
    lines = [line for line in lines if line[0] not in ['/', '#', '*', "'"]]

    x = []
    y = []

    for line in lines:
        x_y_e = line.split()

        # If length of line is not 3, skip line
        if len(x_y_e) != 3:
            continue

        # Even if one of the numbers is not convertible to float, skip line
        try:
            floats = [float(num) for num in x_y_e]
        except ValueError:
            continue

        x.append(Scalar(value=x_y_e[0]))
        y.append(Scalar(value=x_y_e[1], uncertainty=x_y_e[2]))

    two_theta = Property(name="2$\\theta$", scalars=x, units='degrees')
    intensity = Property(name="Intensity", scalars=y,
                         conditions=[Value(name="Temperature", scalars=[Scalar(value=temperature_kelvin)], units="K")])

    chem_sys.properties.append(two_theta)
    chem_sys.properties.append(intensity)

    return chem_sys


if __name__ == "__main__":
    file_name = "LuFe2O4_700Air_hold3-00059.xye"
    chem_system = convert(files=["../test_files/" + file_name], chemical_formula="NaCl", temperature_kelvin="300")

    with open('../test_files/' + file_name.replace('.xye', '.json'), 'w') as fw:
        pif.dump(chem_system, fw, indent=4)
