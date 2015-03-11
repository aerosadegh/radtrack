import numpy as np

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    s = np.convolve(interval, window, 'valid')
    return s
    #smoothed = np.convolve(interval, np.ones(window_size)/window_size)
    #return smoothed

