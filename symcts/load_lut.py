# -*- coding: utf-8 -*-
# @Author: mac
# @Date:   2019-11-02 09:54:23
# @Last Modified by:   eirc
# @Last Modified time: 2019-12-29 15:31:13

from scipy import interpolate
import numpy as np 
import os 
import json

def readindex():

	with open("./utils/settings.json",'r') as f:
		a_dict = json.loads(f.read())
		input_slew = a_dict["library"]["input_slew"] # need to convert to s
		output_load = a_dict["library"]["output_load"] # need to convert to F
	return [slew*1e-12 for slew in input_slew], [cap*1e-15 for cap in output_load]

def readlut(filepath):

	bufsize = 0

	with open("./utils/settings.json",'r') as f:
		a_dict = json.loads(f.read())
		lib_size = a_dict["library"]["lib_size"]
	
	with open("./utils/buffer.json",'r') as f:
		a_dict = json.loads(f.read())
		bufsize = a_dict["buffer_num"]

	delay_lut = np.zeros((lib_size[0],lib_size[1],2,bufsize))
	slew_lut  = np.zeros((lib_size[0],lib_size[1],2,bufsize))
	for s in range(bufsize):
		with open("{}/X{}/lut.txt".format(filepath,s),'r') as f:
			# skip first line
			f.readline()
			# input_slew sweep loop
			for i in range(lib_size[0]):
				# output_cap sweep loop 
				for j in range(lib_size[1]):
					data = f.readline().strip().split(" ")
					delay_lut[i,j,0,s] = float(data[0]) # mean value of delay
					delay_lut[i,j,1,s] = float(data[1]) # standard deviation of delay
					slew_lut[i,j,0,s]  = float(data[2]) # mean value of output slew
					slew_lut[i,j,1,s]  = float(data[3]) # standard deviation of output slew
	return delay_lut,slew_lut

def init_Lut(lut,x,y):
	bufsize = 0
	model = []

	with open("./utils/buffer.json",'r') as f:
		a_dict = json.loads(f.read())
		bufsize = a_dict["buffer_num"]

	for s in range(bufsize):
		# lut model for a specific size
		# using cubic interpolate 
		model_s = interpolate.interp2d(x, y, lut[:,:,s],kind='linear')
		model.append(model_s)
	return model


def load_lut(filepath="./library/lib"):
	if not os.path.exists(filepath):
		print("file path not exist !")
		exit(1)
	else:
		DLut_r,SLut_r = readlut(filepath)
	# delay lut.
	DLut = [DLut_r[:,:,0,:],DLut_r[:,:,1,:]]
	# output slew lut
	SLut = [SLut_r[:,:,0,:],SLut_r[:,:,1,:]]
	return DLut, SLut 

def initialize():
	DModel = []
	SModel = []

	input_slew_index,output_cap_index = readindex()
	Dlut,Slut = load_lut()
	for lut in Dlut:
		DModel.append(init_Lut(lut,input_slew_index,output_cap_index))
	for lut in Slut:
		SModel.append(init_Lut(lut,input_slew_index,output_cap_index))

	return DModel,SModel

def main():
	pass

if __name__ == '__main__':
	main()






