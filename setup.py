import setuptools
import rsgt


# Read Readme file to get long description
with open('README.md', 'r') as fp:
    long_description = fp.read()

# Package configuration
setuptools.setup(
    name='rsgt',
    version=rsgt.__version__,
    description='Implementaton of random smooth grayvalue transformations for training grayvalue independent neural networks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nlessmann/rsgt",
    packages=['rsgt'],
    python_requires='>=2.6',
    install_requires=['numpy'],
    extras_require={'dev': ['pytest']},
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
