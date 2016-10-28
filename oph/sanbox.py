# -*- coding: utf-8 -*-

def seq(start, stop, step = 1):
        n = int(round((stop - start) / float(step)))
        print "n: {}".format(n)
        if n > 1:
            return([start + step * i for i in range(n + 1)])
        else:
            return([])
if __name__ == '__main__':
	print seq(2,10, step=0.5)
