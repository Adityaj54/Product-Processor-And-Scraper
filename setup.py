#!/usr/bin/env python3
"""
Setup script for the product_processor package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="product_processor",
    version="0.1.0",
    author="Your Name",
    author_email="aditya.aj5t4@gmail.com",
    description="A Python application for processing product data from JSON files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/product-processor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "product-processor=product_processor.main:main",
        ],
    },
)