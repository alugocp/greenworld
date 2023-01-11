
# This variable is global for easy module-wide access
report = None

# This variable collects all the algorithm logic methods
rules = []

# Sets up a new report instance
def new_report():
    global report
    report = []

# Returns the current report to another module
def get_report():
    return report

# Returns the list of rules to another module
def get_rules():
    return rules

# Adds any valid information to the current report
def rule(func):
    def wrapper(plant1, plant2):
        pair = func(plant1, plant2)
        if pair:
            report.append(pair)
    rules.append(wrapper)
    return wrapper

# Repeats the decorated function with the tested plants reversed
def mirrored(func):
    def wrapper(plant1, plant2):
        return func(plant1, plant2) or func(plant2, plant1)
    return wrapper

# Does not run the decorated function if the tested plants do not have certain fields
def ensure(both = [], fields1 = [], fields2 = []):
    def decorate_wrapper(func):
        def func_wrapper(plant1, plant2):
            for k in both + fields1:
                if plant1[k] == None:
                    return
            for k in both + fields2:
                if plant2[k] == None:
                    return
            return func(plant1, plant2)
        return func_wrapper
    return decorate_wrapper

# Runs the decorated function with the taller of the tested plants first
def taller_first(func):
    def wrapper(plant1, plant2):
        if plant1.height and ((not plant2.height) or plant1.height > plant2.height):
            return func(plant1, plant2)
        if plant2.height and ((not plant1.height) or plant2.height > plant1.height):
            return func(plant2, plant1)
    return wrapper