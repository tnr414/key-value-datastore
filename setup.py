import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="keyvaluestore-tnr414", # Replace with your own username
    version="0.0.1",
    author="Tanveer Azam Ansari",
    author_email="tnr414@gmail.com",
    description="A key-value datastore based on local file system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tnr414/key-value-datastore.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
