import numpy as np
import matplotlib.pyplot as plt
def plotTimeStamp(tsVec, path, systsVec = []):
    plt.figure()
    norm_tsVec = np.array(tsVec)-tsVec[0]
    if len(systsVec) == 0:
        plt.plot(norm_tsVec)
        plt.xlabel('packet id')
        plt.ylabel('timestamp')
        plt.savefig(path)   
    else:
        plt.plot(systsVec, norm_tsVec)
        plt.xlabel('Time (s)')
        plt.ylabel('timestamp')
        plt.savefig(path)   

def plotRSSI(rssiVec, path, systsVec = []):
    plt.figure()
    if len(systsVec) == 0:
        plt.plot(rssiVec)
        plt.ylabel("RSSI (dB)")
        plt.xlabel("packet id")
        plt.savefig(path)
    else:
        plt.plot(systsVec, rssiVec)
        plt.ylabel("RSSI (dB)")
        plt.xlabel("Time (s)")
        plt.savefig(path)

def plotCSI(ampMat, phsMat, n_subcarriers, path, systsVec = []):
    plt.figure(figsize=(30,10))
    if len(systsVec) == 0:
        plt.subplot(121)
        for i in range(n_subcarriers):
            plt.plot(ampMat[i,:])
        plt.xlabel('sample id')
        plt.ylabel('CSI Amplitude')
        plt.subplot(122)
        for i in range(n_subcarriers):
            plt.plot(phsMat[i,:])
        plt.xlabel('sample id')
        plt.ylabel('CSI Phase')
        plt.savefig(path)
    else:
        plt.subplot(121)
        for i in range(n_subcarriers):
            plt.plot(systsVec,ampMat[i,:])
        plt.xlabel('Time (s)')
        plt.ylabel('CSI Amplitude')
        plt.subplot(122)
        for i in range(n_subcarriers):
            plt.plot(systsVec,phsMat[i,:])
        plt.xlabel('Time (s)')
        plt.ylabel('CSI Phase')
        plt.savefig(path)

def plotCSIPhaseByIdx(phsMat, sc_idx1, sc_idx2, path, systsVec):
    plt.figure(figsize=(20,10))
    plt.plot(systsVec, phsMat[sc_idx1,:],label="subcarrier {}".format(sc_idx1))
    plt.plot(systsVec, phsMat[sc_idx2,:],label="subcarrier {}".format(sc_idx2))
    plt.xlabel("Time (s)")
    plt.ylabel("CSI Phase")
    plt.legend()
    plt.savefig(path.format(sc_idx1, sc_idx2))

def plotTsDiff(tsDiffVec,path, systsVec = []):
    plt.figure()
    if (len(systsVec) == 0):
        plt.plot(tsDiffVec)
        plt.xlabel('packet id')
        plt.ylabel('cycle differences')
        plt.savefig(path)
    else:
        plt.plot(systsVec, tsDiffVec)
        plt.xlabel('Time (s)')
        plt.ylabel('cycle differences')
        plt.savefig(path)

def plotMaxPhaseDiffAcrossSubcarriers(phsDiffVec, path, systsVec = []):
    plt.figure()
    if (len(systsVec) == 0):
        plt.plot(phsDiffVec)
        plt.xlabel('packet id')
        plt.ylabel('phase difference')
        plt.yticks([0,2*np.pi], ['0', '2$\pi$'])
        plt.savefig(path)
    else:
        plt.plot(systsVec, phsDiffVec)
        plt.xlabel('Time (s)')
        plt.ylabel('phase difference')
        plt.yticks([0,2*np.pi], ['0', '2$\pi$'])
        plt.savefig(path)

def plotPhaseBySubcarrierIdx(phsMat, idx_1, idx_2, systsVec, path):
    phsVec_1 = phsMat[idx_1,:]
    phsVec_2 = phsMat[idx_2,:]
    plt.figure()
    plt.plot(systsVec, phsVec_1, label = "subcarrier {}".format(idx_1))
    plt.plot(systsVec, phsVec_2, label = "subcarrier {}".format(idx_2))
    plt.plot(systsVec, phsVec_1-phsVec_2, label = "diff", zorder = 100)
    plt.xlabel("Time (s)")
    plt.ylabel("Phase")
    plt.legend()
    plt.savefig(path)

def plotPhaseVersusSubCarriers(phsMat, pkt_id):
    phsVec = phsMat[:,pkt_id]
    plt.figure()
    plt.scatter(np.arange(-32,32),phsVec)
    plt.xlabel("Subcarrier Index")
    plt.ylabel("Phase")
    xticks = [str(i) for i in range(0,31,4)] + [str(i) for i in range(-32,0,4)]
    plt.xticks(np.arange(-32,32,4),xticks)
    plt.yticks([-np.pi,0,np.pi], ['-$\pi$', '0', '$\pi$'])
    plt.title('Packet id:{}'.format(pkt_id))
    plt.savefig('./img/phase-versus-subcarrier')

def plotCosinePhase(phsMat, sc_idx, systsVec):
    phsVec = phsMat[sc_idx,:]
    cos_phs = np.cos(phsVec)
    plt.figure()
    plt.plot(systsVec, cos_phs)
    plt.savefig('./img/cosine_phase')

def plotThroughput():
    tpVec = [1.37,8.92,16.69,62.64,140.57,215.05,227.58,226.18]
    bwVec = [10,100,1000,10000,50000,100000,200000,500000]
    plt.figure()
    plt.scatter(bwVec,tpVec)
    plt.xscale('log')
    plt.xlim(1,1e6)
    plt.xlabel('iPerf Bandwidth (Kbits/s)')
    plt.ylabel('# packets received')
    plt.savefig('./img/throughput.png')