from __future__ import division
from itertools import product
import random
import sys
import numpy
import decimal
import random
import sys


def eAll(bnet,top_order,evidence):
    
    if len(top_order) == 0: 
        return 1
    e = top_order.pop()
    
    if e in evidence:
        
        
        if len(bnet[e][0]) == 0:
            prob = bnet[e][1][None]
        else:
            
            
            prob = bnet[e][1][tuple([evidence[par] for par in bnet[e][0]])]
        if evidence[e]==True: 
            pr=prob
        else:
            pr=(1-prob)
        product = pr * eAll(bnet,top_order,evidence)
        top_order.append(e)
        return product
    else:
        sum = 0
        
        for item in [True,False]:
            evidence[e] = item
            
            
            if len(bnet[e][0]) == 0:
                prob = bnet[e][1][None]
            else:
            
                
                prob = bnet[e][1][tuple([evidence[par] for par in bnet[e][0]])]
            if evidence[e]==True: 
                pr=prob
            else:
                pr=(1.0-prob)
            sum =sum+ (pr * eAll(bnet,top_order,evidence))
            
        
        evidence.pop(e)
        
        top_order.append(e)
        return sum

        
def enumeration(top_order,evidence,query):
	bnet = {'B':[[],{None:.001}],
      'E':[[],{None:.002}],
      'A':[['B','E'],{(False,False):.001,(False,True):.29,(True,False):.94,(True,True):.95}],
      'J':[['A'],{(False,):.05,(True,):.90}], 
      'M':[['A'],{(False,):.01,(True,):.70}]}
    
	Distr_X= {}
	for var in [False,True]:
        	evidence[query] = var
        
        	Distr_X[var] = eAll(bnet,top_order,evidence)
        
        	evidence.pop(query)
	tot = 0
	for value in Distr_X.values():
	        tot+= value
	for k in Distr_X.keys():
	        Distr_X[k] /= tot
	return Distr_X[True]


def prior(n, bnet):

	evidence = {}
	e=0;q=0
	evidenceNumber = raw_input()
	vals = evidenceNumber.split()
	for y in range(0, int(vals[0])):
		evi = raw_input().split()
		evidence[evi[0]]=evi[1]
	query = raw_input()
	x=0
	prob =0
	
	for j in range(0,10):
		for i in range(0,int(n)):
			Aval='f'; Bval='f'; Eval='f'; Mval='f'; Jval='f'
			counter = 0

			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['B'][1][None]: 
				Bval='t'
			if 'B' in evidence.keys() and evidence['B']==Bval:
				counter= counter+1

			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['E'][1][None]: 
				Eval='t'
			if 'E' in evidence and evidence['E']==Eval:
				counter= counter+1

			decider = numpy.random.uniform(low=0, high=1)
			if decider <=  bnet['A'][1][Bval,Eval]: 
				Aval='t'
			if 'A' in evidence and evidence['A']==Aval:
				counter= counter+1

			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['M'][1][Aval]:
				Mval='t'
			if 'M' in evidence and evidence['M']==Mval:
				counter= counter+1

			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['J'][1][Aval]:
				Jval='t'
			if 'J' in evidence and evidence['J']==Jval:
				counter= counter+1

			if counter == int(vals[0]):
				e=e+1
				if (query=='A' and Aval=='t') or (query=='B' and Bval=='t') or (query=='J' and Jval=='t') or (query=='M' and Mval=='t') or (query=='E' and Eval=='t'):
					q = q+1
	
		try:
			prob = prob + float(float(q)/float(e))
		except ZeroDivisionError:
			pass
	try:	
		finalProb = decimal.Decimal(prob/10)
		finalProb = round(finalProb,6)
		print query + " " + str(finalProb)
	except ZeroDivisionError:
		pass

def rejection(n, bnet):
	
	#Input
	evidence = {}
	evidenceNumber = raw_input()
	vals = evidenceNumber.split()
	for y in range(0, int(vals[0])):
		evi = raw_input().split()
		evidence[evi[0]]=evi[1]
	query = raw_input()

	e=0;q=0;x=0;prob=0
	prob = 0
	
	for i in range(0,10):
		for i in range(0,int(n)):
			Aval='f'; Bval='f'; Eval='f'; Mval='f'; Jval='f'
			counter = 0
	
			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['B'][1][None]:  
				Bval='t'
		
			if 'B' in evidence.keys() and evidence['B']==Bval:
				counter= counter+1
			elif 'B' in evidence.keys() and evidence['B']!=Bval:
				continue
		

			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['E'][1][None]:
				Eval='t'
			if 'E' in evidence and evidence['E']==Eval:
				counter= counter+1
			elif 'E' in evidence and evidence['E']!=Eval:
				continue

			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['A'][1][Bval,Eval]:
				Aval='t'
			if 'A' in evidence and evidence['A']==Aval:
				counter= counter+1
			elif 'A' in evidence and evidence['A']!=Aval:
				continue

			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['J'][1][Aval]:
				Jval='t'
			if 'J' in evidence and evidence['J']==Jval:
				counter= counter+1
			elif 'J' in evidence and evidence['J']!=Jval:
				continue

			decider = numpy.random.uniform(low=0, high=1)
			if decider <= bnet['M'][1][Aval]:
				Mval='t'
			if 'M' in evidence and evidence['M']==Mval:
				counter= counter+1
			elif 'M' in evidence and evidence['M']!=Mval:
				continue
		
			if counter == int(vals[0]):
				e=e+1
				if (query == 'A' and Aval=='t') or (query == 'B' and Bval=='t') or (query == 'E' and Eval=='t') or (query == 'J' and Jval=='t') or (query == 'M' and Mval=='t'):
					q = q+1
		try:
			prob = prob + float(float(q)/float(e))
		except ZeroDivisionError:
			pass
	try:	
		
		finalProb = decimal.Decimal(prob/10)
		finalProb = round(finalProb,6)
		print query + " " + str(finalProb)
	except ZeroDivisionError:
			pass


