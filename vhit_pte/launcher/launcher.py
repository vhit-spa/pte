"""
Official VHIT Python Test Environment

Created By: Camagni Matteo
Contact: external.matteo.camagni@vhit-weifu.com
"""
import os
import sys
import yaml
import platform
import argparse
from pathlib import Path
from ..__version__ import VERSION
from shutil import copytree, rmtree
from behave.__main__ import main as behave_ep

__PTE_NAME__ = 'vhit_pte'
EPILOG = '''
For further detail visit https://github.com/vhit-spa/pte
'''
HTML_PRETTY_ROOT = 'behave.additional-info.{key}={value}'

CHOICES = ['auto', 'manual']

# --- PARSER ---
def is_existing_path(value) -> Path:
    '''argparser custom type checker'''
    pt = Path(value)
    assert pt.exists(), f'Error: {value} path does not exists!'

    return pt

def parse_args() -> dict:
    '''Command line parser'''

    d: dict = {
        'project': None,
        'test_camp': None,
        'sw_version': None,
        'req_version': None,
        'mode': None,
        'symtable_path': None,
    }

    p: argparse.ArgumentParser = argparse.ArgumentParser(
                    description=__doc__,
                    epilog=EPILOG
                    )
    
    # First group of input for the config file
    group1 = p.add_mutually_exclusive_group()
    group1.add_argument("-c", "--conf_file_path", type=is_existing_path, help="Type a path of a yaml config file")
    
    # Second group of input for the explicit inputs
    group2 = p.add_mutually_exclusive_group()
    group2.add_argument("-p", "--project", type=str, help="The project name")
    group2.add_argument("-k", "--test_camp", type=str, help="The test campaign name")
    group2.add_argument("-s", "--sw_version", type=str, help="The commit ID of the tested software")
    group2.add_argument("-r", "--req_version", type=str, help="The baseline ID of the requirement under verification")
    group2.add_argument("-m", "--mode", choices=CHOICES, help="One of the following launch modes:%s" % (f'\n-{x}' for x in CHOICES))
    group2.add_argument("-t", "--symtable_path", type=str, help="The path of the Symbol Table fil;e (.map)")

    #Parse
    cmds: argparse.Namespace = p.parse_args()

    if getattr(cmds,'conf_file_path',None) != None:
        #In case it's provided the config yaml import it
        with cmds.conf_file_path.open() as f:
            m = yaml.safe_load(f)
            assert d.keys() == m.keys(),\
                  "Error: yaml keys mismatch.\nRequired keys:\n- %s" % ('\n- '.join(d.keys()))
            assert m["mode"] in CHOICES,\
                  "Error: the execution mode <%s> is wrong. Choices:\n- %s" % (d["mode"],'\n- '.join(CHOICES))
            d = m
    else:
        #Otherwise use the args to update the dictionary
        for k in d.keys():
            d[k] = getattr(cmds,k)

    #Check the path and update it
    d["symtable_path"] = is_existing_path(d["symtable_path"])

    return d

# --- BEHAVE ARGS ---
def behave_default_args(args: dict) -> list:
    res: list = []

    #Add the formatter
    res += ['-f','behave_html_pretty_formatter:PrettyHTMLFormatter']

    #Add the output report
    res += ['-o','%s_sqt_report.html' % (args['test_camp'])]

    #Manual testing setup
    if args['mode'] == 'manual':
        res += ['--no-capture','--stage', 'manual']

    return res

def behave_pretty_formatter_cfg(args: dict) -> list:
    cfg: list = []
    
    #Add tester identity
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='Tester',
        value= os.getlogin(),
    )]

    #Add project identity
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='Project',
        value= args['project'],
    )]

    #Add test campaign identity
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='Test Campaign',
        value= args['test_camp'],
    )]

    #Add requirement baseline
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='Requirement baseline',
        value= args['req_version'],
    )]

    #Add execution mode
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='Execution mode',
        value= args['mode'],
    )]

    #Add SWUT identity
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='Software Under Test Commit ID',
        value= args['sw_version'],
    )]

    #Add test engine OS
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='Test Machine OS',
        value= platform.platform(),
    )]

    #Add python version
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='Python Version',
        value= sys.version,
    )]

    #Add PTE version
    cfg += ['-D',HTML_PRETTY_ROOT.format(
        key='PTE Version',
        value= VERSION,
    )]       

    return cfg

# --- MANUAL MODE ---
def create_temp_manual_steps(args:dict):
    if args['mode'] == 'manual':
        copytree(
            src=str(Path(__file__).parents[1] / 'steps' / 'manual_steps' ),
            dst=str(Path(os.getcwd()) / 'manual_steps'),
            dirs_exist_ok=True,
        )

def delete_temp_manual_steps(args:dict):
    if args['mode'] == 'manual':
        rmtree(f"{os.getcwd()}\\manual_steps")

# --- MAIN ---
def main() -> None:
    args: dict = parse_args()
    cmd_args: list = \
        behave_default_args(args) + \
        behave_pretty_formatter_cfg(args)
    try:
        create_temp_manual_steps(args)
        behave_ep(cmd_args)
    except:
        pass
    delete_temp_manual_steps(args)

if __name__ == '__main__':
    sys.exit(main())

