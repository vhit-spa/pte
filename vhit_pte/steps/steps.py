'''VHIT step library for Behave'''

from behave import step
from typing import Any
from time import sleep, time_ns
from vhit_pte.api import MTMInterface

MAX_TIME = 1 #Second
MILLI_TO_S = 1000.0
MICRO_TO_S = 1000000.0
MICRO_TO_MILLI = 1000.0

#Delay
@step('wait at least for {delay:d} microsecond(s)')
def wait(context, delay: int):
    sleep(delay/MILLI_TO_S)

@step('wait at least for {ticks:d} tick(s) (tick_factor={factor:f} [us/ticks])')
def wait(context, ticks: int, factor: float):
    sleep(ticks*factor/MICRO_TO_S)

#Read signal steps
@step('the signal {sgn:str} must be equal to {val}')
def check_sgn_val(context,sgn: str, val: Any):
    mtm: MTMInterface = context.mtm
    r_val = mtm.sgn_read(sgn)
    assert r_val==val, \
        "Error, the signal {sgn} real value is {r_val} instead of {val}"

@step('the signal {sgn:str} must be within the range {l_val} and {u_val} (unit:{u})')
def check_sgn_val_tol(context,sgn: str, l_val: Any, u_val: Any):
    mtm: MTMInterface = context.mtm
    r_val = mtm.sgn_read(sgn)
    assert r_val>=l_val and r_val<=u_val, \
        "Error, the signal {sgn} real value {r_val} is not within the range [{l_val}, {u_val}]"

@step('read signal {sgn:str} at tick {tick:int} (tick_factor={factor:f} [us/ticks])')
def scheduled_read(context, sgn:str, tick:int, factor:float):
    mtm: MTMInterface = context.mtm

    #Measure the reading time of the tick
    t_s = time_ns()
    r_tick = mtm.sgn_read(context.tick_sgn)
    dt = time_ns() - t_s

    # sleep time
    #   |   Trigger tick        
    #   |       |   Start tick   
    #   |       |       |   Tick factor   
    #   |       |       |       |       Read time
    #   |       |       |       |           |       
    sleep_us =(tick - r_tick)*factor - dt*MICRO_TO_MILLI

    assert sleep_us>0, "Error requeste is tick has elapsed"
    sleep(sleep_us/MICRO_TO_S)




#Set signal steps
@step('set the signal {sgn:str} equal to {val}')
def set_sgn_val(context, sgn:str, val:Any):
    mtm: MTMInterface = context.mtm
    mtm.sgn_write(sgn,val)

@step('set the signal {sgn:str} equal to {val} (and check it)')
def set_sgn_val_check(context, sgn:str, val:Any):
    context.execute_steps(
        f'''
        Then set the signal {sgn} equal to {val}
        Then the signal {sgn} must be equal to {val}
        '''
        )


    