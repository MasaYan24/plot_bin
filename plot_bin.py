#! /usr/bin/env python3

import argparse
import pandas
import matplotlib.pyplot as plt
import sys

class ReadPlot(object):
    def __init__(self,datafile="score.csv",figfile="score.png",cols=[0],sep='\t',trim=True):
        self.__datafile = datafile
        self.__figfile = figfile
        self.__readfile(datafile=datafile,columns=cols)
        self.__trim = trim

    def __readfile(self,datafile="score.csv",columns=[0]):
        self.__columns = columns
        self.__data = pandas.read_csv(datafile,header=None,encoding='utf-8',skipinitialspace=True,sep='\t',usecols=columns)
        self.__data.columns = [i for i in range(len(self.__data.columns))] # rename columns as sequence number
        self.__average = self.__data.mean()
        print(self.__average)
        print(self.__data[0].values)
        if self.__trim:
            for i in self.__data.columns:
                self.__data[i] = self.__data[i].apply(self.__trim)
                print(self.__data[i])

    def __trim(self,_x):
        if _x < 0: return 0
        if _x > 100: return 100
        return _x



    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.set_xlabel('score')
        ax.set_ylabel('number of people')
        ax.hist(self.__data.values,range=(0,100),rwidth=1.0)
        for i in self.__data.columns:
            ax.axvline(self.__average[i],color='C'+str(i))
        plt.show()
#            print(self.__data[i])
#        print(self.__data)
#        self.__data_array = []
#        print(self.__data[columns[0]])
#        for i in range(len(columns)):
#            print(self.__data[columns[i]])
#            self.__data_array.append(self.__data[columns[i]])
#        print(self.__data_array)
#        for i in range(len(columns)):
#            print(self.__data_array[i])


if __name__ == '__main__':
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,argparse.MetavarTypeHelpFormatter):
        pass
    parser = argparse.ArgumentParser(description="Plot score.", formatter_class=CustomFormatter)
    parser.add_argument('--file', '--datafile', type=str, dest='datafile', nargs=1, default='score.csv', help="input file")
    parser.add_argument('--fig', type=str, dest='figfile', nargs=1, default='score.png', help="output figure file (png)")
    parser.add_argument('--columns', type=int, dest='columns', nargs='+', default=[0], help="column of data")
    parser.add_argument('--notrim', action="store_false", help="do not round-up/down score")
    parser.add_argument('--sep', type=str, dest='sep', nargs=1, default='\t', help="specify data separater")

    args = parser.parse_args()

    stat_inst = ReadPlot(datafile=args.datafile,figfile=args.figfile,cols=args.columns,sep=args.sep,trim=args.notrim)
    stat_inst.plot()
