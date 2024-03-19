from setuptools import setup, find_packages
from vhit_pte import __version__

#Vars
ROOT='vhit_pte'

with open('requirements.txt','r') as f:
    rqs = f.read().splitlines()

#Setup call
setup(
    # Default parameters
    author="Camagni Matteo",
    author_email='external.matteo.camagni@vhit-weifu.com',
    name='vhit-pte',
    version=__version__.VERSION,
    description=__doc__,

    # Package info
    packages=[ROOT] + [f'{ROOT}.{pkg}' for pkg in find_packages(ROOT)],

    # Requirements
    install_requires=rqs,

    #Entry point -> cmd line tools
    entry_points={
        'console_scripts': [
            'vhit_behave = vhit_pte.launcher:main',
        ]
    },

    # #Pack data
    # package_data={'vhit_pte' :['vhit_pte/steps/manual_steps/*']},
    # include_package_data=True,

)