import time


def print_time(start):
    end = time.time() - start
    minutes = int(end / 60)
    seconds = int(end % 60)
    print('Elapsed time: ', minutes, 'min', seconds, 'sec\n')
