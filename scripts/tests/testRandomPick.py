import random
import time

trainDS = range(150)
gs42DS = range(20)

def get_batches_by_doc_mix(DS1, DS2, trainBatch, gsBatch):
    i=j=0
    while i<len(DS1):
        while (i)%trainBatch==0 and j<gsBatch:
            time.sleep(0.25)
            yield 'GS', random.choice(DS2)
            j+=1
        j=0
        time.sleep(0.25)
        yield 'Train',DS1[i]
        i+=1

# exp_comb = [(3,2),(5,1),(10,1),(15,1),(20,1),(25,1)]
exp_comb = [(100,48),(100,24),(100,12),(100,6),(100,3)]

for (trBt, gsBt) in exp_comb:
    print(trBt, gsBt)
    for x,y in get_batches_by_doc_mix(trainDS, gs42DS, trainBatch=trBt, gsBatch=gsBt):
        print(x,y)
    print('-'*100)


