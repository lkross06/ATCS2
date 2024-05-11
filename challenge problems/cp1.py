'''
Given two arrays, A and B, return the first element in A which is not in B.
If no such element exists, return the language's version of null.
Your function must run with an Average case time complexity of O(n),
where n is the maximum size of A and B.  Other complexities with receive partial credit.
'''
def first_element(a, b):
    bset = set(b)

    for i in a:
        if not(i in bset):
            return i

    return None

def most_often(a):
    a = a.lower()

    if len(a) == 0:
        return []

    adict = dict()
    for i in a:
        value = adict.get(i)
        if value != None:
            adict.update({i: value + 1})
        else:
            adict.update({i: 1})

    m = max(adict.values())

    rtn = []
    for key, val in adict.items():
        if val == m:
            rtn.append(key)

    return rtn    


def is_anagram(a, b):
    if len(a) != len(b):
        return False

    bdict = dict()
    for i in b:
        value = bdict.get(i)
        if value != None:
            bdict[i] = value + 1
        else:
            bdict[i] = 1

    for i in a:
        value = bdict.get(i)
        if value == None:
            return False
        elif value >= 1:
            bdict[i] = value - 1
        else:
            return False
    
    return True

A = "panda"; B = "dampa" 
print(is_anagram(A, B))