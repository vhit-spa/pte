from setuptools import setup, find_packages

#Vars
ROOT='vhit_pte'

with open('requirements.txt','r') as f:
    rqs = f.read().splitlines()

#Setup call
setup(
    # Default parameters
    name='vhit-pte',
    version='0.1.0',
    description=__doc__,

    # Package info
    packages=[ROOT] + [f'{ROOT}.{pkg}' for pkg in find_packages(ROOT)],

    # Requirements
    install_requires=rqs,

)