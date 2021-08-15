import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setuptools.setup(
    name="rtpt",
    version="0.0.4",
    author="Quentin Delfosse, Patrick Schramowski, Steven Lang, Johannes Czech",
    author_email="quentin.delfosse@cs.tu-darmstadt.de",
    description="Remaining Time to Process Title",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ml-research/rtpt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
)
