import time


def time_record(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        return_value = f(*args, **kwargs)
        print('----\n'
              'func name: {}\n'
              'start time: {}\n'
              'used time: {}\n'
              '----'.format(f.__name__, t, time.time()-t))
        return return_value
    wrapper.__name__ = f.__name__
    return wrapper




