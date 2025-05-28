from setuptools import setup

from tecscipyModbusTCP import constants

with open("README.rst") as f:
    readme = f.read()

setup(
    name="tecscipyModbusTCP",
    version=constants.VERSION,
    description="A simple Modbus/TCP library for Python",
    long_description=readme,
    author="Loic Lefebvre",
    author_email="loic.celine@free.fr",
    license="MIT",
    url="https://github.com/Monitoramento-Usinas-STEMIS/pyModbusTCP",
    packages=["tecscipyModbusTCP"],
    platforms="any",
)
