from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="DIO-desafio-pacote-processamento-imagem",
    version="0.0.10",
    author="SaulBL7",
    description="Processamento imagem usando Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SaulBL7/DIO-EXs/Ex4",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5'
)