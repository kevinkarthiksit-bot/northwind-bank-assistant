import json
import sys
from collections import Counter

path = sys.argv[1]

with open(path,encoding="utf-8") as handle:
    conversations = json.load(handle)
    print(len(conversations))

fallback_count = 0
for conversation in conversations:
    for turn in conversation["turns"]:
        if turn["fallback"]:
            fallback_count +=1
print(fallback_count)

handoff_count = 0
for conversation in conversations:
    for turn in conversation["turns"]:
        if turn["handoff"]:
            handoff_count+=1
print(handoff_count)


def count_by_intent(conversations):
    counts={}
    for conversation in conversations:
        for turn in conversation["turns"]:
            intent=turn["intent"]
            if intent not in counts:
                counts[intent]=0
            counts[intent]+=1
    return counts

print(count_by_intent(conversations))

for conversation in conversations:
    counts ={}
    for turn in conversation["turns"]:
        intent=turn["intent"]
        if intent not in counts:
            counts[intent]=0
        counts[intent]+=1
    for intent, count in counts.items():
        if count >=3:
            print((conversation["conversation_id"],intent,count))

top_intent = None
top_count = 0
for intent, count in count_by_intent(conversations).items():
    if count > top_count:
        top_intent = intent
        top_count= count
print(top_intent,top_count)
    
fallback_utterances ={}
for conversation in conversations:
    for turn in conversation["turns"]:
        if turn["fallback"]:
            utterance = turn["utterance"]
            if utterance not in fallback_utterances:
                fallback_utterances[utterance]=0
            fallback_utterances[utterance]+=1

print(fallback_utterances)
        
top_utterance = None
top_utterance_count = 0
for utterance, count in fallback_utterances.items():
    if count>top_utterance_count:
        top_utterance = utterance
        top_utterance_count = count
print(top_utterance,top_utterance_count)

intent_counter= Counter()
for conversation in conversations:
    for turn in conversation["turns"]:
        intent_counter[turn["intent"]]+=1
print(intent_counter)

intents = set()
for conversation in conversations:
    for turn in conversation["turns"]:
        intents.add(turn["intent"])
print(intents)


