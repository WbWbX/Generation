import os
import h5py
import json
import re
import sys
import numpy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--weights', dest='weightsFile', type=str, required=True, help='hdf5 file')
parser.add_argument('--reweight','--reweight', dest='reweightCard', type=str, required=True, help='MG reweight card')
parser.add_argument('-o','--output', dest='output', type=str, required=True, help='output name')
args = parser.parse_args()
                
    
def readReweightCard(reweightCard):
    params = []
    with open(reweightCard) as f:
        width = -1
        mass = -1
        for l in f:
            if l.startswith("launch"):
                if width>=0 and mass>=0:
                    params.append({
                        "width":width,
                        "mass":mass
                    })
                width = -1
                mass = -1
            else:
                matchMod = re.match("set\\s+([A-Za-z]+)\\s+([0-9]+)\\s+([0-9]*\\.[0-9]*[eE][+-][0-9]+)",l)
                if matchMod:
                    group = matchMod.group(1)
                    particle = int(matchMod.group(2))
                    value = float(matchMod.group(3))
                    if group=='mass' and particle==6:
                        mass = value
                    elif group=="DECAY" and particle==6:
                        width = value
        if width>=0 and mass>=0:
            params.append({
                "width":width,
                "mass":mass
            })
    return params
    
def readWeights(weights):
    xsecs = []
    with h5py.File(weights,'r') as f:
        weightNames = sorted(filter(lambda x: x.startswith("rwgt"),f.keys()), key=lambda x: int(x.rsplit('_',1)[1]))
        for weightName in weightNames:
            weights = f[weightName][()]
            xsec = sum(weights)/len(weights)

            xsecs.append({'name':weightName,'xsec':xsec})
    return xsecs
                    
                

if not os.path.exists(args.reweightCard):
    print "reweight_card %s file not found"%(args.reweightCard)
    sys.exit(1)
if not os.path.exists(args.weightsFile):
    print "Weight file %s not found"%(args.weightsFile)
    sys.exit(1)

params = readReweightCard(args.reweightCard)
xsecs = readWeights(args.weightsFile)

if len(params)!=len(xsecs):
    print "Error: number of weights %i vs %i do not match"%(len(params),len(xsecs))
    sys.exit(1) 

outputDict = {}
for i,param in enumerate(params):
    print param,xsecs[i]
    outputDict[i+1] = {
        "width": param['width'],
        'mass': param['mass'],
        'xsec': xsecs[i]['xsec']
    }

with open(args.output,"w") as f:
    json.dump(
        outputDict,
        f,
        ensure_ascii=True, 
        check_circular=True, 
        allow_nan=True, 
        cls=None, 
        indent=4, 
        sort_keys=True, 
    )

    
