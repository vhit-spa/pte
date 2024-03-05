'''VHIT step library for Behave'''

from behave import step

@step('the signal {sgn:str} is read')
def read_step(context,sgn: str):
    pass