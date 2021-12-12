import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
from numpy.lib.function_base import percentile

def parseLine(line):
    start = line.find(">")
    end = line.find("</")
    return int(line[start+1:end])

def parseLogFile(fname):
    ack_bit = 1
    inj_bit = 0
    injVec = []
    ackVec = []
    with open(fname, "r") as f:
        raw = f.readlines()
        i = 0
        inj_idx = 0
        ack_idx = 0
        while i < len(raw):
            if i % 2 == inj_bit and raw[i].find("inject") != -1:
                injVec.append(parseLine(raw[i]))
                i += 1
                inj_idx += 1
            elif i % 2 == ack_bit and raw[i].find("ACK") != -1:
                ackVec.append(parseLine(raw[i]))
                i += 1
                ack_idx += 1
            else:
                if i % 2 == ack_bit:
                    # print("err: missing ACK; line:", i)
                    injVec.pop()
                else:
                    print("err: missing inj; line:", i)
                    i += 1
                ack_bit, inj_bit = inj_bit, ack_bit
    return np.array(injVec), np.array(ackVec)

def plotDiff(injVec, ackVec, fpath):
    diffVec = ackVec - injVec
    plt.figure()
    plt.scatter(np.arange(len(diffVec)), diffVec)
    plt.xlabel("Packet ID")
    plt.ylabel("Cycle Difference")
    plt.savefig(fpath)
    return diffVec

def filterByThreshold(arr, bnd):
    res = []
    for i in range(len(arr)):
        if arr[i] > bnd[0] and arr[i] < bnd[1]:
            res.append(arr[i])
    return res

def plotFilteredData(baseline, wall, fpath):
    plt.figure()
    plt.scatter(np.arange(len(baseline)), baseline, label = 'baseline',marker='^')
    plt.scatter(np.arange(len(wall)), wall, label = 'device-on-the-wall', alpha=0.4)
    plt.legend()
    plt.savefig(fpath)

def plotAllData(baseline, wall, fpath):
    plt.figure()
    plt.scatter(np.arange(len(baseline)), baseline, label = 'baseline')
    plt.scatter(np.arange(len(wall)), wall, label = 'device-on-the-wall')
    plt.legend()
    plt.savefig(fpath)

