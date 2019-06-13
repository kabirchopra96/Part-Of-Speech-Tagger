import json
import math
from collections import defaultdict
import sys
tags =set()
# Maintain count of transitions from tag to tag
tag_tag = defaultdict(lambda : defaultdict(int))
# Maintain count for each tag
num_of_tags = defaultdict(int)
# Maintain count of tag and word combination
tag_word = defaultdict(lambda: defaultdict(int))
train= open(sys.argv[1],"r",encoding="utf8")
for sentence in train:
    # Split the sentence into words
    words = sentence.strip().split(' ')
    i=len(words[0])-(words[0].rfind('/'))-1
    # START label can only have first word so both will have the same count
    tag_tag['START'][words[0][-i:]]+=1
    num_of_words=len(words)-1
    for k in range(num_of_words):
        i = len(words[k])-(words[k].rfind('/'))-1
        # Tag is the part after the '/'
        tag1 = words[k][-i:]
        tags.add(tag1)
        j= len(words[k+1])-(words[k+1].rfind('/'))-1
        # Tag for the next word
        tag2 = words[k+1][-j:]
        tag_tag[tag1][tag2]+=1
        # Increase tag count
        num_of_tags[tag1]+=1
        tag_word[words[k][:-(i+1)]][tag1]+=1
    j= len(words[num_of_words]) - (words[num_of_words].rfind('/')) - 1
    tags.add(words[num_of_words][-j:])
    num_of_tags[words[num_of_words][-j:]]+=1
    tag_word[words[num_of_words][:-(j+1)]][words[num_of_words][-j:]]+=1
    
# Apply smoothing for unseen transitions
for tag1, tag2_nums in tag_tag.items():
    for tag in tags:
        if(tag not in tag2_nums.keys()):
            tag_tag[tag1][tag]=1.0
for each_tag in tags:
    if(each_tag not in tag_tag):
        for other_tags in tags:
            tag_tag[each_tag][other_tags]=1.0
# Calculate Transition Probabilities
# t_p :  Transition Probabilities          
t_p = defaultdict(lambda: defaultdict(float))
for tag1, tag2_nums in tag_tag.items():
    for tag,count in tag2_nums.items():
        denom=sum(tag2_nums.values())
        t_p[tag][tag1] = math.log10(float(count)/denom)
# Calculate Emission Probabilities
# e_p :  Emission Probabilities
e_p = defaultdict(lambda: defaultdict(float))
for w, tag_nums in tag_word.items():
    for tag,nums in tag_nums.items():
        e_p[w][tag] = math.log10(float(nums)/num_of_tags[tag])
# Create a dictionary of Tags, Trainsition Probabilities and Emission Probabilities
out = dict({'Tags': list(tags), 'Transition-probability': t_p, 'Emission-probability': e_p})
# Write it to the model file
with open("hmmmodel.txt", "w") as f:
    json.dump(out, f, indent=4)
