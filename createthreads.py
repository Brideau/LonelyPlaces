from threading import Thread


def create_threads(functionToThread, grid, poi, lock,
                   increment=0.2697118131790, numthreads=10):
    """ Splits the grid into n threads to do simultaneous API calls """
    threads = []
    for i in range(numthreads):
        gridpoints = grid[i::numthreads]
        thread = Thread(target=process_grid_sample,
                        args=(functionToThread, gridpoints, poi, lock,
                              increment))
        threads.append(thread)

    # Start each thread, and wait for them to finish before continuing
    [t.start() for t in threads]
    [t.join() for t in threads]


def process_grid_sample(functionToThread, grid_sample, poi, lock, increment):
    """ Given a  sample of the grid, this
    calculates the nearest place to each point"""
    for gridpoint in grid_sample:
        functionToThread(gridpoint[0], gridpoint[1], poi, lock, increment)
