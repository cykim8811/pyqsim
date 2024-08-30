
from setuptools import setup, find_packages

setup(
    name='pyqsim',
    version='0.0.1',
    description='Interactive quantum computing simulator',
    author='Kim Changyeon',
    author_email='cykim8811@snu.ac.kr',
    packages=find_packages(include=['pyqsim']),
    install_requires=[
        'cirq'
    ]
)
