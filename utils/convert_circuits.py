import math
import argparse
import random
import json
import os

class convertion():

    def __init__(self,circuits_name):
        self.head = []
        self.sinks = []
        self.lines = []
        self.num_real_sinks = 0
        self.num_pseudo_sinks = 0
        self.num_sinks = 0
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0
        self.sink_cap = 0
        self.load_sink_cap()
        self.circuits = circuits_name

    def load_sink_cap(self):

        with open("./utils/sink.json",'r') as f:
            a_dict = json.loads(f.read())
            self.sink_cap = a_dict["sink"]["input_cap"]
        

    def bnpPre(self):
        bnp_pre = []
        max_level = int(math.ceil(math.sqrt(self.num_real_sinks)))
        # # enumerate all branch plan combination with all prime number smaller than max_fanout 
        for i1 in range(0, max_level):
            for i2 in range(0, max_level):
                for i3 in range(0,max_level):
                    for i4 in range(0,max_level):
                        bnp_pre.append((2**i1)*(3**i2)*(5**i3)*(7**i4))

        bnp_pre = sorted(bnp_pre)
        # find the closed number to the sink_num in the bnp_pre list
        for i, number in enumerate(bnp_pre):
            if number >= self.num_real_sinks:
                self.num_sinks = number
                break
        self.num_pseudo_sinks = self.num_sinks - self.num_real_sinks

    def readOriginFile(self):

        with open("./circuits/ex_ispd/{}".format(self.circuits),'r') as f:
            area = f.readline()
            self.head.append(area)

            self.minX,self.minY,self.maxX,self.maxY = tuple(map(int,area.split(" ")))          
            # skip second Line
            source = f.readline()
            self.head.append(source)
            sink_info = f.readline()
            self.head.append(sink_info)

            self.num_real_sinks = int(sink_info.split(" ")[2])
            self.num_sinks = self.num_real_sinks

            start_label = 1
            for i in range(self.num_real_sinks):
                sink_line = f.readline()
                data = sink_line.split(" ")
                self.sinks.append(sink_line)
                start_label += 1

                # update horizontal plot constraints
                if int(data[1]) < self.minX:
                    self.minX = int(data[1])
                elif int(data[1]) > self.maxX:
                    self.maxX = int(data[1])

                # update vertical plot constraints
                if int(data[2]) < self.minY:
                    self.minY = int(data[2])
                elif int(data[2]) > self.maxY:
                    self.maxY = int(data[2])
            
            self.bnpPre()
            
            for i in range(self.num_pseudo_sinks):
                x = random.randint(self.minX,self.maxX)
                y = random.randint(self.minY,self.maxY)
                self.sinks.append("{} {} {} {}\n".format(start_label+i,x,y,self.sink_cap))

            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    self.lines.append(line)

    def export_with_pseudo(self):
        with open("./evaluation/input/{}".format(self.circuits),'w') as f:
            for i,line in enumerate(self.head):
                if i < 2:
                    f.write(line)
                else:
                    f.write("num sink {}\n".format(self.num_sinks))
            
            for line in self.sinks:
                f.write(line)
            
            for line in self.lines:
                f.write(line)

def convert_circuits(circuits):
    convert = convertion(circuits)
    convert.readOriginFile()
    convert.export_with_pseudo()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--circuit',dest='circuits',action='append',required=True,help="circuit to be converted")
    args = parser.parse_args()
    circuits = args.circuits
    for a_circuits in circuits:
        convert_circuits(a_circuits)
    
