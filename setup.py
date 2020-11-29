from setuptools import setup, find_packages

long_description = open("README.md").read()

setup(
        name='iotaescrow',
        version='0.0.2.8',
        description='Basic escrow utility using IOTA',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author_email='william.wyatt@cgu.edu',
        url='https://github.com/Tsangares/iotaescrow',
        include_package_data=True,
        packages=find_packages(),
        install_requires=[
            'pyota'
            ],
        entry_points={
            'console_scripts': [
                'iotaescrow = iotaescrow.escrow:main',
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
)
