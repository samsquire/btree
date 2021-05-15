from btree import BTree    
import random

def walk(item, spaces=0):
    
    print("{}{}={} {} {}".format(" " * spaces, item.key, item.value, "leaf" if item.leaf else "", item.parent))
    
    for child in item.children:
        walk(child, spaces + 1)

root = BTree(False, 3, 0, None)\
.insert(1, "1")\
.insert(2, "2")\
.insert(3, "3")\
.insert(4, "4")

for i in range(5, 100):
    root = root.insert(i, str(i))


walk(root)

print(root.children)

def keysonly(items):
    for item in items:
        yield item.key

assert sorted(list(keysonly(root.walk()))) == list(keysonly(root.walk()))

root = BTree(False, 3, 0, None)


seen = {}

for i in range(1, 100):
    num1 = random.randint(0, 100)
    if num1 not in seen:
        seen[num1] = True
    
        root = root.insert(num1, str(num1))



walk(root)

for item in root.walk():
    print(item.key, item.value)

assert sorted(list(keysonly(root.walk()))) == list(keysonly(root.walk()))
