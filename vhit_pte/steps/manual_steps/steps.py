from datetime import datetime
from behave import step

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Globals
_is_header_printed: str = False 
_last_feature: str = None    
_last_scenario: str = None

#Print functions
def print_step_info(feature: str, scenario: str, step: str, step_descr: str) -> None:
    global _last_feature
    global _last_scenario

    res = ''

    #Print feature formatted
    if _last_feature != feature:
        _last_feature = feature
        res += "[FEATURE]: %s\n" % feature
    
    #Print scenario formatted
    if _last_scenario != scenario:
        _last_scenario = scenario
        res += "  ├─[SCENARIO]: %s\n" % scenario

    #Print test step formatted
    res += "  |  ├─[STEP]: %s" % step
    if step_descr:
        res += "\n  |  |  | %s%s%s" % (bcolors.HEADER,str(step_descr),bcolors.ENDC)

    print(res)

def print_header()->None:
    global _is_header_printed

    if not _is_header_printed:
        now = datetime.now().strftime("%H:%M:%S")
        print("-"*8+f"Test execution started at: {now}"+"-"*8)
        _is_header_printed = True

#Main manual step implementation
@step(u'{x}')
def generic_manual(context,x):
    err =''

    #Print to standard output step informations
    print_header()
    print_step_info(
        feature = str(context.feature), 
        scenario = str(context.scenario), 
        step = str(x),
        step_descr = context.text,
    )

    #Request user to insert infos
    res = input("  |  |  |> %sIs the test step passed [Y/N]?%s\n  |  |  |> " % (bcolors.OKCYAN,bcolors.ENDC))
    if res not in ('Y','y'):
        err = input("  |  |  |> %sPlease describe the error:%s\n  |  |  |> " % (bcolors.FAIL,bcolors.ENDC))
        res = False

    #Assert the result
    assert res != False, err