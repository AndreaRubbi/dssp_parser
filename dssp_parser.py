#!/usr/bin/python3

# ─── IMPORTING LIBRARIES ────────────────────────────────────────────────────────
import sys, colored
import numpy as np
from easygui import fileopenbox
import pandas as pd
from colored import stylize

# ─── MASA DICTIONARY ────────────────────────────────────────────────────────────
masa = {'A':115., 'L':170., 'R':225., 'K': 200., 'N':160., 'M':185., 'D':150., \
		'F':210., 'C':135., 'P':145., 'Q': 180., 'S':115., 'E':190., 'T':140., \
		'G':75., 'W': 255., 'H':195., 'Y': 230., 'I':175., 'V':155.}
	
# ─── FUNCTION : GET TOTAL ACCESSIBILITY AREA ────────────────────────────────────
def get_total_asa(dssp):
	s=0.0
	for v in dssp.values():
		s=s+v[2]
	return s
	
# ─── FUNCTION : GIVEN A CHAIN, RETURNS RELATIVE ACCESSIBILITY AREA OF EACH RESIDUE 
def rasa(dssp, chain):
    d = dict()
    ks = dssp.keys()
    ks = sorted(ks)
    for k in ks:
        if k[1] == chain:#chain num res rasa
            d[k[0]] = (dssp[k][0], dssp[k][2]/ masa[dssp[k][0]])
    rasa, res, n = (list() for x in range(3))
    for k in d.keys():
        n.append(k)
        res.append(d[k][0])
        rasa.append(d[k][1])
    tr = {'Chain' : [chain for x in range(len(d))], 'Residue - N' : n, 'Residue - Type' : res, 'RASA' : rasa }
    index = pd.MultiIndex.from_arrays(list(tr.values()), names=(tr.keys()))
    df = pd.DataFrame(data = tr)
    print(df)
        
    return d

# ─── GIVEN A CHAIN, RETURN ACCESSIBILITY AREA ────────────────────────────────────
def get_asa_chain(dssp, chain): #accessibility area of each chain 
	asa=0
	for i in dssp.keys():
		if i[1] == chain: #selects for residues in the correct chain
			asa += dssp[i][2] #sum accessibility area: third elem of values
	return asa

#Parse DSSP file: stores info in dictionary
#Dssp[(int(num),ch)]=[res,ss,asa,phi,psi]

def parse_dssp(dsspfile):
	dssp={}
	fdssp = open(dsspfile)
	c=0
	for line in fdssp:
		if line.find('  #  RESIDUE') == 0:
			c = 1
			continue
		if c == 1:
			num=line[5:10].strip()
			ch = line[11]
			res=line[13]
			ss=line[16]
			asa=float(line[35:38])
			phi=float(line[103:109])
			psi=float(line[109:115])
			if ss == ' ': ss='C'
			try:
				dssp[((num),ch)]=[res,ss,asa,phi,psi]
			except:
				print >> sys.stderr, 'ERROR', line
	return dssp
				
# ─── FINDING SIGNIFICANTLY DIVERGENT RESIDUES ───────────────────────────────────
def div_res(Rasa_tri, Rasa_tet):
    change = dict()
    for res in Rasa_tri.keys():
        perc = (Rasa_tri[res][1] - Rasa_tet[res][1]) #/ Rasa_tri[res][1] * 100
        if perc >= 0.1:
            change[res, Rasa_tri[res][0]] = str(perc)[:4] + '%'
    res_t, res_n, perc = (list() for x in range(3))
    for k in change.keys():
        res_t.append(k[1])
        res_n.append(k[0])
        perc.append(change[k])
        
    df = pd.DataFrame({'Res-N' : res_n, 'Res-type' : res_t, 'Percentage' : perc})
    df.sort_values(by = ('Percentage'), inplace = True, ascending = False)
    print(df.to_string(index = False))
    return change
    
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('',
stylize('    ___                             ____            ', colored.fg(13)),
stylize('   /   |  ________  ____ _   ____  / __/             ', colored.fg(13)),
stylize('  / /| | / ___/ _ \/ __ `/  / __ \/ /_               ', colored.fg(13)),
stylize(' / ___ |/ /  /  __/ /_/ /  / /_/ / __/               ', colored.fg(13)),
stylize('/_/ _|_/_/  _\___/\__,_/   \____/_/  __  _           ', colored.fg(13)),
stylize('   (_)___  / /____  _________ ______/ /_(_)___  ____ ', colored.fg(13)),
stylize("  / / __ \/ __/ _ \/ ___/ __ `/ ___/ __/ / __ \/ __ \ ", colored.fg(13)),
stylize(' / / / / / /_/  __/ /  / /_/ / /__/ /_/ / /_/ / / / /', colored.fg(13)),
stylize('/_/_/ /_/\__/\___/_/ __\__,_/\___/\__/_/\____/_/ /_/ ', colored.fg(13)),
stylize('  ____ _____  ____ _/ /_  __________  _____          ', colored.fg(13)),
stylize(' / __ `/ __ \/ __ `/ / / / / ___/ _ \/ ___/          ', colored.fg(13)),
stylize('/ /_/ / / / / /_/ / / /_/ (__  )  __/ /              ', colored.fg(13)),
stylize('\__,_/_/ /_/\__,_/_/\__, /____/\___/_/               ', colored.fg(13)),
stylize('                   /____/                            ', colored.fg(13)),
'\n\tBy: Andrea Rubbi\n', sep = '\n\t')
    print('\n─────────────────────────────────────────\n')
    print('Select the Dssp file of one Trimer with the chain of interest')
    Tri = fileopenbox(title = 'Trimer')
    print('You have selected: ', Tri)
    print('\n─────────────────────────────────────────\n')
    print('Select the Dssp file of the Tetramer')
    Tet = fileopenbox(title = 'Tetramer')
    print('You have selected: ', Tet)
    print('\n─────────────────────────────────────────\n')
    dssp_tri = parse_dssp(Tri)
    dssp_tet = parse_dssp(Tet)
    chain = sys.argv[1]
    if len(sys.argv) >= 2:#code for asa of a chain
        TT = input('Trimer or Tetramer?\n(r/e): ')   
        if input('Would you like to calculate the Accessible Area?:\n(y/n): ') == 'y':
            if TT == 'r': 
                print('\n─────────────────────────────────────────\n')
                print('Total accessible Area: ', get_asa_chain(dssp_tri,chain))
            else: 
                print('\n─────────────────────────────────────────\n')
                print('Total accessible Area: ', get_asa_chain(dssp_tet,chain))
            #code for rasa of residues of a chain 
        print('\n─────────────────────────────────────────\n')
        if input('Would you like to calculate the Relative Accessible Area of Each Residue?:\n(y/n): ') == 'y':
            print('\n─────────────────────────────────────────\n')
            chain = sys.argv[1]
            print('Relative accesible Area of each residue of chain {chain}:\n'.format(chain = chain))
            print('\nIn the Trimer:\n')
            Rasa_tri = rasa(dssp_tri, chain)
            print('\n─────────────────────────────────────────\n')
            print('\nIn the Tetramer:\n')
            Rasa_tet = rasa(dssp_tet, chain)
            print('\n─────────────────────────────────────────\n')
            print('\nResidues whose RASA variates significantly:\n')
            div_res(Rasa_tri, Rasa_tet)
            print('\n─────────────────────────────────────────\n')
            
            
		
		

                        
