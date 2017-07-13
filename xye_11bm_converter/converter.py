from pypif.obj import *
from pypif import pif


def convert(files=[], sample_id=None, chemical_formula=None, temperature_kelvin=None):
    """
    Ingest .xye files from the 11-BM beamline instrument at APS

    Args:
        files: (list) of string .xye filenames to parse, including the (relative)path to the file.
        sample_id: (str) ID of sample being measured.
        chemical_formula: (str) chemical formula of sample material.
        temperature_kelvin: (str) measurement temperature in Kelvin.

    Returns: a pif chemical system from a single .xye file

    """
    # only expecting 1 file
    assert len(files) == 1

    if not sample_id:
        raise ValueError("sample_id is a required argument")
    if not chemical_formula:
        raise ValueError("chemical_formula is a required argument")

    chem_sys = ChemicalSystem()
    chem_sys.ids = [Id(name="Sample ID", value=sample_id)]
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

    intensity = Property(name="Intensity", scalars=y,
                         conditions=[Value(name="2$\\theta$", scalars=x, units="degrees")])
    chem_sys.properties.append(intensity)

    if temperature_kelvin:
        temperature = Property(name="Temperature", scalars=[Scalar(value=temperature_kelvin)], units="K")
        chem_sys.properties.append(temperature)

    return chem_sys


if __name__ == "__main__":
    file_name = "LuFe2O4_700Air_hold3-00059.xye"
    # file_name = "11bmb_2144_AA0037_YbFeO_red.xye"
    # file_name = "NOM_LuFe2O4_Ex_situ_20C-5.xye"
    # file_name = "PG3_27954-3.xye"
    chem_system = convert(files=["../test_files/" + file_name], sample_id="001",
                          chemical_formula="NaCl", temperature_kelvin="300")

    with open('../test_files/' + file_name.replace('.xye', '.json'), 'w') as fw:
        pif.dump(chem_system, fw, indent=4)
