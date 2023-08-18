from setuptools import setup , find_packages
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path : str) -> List[str]:
    """
    this function will return the list of requirements
    """
    requirements = list()
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n" , "")for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name = "MLPRO",
    version="0.0.1",
    author="Bygetx",
    author_email="mehrezaymen0@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements("requirements.txt")


)