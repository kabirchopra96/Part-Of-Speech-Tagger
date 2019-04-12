import json
from collections import defaultdict
import sys

''' Reading from the model file '''
with open("hmmmodel.txt") as o:
    a = json.load(o)
tags = a['Tags']
t_p = a['Transition-probability']
e_p = a['Emission-probability']

f = open("hmmoutput.txt", 'w')
prob_of_tags = defaultdict(int)
test=open(sys.argv[1], "r", encoding="utf8")
for sentence in test:
    prev_tags = {}
    words = sentence.strip().split(' ')
    #if new word
    if(words[0] not in e_p.keys()):
        for each_tag in tags:
            prob_of_tags[each_tag] = t_p[each_tag]['START']
            prev_tags[(each_tag, 0)] = 'START'
    else:
        for each_tag in e_p[words[0]].keys():
            prob_of_tags[each_tag] = e_p[words[0]][each_tag] + t_p[each_tag]['START']
            prev_tags[(each_tag, 0)] = 'START'
    for k in range(1, len(words)):
        a = {}
        # if new word
        if(words[k] not in e_p.keys()):
            for each_tag in tags:
                a[each_tag] = 0.0
            e_p[words[k]] = a
        t = {}
        for tag1 in e_p[words[k]].keys():
            max1 = float('-Inf')
            for tag0 in prob_of_tags.keys():
                total = prob_of_tags[tag0] + t_p[tag1][tag0]
                if(total > max1):
                    best = tag0
                    max1 = total
            t[tag1] = max1 + e_p[words[k]][tag1]
            prev_tags[(tag1, k)] = best
        prob_of_tags = t
    best = max(prob_of_tags, key=prob_of_tags.get)
    sentence_with_tags = words[len(words)-1] + "/" + best + " "
    for i in range(len(words)-1, 0, -1):
        tag0 = prev_tags[(best, i)]
        best = tag0
        sentence_with_tags = words[i-1] + "/" + tag0 + " " + sentence_with_tags
    f.write(sentence_with_tags[:-1])
    f.write("\n")