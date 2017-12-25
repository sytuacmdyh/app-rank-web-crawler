import csv
import matplotlib.pyplot as plt

# appId = '3244609'
appId = '34636'

x = range(1,366)
y = []

with open('data/2016-12-01_2017-12-01_rank_free.csv', 'r') as f:
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
	
    eventList = None
    startTime = None
    endTime = None

    def addEvent(self, leadingEvent):
        if not self.eventList:
            self.eventList = []
        self.eventList.append(leadingEvent)
        self.endTime = leadingEvent.endTime

K = 200
T = 7
eventList = []
event = None
for i in range(0,len(y)):
    if y[i] <= K:
        if event:
            event.endTime = i+1
        else:
            event = LeadingEvent()
            event.startTime = event.endTime = i+1
    elif event:
        eventList.append(event)
        event = None
if event:
    eventList.append(event)
    
print("leadingevent:")
for event in eventList:
	print(str(event.startTime)+"_"+str(event.endTime))

# for event in eventList:
#     print(event.startTime)

session = None
sessionList = []
for event in eventList:
    if not session:
        session = LeadingSession()
        session.addEvent(event)
        session.startTime = event.startTime
        continue
    if session.endTime + 7 >= event.startTime:
        session.addEvent(event)
    else:
        sessionList.append(session)
        session = LeadingSession()
        session.addEvent(event)
        session.startTime = event.startTime
if session:
    sessionList.append(session)

print("leadingsession:")
for session in sessionList:
    print(str(session.startTime)+"_"+str(session.endTime))
    #print(len(session.eventList))


plt.figure()
plt.plot(x, y)
plt.ylim(0, 200)
plt.gca().invert_yaxis()
plt.show()
