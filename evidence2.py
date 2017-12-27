import Leadingsession as ls
import math

R = 100
indexs = []

for session in ls.sessionList:
    index_sum = []
    for event in session.eventList:
        startTime = event.startTime
        endTime = event.endTime
        middle1Time = 0
        middle2Time = 0
        for time in range(startTime, endTime, 1):
            if middle1Time == 0:
                if ls.y[time] <= R:
                    middle1Time = middle2Time = time
            elif ls.y[time] <= R:
                middle2Time = time
            else:
                break
        if middle1Time == 0 or middle2Time == 0:
            continue
        try:
            print('~~', startTime, middle1Time, middle2Time, endTime)
            t_change = middle2Time - middle1Time + 1
            sum_rank = 0
            for time in range(middle1Time, middle2Time, 1):
                sum_rank += ls.y[time]
            rank_average = sum_rank / t_change
            index = (ls.K - rank_average) / t_change
            index_sum.append(index)
        except ZeroDivisionError:
            print('******')
            continue
    if len(index_sum) == 0:
        continue
    index_s = sum(index_sum) / len(index_sum)
    indexs.append(index_s)
if len(indexs) == 0:
    print('无数据')
    exit(1)

if len(indexs) == 1:
    print(indexs[0])
    exit(1)

average = sum(indexs) / len(indexs)
variance = 0
sum_index = 0

for i in indexs:
    sum_index += (i - average) * (i - average)
    # variance = (i - average) * (i - average)
    # evidence1 = 1 / 2 * (1 + math.erf((i - average) / (math.sqrt(variance) * math.sqrt(2))))
    # print(i, evidence1)
variance = sum_index / len(indexs)  # 均值
for sindex in indexs:
    evidence2 = 1 / 2 * (1 + math.erf((sindex - average) / (variance * math.sqrt(2))))
    print(sindex, evidence2)
