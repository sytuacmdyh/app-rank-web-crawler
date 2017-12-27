import Leadingsession as ls
import math

event_number = []

for session in ls.sessionList:
    event_number.append(len(session.eventList))
# print(len(session.eventList))

average_number = sum(event_number) / len(event_number)


def f(n):
    c = 1
    for i in range(n + 1):
        if i == 0:
            c = 1
        else:
            c *= i
    return c


sum = 0
for event_number in event_number:
    for i in range(0, event_number):
        sum += (average_number ** i) / f(i)
    evidence3 = math.exp(-average_number) * sum
    print(event_number, evidence3)
