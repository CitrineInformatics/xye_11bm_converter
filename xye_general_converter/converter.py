from pypif.obj import *


def convert(files=[], important_argument=None):
    """
    Convert files into a pif
    :param files: to convert
    :param important_argument: an important argument, must be provided
    :param whatever_argument: a less important argument with default 1
    :param kwargs: any other arguments
    :return: the pif produced by this conversion
    """
    # only expecting 1 file
    assert len(files) == 1

    chem_sys = ChemicalSystem()
    chem_sys.properties = []

    # Read in the whole database
    with open(files[0], 'r') as f:
        lines = f.readlines()

    # Remove metadata lines
    lines = [line for line in lines if line[0] not in ['/', '#', '*', "'"]]

    x = []
    y = []
    e = []

    for line in lines:
        print line
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

    two_theta = Property(name="2$\theta$", scalars=x, units='degrees')
    intensity = Property(name="Intensity", scalars=y)

    chem_sys.properties.append(two_theta)
    chem_sys.properties.append(intensity)




    # print len(lines)
    # print lines[2502]
    # print lines[-1:]

if __name__ == "__main__":
    convert(files=["../test_files/LuFe2O4_700Air_hold3-00059.xye"])