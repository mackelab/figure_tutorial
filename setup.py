from setuptools import find_packages, setup

REQUIRED = [
    "svgutils==0.3.1",
    "invoke",
    "jupyterlab",
    "matplotlib",
]

setup(
    name="figure_tutorial",
    python_requires=">=3.6.0",
    packages=find_packages(),
    install_requires=REQUIRED,
)
