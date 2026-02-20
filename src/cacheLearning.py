import time
from collections import defaultdict


cache = defaultdict(int)
def collatz_cache(n):
    if n in cache:
        return cache[n]
    if n == 1:
        return 0
    elif n % 2 == 0:
        result = 1 + collatz_cache(n // 2)
    else:
        result = 1 + collatz_cache(3 * n + 1)
    cache[n] = result
    return result

def collatz(n):
    length = 0
    if n == 1:
        return length
    elif n % 2 == 0:
        length = 1 + collatz(n // 2)
    else:
        length = 1 + collatz(3 * n + 1)
    return length

def run(maxNum, func):
    timeData = []
    for i in range(1, maxNum + 1):
        timestart = time.time()
        func(i)
        timeend = time.time()
        timeData.append((i, cache[i], timeend - timestart))
    return timeData

def outputTimeData(timeData, filename):
    with open(filename, "w") as f:
        print("Number,Collatz Length,Time Taken", file=f)
        for n, c, t in timeData:
            print(f"{n},{c},{t}", file=f)

def main():
    maxNum = 1000000000
    timeDataCache = run(maxNum, collatz_cache)
    outputTimeData(timeDataCache, "timeDataCache.txt")
    #timeDataNoCache = run(maxNum, collatz)
    #outputTimeData(timeDataNoCache, "timeDataNoCache.txt")

main()

