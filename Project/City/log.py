import logging

log = logging.getLogger("City")

def logfunc(start=None, end=None, lvl="INFO"):
    def logfunc(func):
        nonlocal start, end
        if not start:
            start = "Function Start: {}.{}".format(func.__module__, func.__name__)
        if not end:
            end = "Function Finished: {}.{}".format(func.__module__, func.__name__)
        def logfunc(*args, **kwargs):
            log.log(getattr(logging, lvl.upper()), start)
            res = func(*args, **kwargs)
            log.log(getattr(logging, lvl.upper()), end)
            return res
        return logfunc
    return logfunc