def likelihood(n, bnet):
	evidence = {}
	e=0;q=0
	evidenceNumber = raw_input()
	vals = evidenceNumber.split()
	for y in range(0, int(vals[0])):
		evi = raw_input().split()
		evidence[evi[0]]=evi[1]
	#print evidence
	query = raw_input()
	weight = 1

	sampleWeightList = []
	# p(j|B,e)
	prob = 0
	for j in range(0,10):
		for i in range(0,int(n)):
			sampleDict = {'B':'f','A':'f','E':'f','M':'f','J':'f','W':0}; weight = 1
			if 'B' in evidence.keys():
				sampleDict['B'] = evidence['B']
				if evidence['B'] == 't': 
					weight = weight*bnet['B'][1][None] 
				else: 
					weight = weight*(1 - bnet['B'][1][None])
		
			else:
				decider = numpy.random.uniform(low=0, high=1)
				if decider <=  bnet['B'][1][None]:
					sampleDict['B'] = 't' 
				else: 
					sampleDict['B'] = 'f'
	
			if 'E' in evidence.keys():
				sampleDict['E'] = evidence['E']
				if evidence['E'] == 't': 
					weight = weight*bnet['E'][1][None] 
				else: 
					weight = weight*(1 - bnet['E'][1][None])
			else:
				decider = numpy.random.uniform(low=0, high=1)
				if decider <= bnet['E'][1][None]:
					sampleDict['E'] = 't' 
				else: 
					sampleDict['E'] = 'f'

			if 'A' in evidence.keys():
				sampleDict['A'] = evidence['A']
				if evidence['A'] == 't':
					weight = weight*bnet['A'][1][sampleDict['B'],sampleDict['E']]

				else:
					weight = weight*(1 - bnet['A'][1][sampleDict['B'],sampleDict['E']])
			else:
				decider = numpy.random.uniform(low=0, high=1)
				if decider <=  bnet['A'][1][sampleDict['B'],sampleDict['E']]: 
					sampleDict['A'] = 't' 
				else: 
					sampleDict['A'] = 'f'	
			if 'J' in evidence.keys():
				sampleDict['J'] = evidence['J']
				if evidence['J'] == 't': 
					weight = weight*bnet['J'][1][sampleDict['A']] 
				else: 
					weight = weight* (1 - bnet['J'][1][sampleDict['A']])
			else:
				decider = numpy.random.uniform(low=0, high=1)
				if decider <=  bnet['J'][1][sampleDict['A']]:
					sampleDict['J'] = 't' 
				else: 
					sampleDict['J'] = 'f'	
			if 'M' in evidence.keys():
				sampleDict['M'] = evidence['M']
				if evidence['M'] == 't': 
					weight = weight*bnet['M'][1][sampleDict['A']] 
				else: 
					weight = weight* (1 - bnet['M'][1][sampleDict['A']])
			else:
				decider = numpy.random.uniform(low=0, high=1)
				if decider <= bnet['M'][1][sampleDict['A']]: 
					sampleDict['M'] = 't' 
				else: 
					sampleDict['M'] = 'f'

			sampleDict['W']=weight
		
			sampleWeightList.append(sampleDict)

		weightEvidence = 0
		totalWeight = 0
		for x in sampleWeightList:
			if x[query] == 't':
				weightEvidence = weightEvidence + x['W']
				totalWeight = totalWeight + x['W']
			else:
				totalWeight = totalWeight + x['W']
		
		try:
			prob = prob + float(float(weightEvidence)/float(totalWeight))
		except ZeroDivisionError:
			pass
	try:
		finalProb = decimal.Decimal(prob/10)
		finalProb = round(finalProb,6)
		print query + " " + str(finalProb)
	except ZeroDivisionError:
		pass

if __name__ == "__main__":
	algo = sys.argv[1]
	samples = sys.argv[2]
	
	bnet = {'B':[[],{None:.001}],
	'E':[[],{None:.002}],
	'A':[['B','E'],{('f','f'):.001,('f','t'):.29,('t','f'):.94,('t','t'):.95}],
	'J':[['A'],{'f':.05,'t':.90}], 
	'M':[['A'],{'f':.01,'t':.70}]}
	var1 = ['M','J','A','B','E']

	if algo=='e':

		evidence={}
        	evidenceNumber = raw_input()
        	vals = evidenceNumber.split()
        	for y in range(0, int(vals[0])):
            		evi = raw_input().split()
            		if evi[1]=='t':
                		evidence[evi[0]]=True
            		elif evi[1]=='f':
                		evidence[evi[0]]=False
            
    
        	
            	query = raw_input()
                prob = enumeration(var1,evidence,query)
		finalProb = round(prob,6)
		print query + " " + str(finalProb)

	if algo=='p':
		prior(samples,bnet)
	if algo=='r':
		rejection(samples,bnet)
	if algo=='l':
		likelihood(samples,bnet)
