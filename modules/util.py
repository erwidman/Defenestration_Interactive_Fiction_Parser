#https://stackoverflow.com/questions/9501337/binary-search-algorithm-in-python
def binary_search(array, target):
    lower = 0
    upper = len(array)
    while lower < upper:   # use < instead of <=
        x = lower + (upper - lower) // 2
        val = array[x]
        if target == val:
            return x
        elif target > val:
            if lower == x:   # these two are the actual lines
                break        # you're looking for
            lower = x
        elif target < val:
            upper = x


def customPrint(string):
    tmpbuffer="\n   "
    index=0

    for c in string:
        tmpbuffer+=("%c"%c)
        if index>75 and c==' ' or index==89:
            print(tmpbuffer)
            index=0
            tmpbuffer="   "
        elif c == '\n':
            index=0
        else:
            index+=1
    print("%s\n" % tmpbuffer)

def failPrint():
    customPrint("Not sure what that means.")