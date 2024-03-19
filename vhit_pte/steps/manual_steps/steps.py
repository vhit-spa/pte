from behave import step

@step(u'{x:l}')
def generic_manual(context,x):
    err =''
    res = input(">Is the test step passed[Y/N]?\n")
    if res not in ('Y','y'):
        err = input(">Please describe the error:\n")
        res = False
    assert res != False, err