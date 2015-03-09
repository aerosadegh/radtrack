import scipy
import scipy.fftpack
import numpy as np

def FourT(signal,t, Np):
    FFT_C=scipy.fft(signal)*2/Np
    print np.shape(FFT_C)
    freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
    return (FFT_C, freqs)
