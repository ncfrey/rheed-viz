import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rheedviz",
    version="0.0.1",
    description="AtomicAI-Gophers Acceleration Consortium Hackathon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncfrey/rheed-viz",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
