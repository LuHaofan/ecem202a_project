import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy import signal
def getMinTimeGap(t):
    diff = []
    prev = t[0]
    for i in range(1,len(t)):
        diff.append(t[i]-prev)
        prev = t[i]
    return min(diff)

def interpolation(t, x, start, end, n):
    tVec = t[start:end+1]
    xVec = x[start:end+1]
    f = interp1d(tVec, xVec, kind = "linear")
    tNew = np.linspace(t[start],t[end],num = n, endpoint=True)
    xNew = f(tNew)
    t = np.insert(t, end, tNew[1:-1])
    x = np.insert(x, end, xNew[1:-1])
    return t, x

def nonUniformFFT(t, x):
    assert(len(t) == len(x))
    d = round(getMinTimeGap(t),5)
    i = 1
    while (i < len(t)):
        itv = round(t[i] - t[i-1],5)
        if itv > d:
            count = int(np.ceil(itv/d)+1)
            t,x = interpolation(t, x, i-1, i, count)
            i += count-2
        i+=1
    # print(t)
    return np.fft.fft(x), t, x

def hamming(raw_sig):
    win = signal.hamming(len(raw_sig))
    return raw_sig*win

def nonUniformDFT(t, x):
    T = t[-1]
    N = len(x)
    x = hamming(x)
    dftMat = np.array([[np.exp(-2j * np.pi / T * k * t[n]) for n in range(N)] for k in range(N)])
    # print(np.round(np.dot(dftMat,dftMat.T),3))
    return np.dot(dftMat, x)

def getPeakFrequencyFromFFT(fft, fs):
    f_ax = np.linspace(0, fs, len(fft))
    fft_mag = np.abs(fft)
    return f_ax[np.argmax(fft_mag)]

def testUniformAliasing():
    tVec = np.linspace(0, 1, 100)
    freq = 30
    u_x = np.cos(2 * np.pi * freq * tVec)
    u_x_ndft = nonUniformDFT(tVec, u_x)
    # u_x_fft = np.fft.fft(u_x)
    # fs = len(tVec)/(tVec[-1]-tVec[0])
    # N = len(tVec)
    # plt.figure(figsize=(20,10))
    # plt.subplot(121)
    # plt.plot(tVec, u_x, label = 'fs = {} Hz, f = {} Hz'.format(fs, freq))
    # plt.xlabel("Time (s)")
    # plt.ylabel("Amplitude")
    # plt.legend()
    # plt.subplot(122)
    # plt.plot(np.linspace(0, fs*(N-1)/N, len(u_x_ndft)), np.abs(u_x_ndft), 
    #     label = "DFT peak at: {:.3} Hz".format(getPeakFrequencyFromFFT(np.abs(u_x_ndft),fs)))
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("Magnitude")
    # plt.legend()
    # plt.savefig('./img/test-uniform-aliasing.png')

def plotMeanSamplingRate(seed = 0):
    np.random.seed(seed)
    srate = []
    denVec = list(range(0,201,10))
    denVec[0] = 1
    for den in denVec:
        nu_itvs = np.random.rand(100)/den
        nu_t = np.cumsum(nu_itvs)
        nu_t= np.insert(nu_t, 0, 0)
        srate.append(len(nu_t)/(nu_t[-1]-nu_t[0]))
    plt.figure(figsize=(17,17))
    plt.plot(denVec,srate)
    plt.xlabel('denominator')
    plt.ylabel('sampling rate')
    plt.savefig('./img/sim-nusampling-rate-vs-denom')

def testNonUniformAliasing(seed = 0):
    freq = 200
    np.random.seed(seed)
    nu_itvs = np.random.rand(1000)/25
    nu_t = np.cumsum(nu_itvs)
    nu_t= np.insert(nu_t, 0, 0)
    T = nu_t[-1]-nu_t[0]
    N = len(nu_t)
    fs = len(nu_t)/nu_t[-1]
    nu_x = np.cos(2 * np.pi * freq * nu_t)
    nu_x_ndft = nonUniformDFT(nu_t, nu_x)
    # nu_x_fft = np.fft.fft(nu_x)
    # nu_x_nfft, t_nfft, x_nfft = nonUniformFFT(nu_t, nu_x)
    # nu_fs = len(t_nfft)/t_nfft[-1]
    plt.figure(figsize=(20,10))
    plt.subplot(121)
    plt.plot(nu_t,nu_x, label = 'f = {:} Hz, fs = {:.2f} Hz'.format(freq, fs))
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.subplot(122)
    plt.plot(1/T * np.arange(N), np.abs(nu_x_ndft), 
        label = "DFT peak at: {:.2f} Hz".format(getPeakFrequencyFromFFT(np.abs(nu_x_ndft),fs)))
    # plt.plot(1/T * np.arange(N), np.abs(nu_x_fft),
    #     label = "FFT")
    # plt.plot(np.linspace(0, nu_fs, len(nu_x_nfft)), np.abs(nu_x_nfft), 
    #     label = "FFT peak at: {:.3} Hz".format(getPeakFrequencyFromFFT(np.abs(nu_x_nfft),nu_fs)))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.savefig("./img/test-non-uniform-aliasing.png")

