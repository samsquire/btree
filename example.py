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
inserted = [1,2,3,4]
for i in range(5, 100):
    root = root.insert(i, str(i))
    inserted.append(i)


walk(root)

print(root.children)

def keysonly(items):
    for item in items:
        yield item.key

assert sorted(list(keysonly(root.walk()))) == list(keysonly(root.walk()))
assert sorted(list(keysonly(root.walk()))) == sorted(inserted)

root = BTree(False, 3, 0, None)
inserted = []

seen = {}

for i in range(1, 100):
    num1 = random.randint(0, 100)
    if num1 not in seen:
        seen[num1] = True
        inserted.append(num1) 
        root = root.insert(num1, str(num1))



walk(root)

for item in root.walk():
    print(item.key, item.value)

assert sorted(list(keysonly(root.walk()))) == list(keysonly(root.walk()))
assert sorted(list(keysonly(root.walk()))) == sorted(inserted)

print("search test")
for item in root.search(25, 30):
    comparisons, child = item
    print(comparisons, child.key)

print(root.find_exact(30))
