from greenworld.model.types import Range

def overlaps(r1: Range, r2: Range) -> bool:
    return ((r1[0] >= r2[0] and r1[0] <= r2[1]) or
        (r1[1] >= r2[0] and r1[1] <= r2[1]) or
        (r2[0] >= r1[0] and r2[1] <= r1[1]))
