
# These variables are global for easy module-wide access
CONNECTION = None
REPORT = None

# This variable collects all the algorithm logic methods
RULES = []

# Sets up a new report instance
def new_report():
    # pylint: disable-next=global-statement
    global REPORT
    REPORT = []

# Returns the current report to another module
def get_report():
    return REPORT

# Adds a pair to the current report
def add_to_report(pair):
    REPORT.append(pair)

# Sets the current SQLAlchemy connection
def set_connection(con):
    # pylint: disable-next=global-statement
    global CONNECTION
    CONNECTION = con

# Returns the current SQLAlchemy connection
def get_connection():
    return CONNECTION

# Returns the list of rules to another module
def get_rules():
    return RULES

# Returns true if the two intervals overlap or touch at all
def overlaps(a, b):
    return min(a.upper, b.upper) - max(a.lower, b.lower) >= 0

def reduce_intervals(plant1, plant2, field1, field2):
    return (getattr(plant1[field1], field2) if plant1[field1] else 0) + (getattr(plant2[field1], field2) if plant2[field1] else 0)

# Adds any valid information to the current report
def rule(func):
    def wrapper(plant1, plant2):
        pair = func(plant1, plant2)
        if pair:
            interval, reason = pair
            if interval:
                dist1, dist2 = interval
                interval = (round(float(min(dist1, dist2)), 3), round(float(max(dist1, dist2)), 3))
            add_to_report((interval, reason))
    RULES.append(wrapper)
    return wrapper

# Repeats the decorated function with the tested plants reversed (if nothing was returned the first time)
def mirrored(func):
    def wrapper(plant1, plant2):
        return func(plant1, plant2) or func(plant2, plant1)
    return wrapper

# Does not run the decorated function if the tested plants do not have certain fields
def ensure(both = [], fields1 = [], fields2 = []):
    def decorate_wrapper(func):
        def func_wrapper(plant1, plant2):
            for k in both + fields1:
                if plant1[k] is None:
                    return None
            for k in both + fields2:
                if plant2[k] is None:
                    return None
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
        return None
    return wrapper