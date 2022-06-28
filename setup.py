from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='LRFutils',
    url='https://github.com/LeiRoF/Utils',
    author='Vincent Foriel',
    author_email='vince.lrf@gmail.com',
    install_requires=['numpy'],
    version='0.4',
    description="Just a custom library to share with some colleagues.",
    long_description=open('README.md').read(),
)

setup(
    name="LRFutils",
    version = "0.0.5",
    description = 'Just a custom library to share with some colleagues. Use it at your own risks.',
    author = 'ZRunner',
    author_email = 'vince.lrf@gmail.com',
    url = 'https://github.com/LeiRoF/Utils',
    packages=['LRFutils'],
    install_requires=[
        'gitpython',
        'numpy',
        'matplotlib',
        'scipy',
        'regex'
        ],
    python_requires='>3.9.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers'
    ]
)