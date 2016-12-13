#!/usr/bin/env python
# encoding: utf-8

'''
因为dict无排序概念，所以返回list
return list, each item is a tuple
'''
def sort_dict(dic, by_key = True):
    # 按照key排序，从小到大
    if by_key == True:
        l = sorted(dic.iteritems(), key=lambda d:d[0], reverse=False)
    else:
        l = sorted(dic.iteritems(), key=lambda d:d[1], reverse=False)
    return l

def test_sort_dict():
    d = {'hello': 'world', 'I': 'miss you', 'me': 'too'}
    print d  # d是无序的
    l = sort_dict(d)  #l是有序的
    print l
 
if __name__ == '__main__':
    test_sort_dict()    
