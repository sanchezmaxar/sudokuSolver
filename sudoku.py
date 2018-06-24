import math
import os
import sys
#sudoku
def check(sudoku):
	dim=len(sudoku[0])
	for n in range(1,dim):
		for i in range(dim):
			if sudoku[0][i].count(n)>1:
				return False
			elif sudoku[1][i].count(n)>1:
				return False
			for j in range(int(math.sqrt(dim))):
				if sudoku[2][int(math.sqrt(i))][j].count(n)>1:
					return False
	return True
# Este programa debera resolver el sudoku para nxn 
def transformar(simbolo):
	try:
		return int(simbolo)
	except:
		return simbolo

def transponer(arreglo):
	arrp=[["*" for j in range(len(arreglo))] for i in range(len(arreglo))]
	for i in range(len(arreglo)):
		for j in range(len(arreglo)):
			arrp[j][i]=arreglo[i][j]
	return arrp


def getSquare(hor):
	dim=int(math.sqrt(len(hor)))
	square=[[[] for j in range(dim)] for i in range(dim)]
	for i in range(len(hor)):
		for j in range(len(hor)):
			square[int(i/dim)][int(j/dim)].append(hor[i][j])
	return square

def leer(nombre):
	arch=open(nombre,"r")
	lineas=arch.readlines()
	HVC=[]
	arreglo=[]
	for l in lineas:
		arreglo.append(map(transformar,l.split()))
	dim=math.sqrt(len(arreglo))
	HVC.append(arreglo)
	HVC.append(transponer(arreglo[:][:]))
	HVC.append(getSquare(arreglo))
	return HVC

def contar(i,j,HVC):
	posibles=[]
	dim=math.sqrt(len(HVC[0]))
	for k in range(1,len(HVC[0])+1):
		if not(k in HVC[0][i] or k in HVC[1][j] or k in HVC[2][int(i/dim)][int(j/dim)]):
			posibles.append(k)
	return posibles

def genListas(HVC):
	arreglo=HVC[0]
	listas=[[[]for i in range(len(arreglo))] for j in range(len(arreglo))]
	for i in range(len(arreglo)):
		for j in range(len(arreglo)):
			if arreglo[i][j]=='*': 
				listas[i][j]=contar(i,j,HVC)
	return listas

def solve(HVC,HVCp):
	dim=int(math.sqrt(len(HVC[0])))
	for i in range(len(HVCp[0])):
		for j in range(len(HVCp[0][i])):
			if len(HVCp[0][i][j])==1:
				HVC[0][i][j]=HVCp[0][i][j][0]
	for i in range(len(HVCp[1])):
		for j in range(len(HVCp[1][i])):
			if len(HVCp[1][i][j])==1:
				HVC[0][j][i]=HVCp[1][i][j][0]
	for k in range(len(HVCp[2])):
		for i in range(len(HVCp[2][k])):
			for j in range(len(HVCp[2][k][i])):
				if len(HVCp[2][k][i][j])==1:
					# k*dim+j/dim,i*dim+j%dim
					HVC[0][k*dim+j/dim][i*dim+j%dim]=HVCp[2][k][i][j][0]
	for k in range(1,int(dim*dim)+1):
		for i in range(dim*dim):
			coord=[]
			cond=False
			cond2=False
			for j in range(dim*dim):
				if k in HVCp[0][i][j] and cond2==False:
					cond=True
					coord=[i,j]
					cond2=True
				elif k in HVCp[0][i][j]:
					cond=False
			if cond:
				HVC[0][coord[0]][coord[1]]=k
		for i in range(dim*dim):
			coord=[]
			cond=False
			cond2=False
			for j in range(dim*dim):
				if k in HVCp[1][i][j] and cond2==False:
					cond=True
					coord=[i,j]
					cond2=True
				elif k in HVCp[1][i][j]:
					cond=False
			if cond:
				HVC[0][coord[1]][coord[0]]=k
		for m in range(dim):
			for i in range(dim):
				coord=[]
				cond=False
				cond2=False
				for j in range(dim*dim):
					if k in HVCp[2][m][i][j] and cond2==False:
						coord=[m*dim+j/dim,i*dim+j%dim,j]
						cond=True
						cond2=True
					elif k in HVCp[2][m][i][j]:
						cond=False
				if cond:
					HVC[0][coord[0]][coord[1]]=k
	return HVC


HVC=leer(sys.argv[1])
# print "\n".join(map(lambda x:" ".join(map(str,x)),HVC[0]))
for i in range(26):
	listash=genListas(HVC)
	HVCp=[listash,transponer(listash),getSquare(listash)]
	# print "\n".join(map(lambda x:" ".join(map(str,x)),HVCp[1]))
	HVC=solve(HVC,HVCp)
	HVC=[HVC[0],transponer(HVC[0]),getSquare(HVC[0])]
	# print("\nIteracion: "+str(i+1)+" check: "+str(check(HVC)))
	# print "\n".join(map(lambda x:" ".join(map(str,x)),HVC[0]))
# print check(HVC)
# print "\n".join(map(lambda x:" ".join(map(str,x)),HVC[0]))	