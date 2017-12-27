import Leadingsession as ls
import math
import evidence1 as e1
import evidence2 as e2
import evidence3 as e3

evidence = [e1.evidence1, e2.evidence2, e3.evidence3]

for i in range(1, len(e1.degrees)):
    middle_data = (e1.evidence1 + e2.evidence2 + e3.evidence3) / len(e1.degrees)
    for j in range(1, len(evidence)):
        evidence_aggregation = (evidence[j] - middle_data) * (evidence[j] - middle_data)
        print(evidence_aggregation)
