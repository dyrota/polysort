from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="polysort",
    version="0.1.0",
    description="A collection of sorting algorithms with a consistent SortProblem interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Chase Taylor",
    url="https://github.com/dyrota/polysort",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
