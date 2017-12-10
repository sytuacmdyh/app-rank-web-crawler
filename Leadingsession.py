import csv
import matplotlib.pyplot as plt

# appId = '3244609'
appId = '516140'

x = range(364)
y = []

with open('data/2016-12-01_2017-12-01_rank.csv', 'r') as f:
    f.readline()
    reader = csv.reader(f)
    for line in reader:
        try:
            y.append(line.index(appId) + 1)
        except ValueError:
            y.append(10000)


# leading session


class LeadingEvent:
    startTime = 0
    endTime = 0


class LeadingSession:
    eventList = []
    startTime = None
    endTime = None

    def addEvent(self, leadingEvent):
        self.eventList.append(leadingEvent)
        self.endTime = leadingEvent.endTime
        if not self.startTime:
            self.startTime = leadingEvent.startTime


K = 75
T = 7
eventList = []
event = None
for i in range(len(y)):
    if y[i] <= K:
        if event:
            event.endTime = i
        else:
            event = LeadingEvent()
            event.startTime = event.endTime = i
    elif event:
        eventList.append(event)
        event = None
if event:
    eventList.append(event)

# for event in eventList:
#     print(event.startTime)

session = None
sessionList = []
for event in eventList:
    if not session:
        session = LeadingSession()
        session.addEvent(event)
        continue
    if session.endTime + 7 >= event.startTime:
        session.addEvent(event)
    else:
        sessionList.append(session)
        session = LeadingSession()
        session.addEvent(event)
if session:
    sessionList.append(session)

for session in sessionList:
    print(session.startTime)
    print(session.endTime)

#
# plt.figure()
# plt.plot(x, y)
# plt.ylim(0, 200)
#
# plt.gca().invert_yaxis()
# plt.show()