def simVaryingCFO(seed = 0):
    sigma = 10
    freq = 1000000
    n_samples = 2000
    np.random.seed(seed)
    var_freq = np.random.uniform(-sigma,sigma,n_samples)
    cfo = var_freq + freq
    nu_itvs = np.random.rand(n_samples)/1000000
    nu_t = np.cumsum(nu_itvs)
    nu_t[0] = 0
    T = nu_t[-1]-nu_t[0]
    N = len(nu_t)
    fs = len(nu_t)/nu_t[-1]
    nu_x = np.cos(2 * np.pi * cfo * nu_t)
    nu_x_ndft = nonUniformDFT(nu_t, nu_x)
    # nu_x_fft = np.fft.fft(nu_x)
    # nu_x_nfft, t_nfft, x_nfft = nonUniformFFT(nu_t, nu_x)
    # nu_fs = len(t_nfft)/t_nfft[-1]
    plt.figure(figsize=(20,10))
    plt.subplot(121)
    plt.plot(nu_t,nu_x, label = 'f = {:} Hz, fs = {:.2f} Hz, sigma = {}'.format(freq, fs, sigma))
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.subplot(122)
    plt.plot(1/T * np.arange(N), np.abs(nu_x_ndft), 
        label = "DFT peak at: {:.2f} Hz".format(getPeakFrequencyFromFFT(np.abs(nu_x_ndft),fs)))
    # plt.plot(1/T * np.arange(N), np.abs(nu_x_fft),
    #     label = "FFT")
    # plt.plot(np.linspace(0, nu_fs, len(nu_x_nfft)), np.abs(nu_x_nfft), 
    #     label = "FFT peak at: {:.3} Hz".format(getPeakFrequencyFromFFT(np.abs(nu_x_nfft),nu_fs)))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.savefig("./img/test-varying-cfo.png")

def testNonUniformFFT(seed = 0):
    np.random.seed(seed)
    nu_itvs = np.random.rand(100)/100
    nu_t = np.cumsum(nu_itvs)
    nu_t= np.insert(nu_t, 0, 0)
    T = nu_t[-1] - nu_t[0]
    N = len(nu_t)
    freq = 42
    nu_x = np.cos(2 * np.pi * freq * nu_t)
    u_t = np.linspace(nu_t[0], nu_t[-1], len(nu_t), endpoint=True)
    u_x = np.cos(2 * np.pi * freq * u_t)
    nu_x_fft = np.fft.fft(nu_x)
    u_x_fft = np.fft.fft(u_x)
    nu_x_nfft, t_nfft, x_nfft = nonUniformFFT(nu_t, nu_x)
    nu_x_ndft = nonUniformDFT(nu_t, nu_x)
    fs = len(u_t)/u_t[-1]
    nu_fs = len(t_nfft)/t_nfft[-1]
    
    print("Uniform Sampling Frequency:", fs)
    print("Estimated Frequency (uniform sampling fft): {}".format(getPeakFrequencyFromFFT(u_x_fft, fs)))
    print("Estimated Frequency (non-uniform sampling fft): {}".format(getPeakFrequencyFromFFT(nu_x_fft, fs)))
    print("Estimated Frequency (non-uniform sampling nfft): {}".format(getPeakFrequencyFromFFT(nu_x_nfft, nu_fs)))
    print("Estimated Frequency (non-uniform sampling ndft): {}".format(getPeakFrequencyFromFFT(nu_x_ndft, fs)))
    plt.figure(figsize=(20,10))
    plt.subplot(121)
    plt.plot(nu_t,nu_x, label = 'non-uniform sampling')
    plt.plot(u_t, u_x, label = 'uniform sampling')
    plt.plot(t_nfft, x_nfft, label = 'after interpolation')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.subplot(122)
    # plt.plot(np.linspace(0, fs, len(u_x_fft)), np.abs(u_x_fft), label = 'uniform sampling FFT')
    # plt.plot(np.linspace(0, fs, len(nu_x_fft)), np.abs(nu_x_fft), label = 'non-uniform sampling FFT')
    # plt.plot(np.linspace(0, nu_fs, len(nu_x_nfft)), np.abs(nu_x_nfft), label = 'non-uniform sampling NFFT')
    plt.plot(1/T * np.arange(N), np.abs(nu_x_ndft), label = 'non-uniform sampling NDFT')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.savefig("./img/test-non-uniform-fft.png")

if __name__ == "__main__":
    # plotMeanSamplingRate()
    # testNonUniformAliasing()
    simVaryingCFO()
    # testNonUniformFFT(2)
    # testNonUniformAliasing()
    # testUniformAliasing()
    pass
    