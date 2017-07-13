from setuptools import setup, find_packages

setup(name='xye_11bm_converter',
    version='0.0.1',
    url='https://github.com/CitrineInformatics/xye_11bm_converter',
    description='This converter ingests .xye files generated specifically from the 11-BM beamline instrument for powder diffraction.',
    author='Saurabh Bajaj',
    author_email='saurabh@citrine.io',
    packages=find_packages(),
    install_requires=[
        'pypif',
    ],
    entry_points={
        'citrine.dice.converter': [
            'xye_11bm = xye_11bm_converter.converter',
        ],
    },
)
