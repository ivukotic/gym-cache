import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gym_cache',
    version='1.0.1',
    install_requires=[
        'gym>=0.2.3',
        'pandas>=0.24.2',
        'scikit-learn>=0.22.1'
    ],
    scripts=['unit.py'],
    author="Ilija Vukotic",
    author_email="ivukotic@cern.ch",
    description="gym environment simulating file cache.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ivukotic/gym_cache",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