def filter(diff):
    val, cnt = np.unique(diff, return_counts=True)
    # Interpolation
    val_interp = np.arange(val[0], val[-1])
    cnt_interp = []
    for i in range(len(val_interp)):
        if val_interp[i] in val:
            cnt_interp.append(cnt[np.where(val == val_interp[i])[0][0]])
        else:
            cnt_interp.append(0)
    assert(len(val_interp) == len(cnt_interp))
    cdf_interp = np.cumsum(cnt_interp) / np.sum(cnt_interp)
    win_len = 100
    thrd = 0.6
    perc_vec = []
    val_interp = np.arange(val_interp[0], val_interp[-1]+1+win_len)
    cdf_interp = np.concatenate((cdf_interp, np.array([1.]*win_len)))
    assert(len(val_interp) == len(cdf_interp))
    for i in range(len(val_interp)-win_len):
        perc_vec.append(cdf_interp[i+win_len] - cdf_interp[i])
    filtered_idx =[]
    for i in range(len(perc_vec)):
        if perc_vec[i] > thrd:
            filtered_idx.append(i)
    center = (filtered_idx[0]+win_len+filtered_idx[-1])//2
    # Get the weighted average within the window
    left = val_interp[center-win_len//2]
    right = val_interp[center+win_len//2]
    filtered_samples = []
    for i in range(len(diff)):
        if diff[i] >= left and diff[i] <= right:
            filtered_samples.append(diff[i])
    # print(filtered_samples)
    return filtered_samples

def plotDistribution(diff, fpath):
    val, cnt = np.unique(diff, return_counts=True)
    cdf = np.cumsum(cnt) / np.sum(cnt)
    plt.figure()
    plt.plot(val, cdf)
    plt.xlabel("Cycle Difference")
    plt.ylabel("CDF")
    plt.savefig(fpath)


def drawLayout():
    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
    plt.figure(figsize=(12,10))
    plt.gca().invert_yaxis()
    # length
    plt.plot(np.linspace(0,162,100), [0] * 100, c = 'k')
    plt.plot(np.linspace(0,162,100), [135] * 100, c = 'k')
    # width
    plt.plot([0] * 100, np.linspace(0, 135, 100), c = 'k')
    plt.plot([162] * 100, np.linspace(0, 135, 100), c = 'k')
    # Anchor Points
    plt.scatter([64, 0, 162], [0, 106, 73], marker='x', s = 100, label = "Anchor Points")
    # Target
    plt.scatter([162-26.5],[135-25.5], marker="o", s = 200, edgecolors='r', c = 'w', label = "Target")
    plt.legend(loc = 'upper right')
    plt.savefig("./imgs/deployment-layout.png")

def estimateDistance(baseline, anchor, id):
    print(id[1:])
    common_path_all = "./imgs/all-pt{}.png"
    common_path_filtered = "./imgs/filtered-pt{}.png"
    plotAllData(baseline, anchor, common_path_all.format(id))
    filtered_bl = filter(baseline)
    filtered_anchor = filter(anchor)
    plotFilteredData(filtered_bl, filtered_anchor, common_path_filtered.format(id))
    mean_diff = np.mean(filtered_anchor)-np.mean(filtered_bl)
    print("Mean difference:", mean_diff)
    print("Estimated distance:", mean_diff/240e6 * 3e8/2)

def measOnTheWall():
    # baseline Point 1
    injVec, ackVec = parseLogFile("./logs/baseline-pt2.log")
    assert(len(injVec) == len(ackVec))
    baseline_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-baseline-pt1.png')
    # Point 1
    injVec, ackVec = parseLogFile("./logs/wall-pt1.1.log")
    assert(len(injVec) == len(ackVec))
    pt1_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-pt1.png')
    estimateDistance(baseline_diff, pt1_diff, 1)

    # baseline Point 2
    injVec, ackVec = parseLogFile("./logs/baseline-pt2.log")
    assert(len(injVec) == len(ackVec))
    baseline_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-baseline-pt2.png')
    # Point 2
    injVec, ackVec = parseLogFile("./logs/wall-pt2.1.log")
    assert(len(injVec) == len(ackVec))
    pt2_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-pt2.png')
    estimateDistance(baseline_diff, pt2_diff, 2)

    # baseline Point 3
    injVec, ackVec = parseLogFile("./logs/baseline-pt3.log")
    assert(len(injVec) == len(ackVec))
    baseline_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-baseline-pt3.png')
    # Point 3
    injVec, ackVec = parseLogFile("./logs/wall-pt3.1.log")
    assert(len(injVec) == len(ackVec))
    pt3_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-pt3.png')
    estimateDistance(baseline_diff, pt3_diff, 3)
    
    plotDistribution(baseline_diff,"./imgs/cdf-baseline.png")
    plotDistribution(pt1_diff,"./imgs/cdf-pt1.png")
    plotDistribution(pt2_diff,"./imgs/cdf-pt2.png")
    plotDistribution(pt3_diff,"./imgs/cdf-pt3.png")
    drawLayout()

def measAligned():
    # baseline 
    injVec, ackVec = parseLogFile("./logs/aligned-baseline.log")
    assert(len(injVec) == len(ackVec))
    baseline_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-aligned-baseline.png')
    plotDistribution(baseline_diff,"./imgs/cdf-baseline.png")
    # 1 meter
    injVec, ackVec = parseLogFile("./logs/aligned-1m.log")
    assert(len(injVec) == len(ackVec))
    pt1_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-aligned-1m.png')
    plotDistribution(pt1_diff,"./imgs/cdf-1m.png")
    estimateDistance(baseline_diff, pt1_diff, "-1m")
    # 2 meter
    injVec, ackVec = parseLogFile("./logs/aligned-2m.log")
    assert(len(injVec) == len(ackVec))
    pt2_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-aligned-2m.png')
    plotDistribution(pt2_diff,"./imgs/cdf-2m.png")
    estimateDistance(baseline_diff, pt2_diff, "-2m")
    # 3 meter
    injVec, ackVec = parseLogFile("./logs/aligned-3m.log")
    assert(len(injVec) == len(ackVec))
    pt3_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-aligned-3m.png')
    plotDistribution(pt3_diff,"./imgs/cdf-3m.png")
    estimateDistance(baseline_diff, pt3_diff, "-3m")
    # 4 meter
    injVec, ackVec = parseLogFile("./logs/aligned-4m.log")
    assert(len(injVec) == len(ackVec))
    pt4_diff = ackVec - injVec
    plotDiff(injVec, ackVec, './imgs/diff-aligned-4m.png')
    plotDistribution(pt4_diff,"./imgs/cdf-4m.png")
    estimateDistance(baseline_diff, pt4_diff, "-4m")

if __name__ == "__main__":
    # measOnTheWall()
    measAligned()


    
    




