import numpy as np
import matplotlib.pyplot as plt

def rmHdrFtr(fname):
    text = ''
    hdr_bnd = 0
    ftr_bnd = 0
    with open(fname,'r') as f:
        text = f.read()
        hdr_bnd = text.find("<")
        ftr_bnd = text.rfind(">")
    with open(fname, 'w') as f:
        f.write(text[hdr_bnd:ftr_bnd+1])

def parseTimeStamp(ts):
    start = ts.find(">")
    end = ts.find("</")
    return int(ts[start+1:end])

def parseRSSI(rssi):
    start = rssi.find(">")
    end = rssi.find("</")
    return int(rssi[start+1:end])

def parseCSI(csi):
    start = csi.find(">")
    end = csi.find("</")
    anchor = start+1
    im = []
    re = []
    amp = []
    phs = []
    count = 0
    for i in range(start+1, end):
        if csi[i] != ' ':
            continue
        val = int(csi[anchor:i])
        anchor = i+1
        if count % 2 == 0:
            im.append(val)
        else:
            re.append(val)
        count+=1
    # print(len(im), len(re))
    if (len(im) != 64):
        return [],[]
    
    for i in range(len(im)):
        z = complex(re[i],im[i])
        amp.append(np.absolute(z))
        phs.append(np.angle(z))
    return amp, phs

def getCycleDiffAmongPkts(ts):
    prev = ts[0]
    diffVec = []
    for i in range(len(ts)):
        curr = ts[i]
        if curr >= prev:
            diffVec.append(curr-prev)
        else:
            diffVec.append(curr+(2**32-1-prev))
        prev = curr

    # print(240e6/np.mean(diffVec[2000:5000]))
    return diffVec

def getMaxPhaseDiffAcrossSubcarriers(phsMat):
    # The 28~36 subcarriers are not used, their phase and amplitude are always 0
    phsDiffVec = []
    for c in range(phsMat.shape[1]):
        phsVec = np.concatenate((phsMat[2:28,c],phsMat[37:,c]),axis=0)
        maxi = np.max(phsVec)
        mini = np.min(phsVec)
        diff = maxi-mini
        phsDiffVec.append(diff)
    return phsDiffVec

def getTimeFromCycleCount(ts):
    cpu_speed = 240e6
    tVec = [0]
    diffVec = getCycleDiffAmongPkts(ts)
    for i in range(len(diffVec)):
        tVec.append(tVec[-1]+diffVec[i]/cpu_speed)
    return tVec[1:]

def binarySearch(arr, target):
    l, r = 0, len(arr)-1
    while l < r:
        m = (l+r)//2
        if arr[m] > target:
            r = m
        elif arr[m] < target:
            l = m+1
        else:
            return m
    return l
    
def getSamples(t_start, dura, tVec):
    return binarySearch(tVec, t_start), binarySearch(tVec, t_start+dura)

def getAmplitudeVariance(ampMat):
    scVec = []
    for i in range(ampMat.shape[0]):
        scVec.append(np.var(ampMat[i,:]))
    return scVec
