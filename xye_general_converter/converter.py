from pypif.obj import ChemicalSystem


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

    # Read in the whole database
    with open(files[0], 'r') as f:
        lines = f.readlines()

    print lines

if __name__ == "__main__":
    convert(files=["../test_files/LuFe2O4_700Air_hold3-00059.xye"])