import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import diff
from utils import parse, plot, dsp

fname = "./logs/pkt-rate-vs-bw-200M.log"

def motionDetector(ampMat, tvec):
    res = []
    n_sc = 4
    for k in range(ampMat.shape[0]-n_sc, ampMat.shape[0]):
        sc = ampMat[k,:]
        # Normalization
        mu = np.mean(sc)
        std = np.std(sc)
        if std == 0:
            continue
        sc = (sc-mu)/std
        # Remove outliers
        thd = 50
        median = np.median(sc)
        for i in range(len(sc)):
            if sc[i] > thd:
                sc[i] = median
        
        # Moving average
        win = 200
        filt = np.array([1/win]*win)
        s_sc = np.convolve(sc, filt, 'same')
        if len(res) == 0:
            res = s_sc
        else:
            res += s_sc
    plt.figure()
    plt.plot(tvec, res/n_sc, label = 'Subcarrier')
    plt.hlines(0.5, np.min(tvec), np.max(tvec), linestyles='dashed', label = 'threshold')
    plt.xlabel("Time (s)")
    plt.ylabel("Normalized CSI Amplitude")
    plt.legend()
    plt.savefig('./img/motion-detector.png')


def testWiFiSniffer():
    # rmHdrFtr(w_traffic_fname)
    with open(fname, 'r') as f:
        raw = f.readlines()
        n_samples = int(len(raw)/2)
        tsVec = []
        # rssiVec = []
        ampMat = []
        phsMat = []
        # systsVec = []
        for i in range(n_samples):
            tsVec.append(parse.parseTimeStamp(raw[i*2])) 
            # systsVec.append(parse.parseTimeStamp(raw[i*6+2])/1e6)
            # rssiVec.append(parse.parseRSSI(raw[i*6+3]))
            amp, phs = parse.parseCSI(raw[i*2+1])
            if len(amp) == 0 or len(phs) == 0:
                continue
            ampMat.append(amp)
            phsMat.append(phs)
        
        ampMat = np.array(ampMat).T
        phsMat = np.array(phsMat).T
        # ampMat, phsMat shapes: (64, 768) at this point
        # plotCSIPhaseByIdx(phsMat,2,52, "./img/subcarrier-phase-{}-{}.png",systsVec)
        tsDiffVec = parse.getCycleDiffAmongPkts(tsVec)
        tVec = parse.getTimeFromCycleCount(tsVec)
        # phsDiffVec = getMaxPhaseDiffAcrossSubcarriers(phsMat)
        # plotPhaseVersusSubCarriers(phsMat,68)
        # plotCosinePhase(phsMat, 2, systsVec)
        # plotPhaseBySubcarrierIdx(phsMat, 0, 1, systsVec, "./img/phase-difference-two-subcarriers.png")
        # plotMaxPhaseDiffAcrossSubcarriers(phsDiffVec,"./img/phase-difference-among-subcarriers.png", systsVec)
        # plot.plotTimeStamp(tsVec, "./img/timestamp-50M.png")
        # plotRSSI(rssiVec,"./img/RSSI-w-traffic.png", systsVec)
        # plot.plotCSI(ampMat,phsMat, 64, "./img/CSI-w-traffic.png",systsVec=tVec)
        # plot.plotTsDiff(tsDiffVec, "./img/ts-diff-w-traffic.png")
        # plot.plotThroughput()
        return ampMat, phsMat, tVec
        

    
def testNFFT(tVec):
    tVec = tVec - tVec[0]
    T = tVec[-1]-tVec[0]
    N = len(tVec)
    freq = 60
    nu_x = np.cos(2 * np.pi * freq * tVec)
    nu_x_ndft = dsp.nonUniformDFT(tVec, nu_x)
    nu_x_fft = np.fft.fft(nu_x)
    fs = len(tVec)/(tVec[-1]-tVec[0])
    # print(fs)
    plt.figure(figsize=(20,10))
    plt.subplot(121)
    plt.plot(tVec, nu_x)
    plt.subplot(122)
    plt.plot(1/T * np.arange(N), np.abs(nu_x_ndft), label = 'non-uniform sampling NDFT')
    plt.plot(1/T * np.arange(N), np.abs(nu_x_fft), label = 'non-uniform sampling FFT')
    plt.legend()
    # plt.plot(np.abs(nu_x_ndft))
    plt.savefig('./img/fake-single-freq-ndft.png')

def estimateCFO(ampMat, phsMat, tVec):
    dura = 5
    t_start = 13
    sc_idx = 10
    start, end = parse.getSamples(t_start, dura, tVec)
    s_tVec = np.array(tVec[start:end])
    # s_tVec = s_tVec - s_tVec[0]
    # testNFFT(s_tVec)
    s_phsMat = phsMat[sc_idx,start:end]
    s_ampMat = ampMat[:,start:end]
    scVar = parse.getAmplitudeVariance(s_ampMat)
    plt.figure()
    plt.plot(scVar)
    plt.xlabel("Subcarrier Index")
    plt.ylabel("Var(Amplitude)")
    plt.savefig("./img/amplitude-variance.png")
    # fs = len(s_tVec)/(s_tVec[-1]-s_tVec[0])
    # print("sampling frequency before interpolation:", fs)
    # sig = np.cos(s_phsMat)
    # # nu_x_nfft, t_nfft, x_nfft = dsp.nonUniformFFT(s_tVec, sig)
    # nu_x_ndft = dsp.nonUniformDFT(s_tVec, sig)
    # nu_x_fft = np.fft.fft(sig)
    # # nu_fs = len(t_nfft)/(t_nfft[-1]-t_nfft[0])
    # # print("sampling frequency after interpolation:",nu_fs)
    # plt.figure(figsize=(20,10))
    # plt.subplot(121)
    # plt.plot(s_tVec, sig, label = 'before interpolation')
    # # plt.plot(t_nfft, x_nfft, label = 'after interpolation')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Amplitude')
    # plt.legend()
    # plt.subplot(122)
    # # plt.plot(np.linspace(0, nu_fs, len(nu_x_nfft)), np.abs(nu_x_nfft), label = 'non-uniform sampling NFFT')
    # plt.plot(np.linspace(0, fs, len(nu_x_ndft)), np.abs(nu_x_ndft), label = 'non-uniform sampling NDFT')
    # plt.plot(np.linspace(0, fs, len(nu_x_fft)), np.abs(nu_x_fft), label = 'non-uniform sampling FFT')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Magnitude')
    # plt.legend()
    # plt.savefig("./img/nfft-csi-phase.png")

if __name__ == "__main__":
    ampMat, phsMat, tVec = testWiFiSniffer()
    # estimateCFO(ampMat, phsMat, tVec)
    motionDetector(ampMat, tVec)
    
