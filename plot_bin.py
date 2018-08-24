#! /usr/bin/env python3

import argparse
import pandas
import matplotlib.pyplot as plt
import matplotlib
import subprocess
import sys

class ReadPlot(object):
    def __init__(self,datafile="score.csv",figfile="score.png",cols=[0],sep='\t',trim=True,labels=None,flag_ave_label=False):
        self.__datafile = datafile
        self.__figfile = figfile
        self.__readfile(datafile=datafile,columns=cols)
        self.__trim = trim
        self.__flag_ave_label = flag_ave_label
        print("#################",self.__flag_ave_label)
        if labels is not None:
            self.__labels = labels

    def __readfile(self,datafile="score.csv",columns=[0]):
        self.__columns = columns
        self.__data = pandas.read_csv(datafile,header=None,encoding='utf-8',skipinitialspace=True,sep='\t',usecols=columns)
        self.__data.columns = [i for i in range(len(self.__data.columns))] # rename columns as sequence number
        self.__average = self.__data.mean()
        if self.__trim:
            for i in self.__data.columns:
                self.__data[i] = self.__data[i].apply(self.__trim)

    def __trim(self,_x):
        if _x < 0: return 0
        if _x > 100: return 100
        return _x



    def plot(self):
        if self.__flag_ave_label:
            for i in range(len(self.__labels)):
                self.__labels[i] = self.__labels[i] + "(" + str(self.__average[i]) + ")"
        font = {'family': 'Meiryo'}
        #font = {'family': 'Osaka'}
        matplotlib.rc('font', **font)
        cmap = plt.get_cmap("tab10")
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.set_xticks(range(0,110,10))
        ax.set_xlabel('score')
        ax.set_ylabel('number of people')
        ax.set_xlim([0,100])
        #ax.hist(self.__data.values,range=(0,100),rwidth=1.0)
        ax.hist(self.__data.values,range=(0,100))
        for i in self.__data.columns:
            ax.axvline(self.__average[i],color=cmap(i),alpha=0.5)
        try:
            plt.legend(self.__labels)
        except:
            pass
#        plt.show()
        plt.savefig(self.__figfile)
        subprocess.Popen("open "+self.__figfile,shell=True)


if __name__ == '__main__':
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,argparse.MetavarTypeHelpFormatter):
        pass
    parser = argparse.ArgumentParser(description="Plot score.",epilog="example: ./plot_bin.py --columns 0 2 --labels \"テスト\" \"総合\"", formatter_class=CustomFormatter)
    parser.add_argument('--file', '--datafile', type=str, dest='datafile', nargs=1, default='score.csv', help="input file")
    parser.add_argument('--fig','--figfile', type=str, dest='figfile', nargs=1, default='score.png', help="output figure file (png)")
    parser.add_argument('--columns','--cols', type=int, dest='columns', nargs='+', default=[0], help="column of data")
    parser.add_argument('--labels', type=str, dest='labels', nargs='+', default=None, help="title column")
    parser.add_argument('--avelabels', action="store_true", dest='flagavelabel', help="add average value to labels")
    parser.add_argument('--notrim', action="store_false", help="do not round-up/down score")
    parser.add_argument('--sep', type=str, dest='sep', nargs=1, default='\t', help="specify data separater in datafile")

    args = parser.parse_args()

    stat_inst = ReadPlot(datafile=args.datafile,figfile=args.figfile,cols=args.columns,sep=args.sep,trim=args.notrim,labels=args.labels,flag_ave_label=args.flagavelabel)
    stat_inst.plot()
