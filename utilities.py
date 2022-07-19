from log import *



def saveListToFile(filename: str,list: list , encoding: str):

    Log.info('Saving list to file ' + filename)
    f = open(filename,'a+',encoding=encoding)
    for i in list:
        f.write(str(i).strip() + '\n' )
    f.close()


def loadListFromFile(filename: str , encoding: str):

    l = []
    Log.info('loading list from file ' + filename)
    f = open(filename, 'r', encoding=encoding)
    for i in f:
        l.append(i.strip())
    f.close()
    return l


def removeDUPfromFile(filename: str , encoding: str):
    try:
        list = []
        f = open(filename,'r')
        for i in f:
            list.append(i.strip())
        newList = dict.fromkeys(list)
        f.close()
        a = open(filename,'w+',encoding=encoding)
        for i in newList:
            a.write(i.strip() + '\n')
        a.close()
    except:
        pass



