from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="LRFutils",
    version = "0.0.14",
    description = 'Just a custom library to share with some colleagues. Use it at your own risks.',
    author = 'Leirof',
    author_email = 'vince.lrf@gmail.com',
    url = 'https://github.com/LeiRoF/Utils',
    readme = "README.md",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['LRFutils'],
    install_requires=requirements,
    python_requires='>=3.10.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers'
    ]
)