from workloads import WORKLOADS

def run_task(fn_name: str, arg):
    return WORKLOADS[fn_name](arg)