'''
Given a String which supposedly represents an integer in base sixteen (hex), 
return the conversion to base ten.  
You may only use basic arithmetic operators (+, -, *, /, %).  
If the String is an invalid base sixteen number, then return the language's version of null.
The algorithm must execute in a time complexity of O(n), where n is the number of letters in the String.   Other complexities will get partial credit.
 
Note: Hex numbers may start with 0x or not.
 
For example:
String = "122" => 290
String = "0x122" => 290
String = "a12" => 2578
String = "ga4" => None
String = "0xze1" => None
String = "0g122" => None
'''
def hex_to_dec(hex):
    hex = hex.lower().strip("0x")
    hexchars = [n[1] for n in enumerate("0123456789abcdef")]
    
    hexdict = dict()
    j = 0
    for i in hexchars:
        hexdict.update({i : j})
        j += 1

    sum = 0
    n = 1

    for i in range(len(hex) - 1):
        n *= 16

    for i in hex:

        val = hexdict.get(i)
        if val == None:
            return None

        sum += (n * val)
        n /= 16

    return int(sum)

'''
Given the head to a sorted singular linked list, remove all nodes with duplicate values.
Your algorithm must only complete one pass through the linked list.
More than one pass will get partial credit.
 
Additionally: Define the Node type of the linked list nodes.
Your function should take one of these as your parameter.

1->2->2->3->3->4->4->5
1->5

1->1->2->3->4->4->4->5->5
2->3
'''

def remove_dupes(root):
    def find_first_non_duplicate(curr):
        if curr.next == None:
            return None
        
        while curr.next.next != None:
            if curr.data == curr.next.data or curr.next.data == curr.next.next.data:
                curr = curr.next
            else:
                return curr.next

        if curr.data == curr.next.data:
            return None
        else:
            return curr.next
        
    if root == None:
        return None
    
    if root.next != None:
        if root.data == root.next.data:
            root = find_first_non_duplicate(root)

    curr = root
    while curr != None:
        curr.next = find_first_non_duplicate(curr)

        curr = curr.next

    return root



def traverse(root):
    curr = root
    while curr != None:
        print(str(curr.data) + " -> ", end="")
        curr = curr.next
    print("\n")


class LLNode:
    def __init__(self):
        self.data = None
        self.next = None

h = LLNode()
h.data = 5

g = LLNode()
g.data = 5
g.next = h

f = LLNode()
f.data = 4
f.next = g

e = LLNode()
e.data = 4
e.next = f

d = LLNode()
d.data = 4
d.next = e

c = LLNode()
c.data = 3
c.next = d

b = LLNode()
b.data = 1
b.next = c

a = LLNode()
a.data = 1
a.next = b

r = LLNode()
r.data = 1
r.next = a

r = remove_dupes(r)
traverse(r)

'''
Given the node to a k-ary tree holding integers,
calculate the average value contained within the tree.
 
Additionally: Define the Node type of the k-ary tree nodes.
Your function should take one of these as your parameter.
'''

def get_avg_kary_tree(root):  
    def traverse_children(curr, total, count):
        for i in curr.children:
            vals = traverse_children(i, total + i.data, count + 1)
            total = vals[0]
            count = vals[1]

        return [total, count]
    
    vals = traverse_children(root, root.data, 1)
    return vals[0] / vals [1]


class KaryNode:
    def __init__(self):
        self.data = None
        self.children = []
    
d = KaryNode()
d.data = 1

e = KaryNode()
e.data = 3

f = KaryNode()
f.data = 2

g = KaryNode()
g.data = 15

h = KaryNode()
h.data = 22

i = KaryNode()
i.data = 1

a = KaryNode()
a.data = 7
a.children = [d, e]

b = KaryNode()
b.data = 4
b.children = [f]

c = KaryNode()
c.data = 8
c.children = [g, h, i]

root = KaryNode()
root.data = 12
root.children = [a, b, c]

#print(get_avg_kary_tree(root)) #should be 7.5
