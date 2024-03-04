from setuptools import setup, find_packages

#Vars
ROOT='src'

with open('requirements.txt') as f:
    rqs = f.read().splitlines()

#Setup call
setup(
    # Default parameters
    name='vhit_pte',
    version='0.1.0',
    description=__doc__,

    # Package info
    packages=[ROOT] + [f'{ROOT}.{pkg}' for pkg in find_packages(ROOT)],

    # Requirements
    install_requires=rqs,

)