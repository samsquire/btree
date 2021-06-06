import bisect
import random

class BTree():
    def __init__(self, leaf, M, key, value, parent=None):
        self.leaf = leaf
        self.children = []
        self.M = M
        self.key = key
        self.value = value
        self.parent = parent
    
   
    def walk(self):
        for child in self.children:
            
            if child.leaf:
                yield child
            yield from child.walk()
        
    def __repr__(self):
        return "{}:{}".format(self.key, self.value)

    def __str__(self):
        return "{}:{}".format(self.key, self.value)

    def find_exact(self, key):
        leaf, last_child, parents = self.find(key)
        if leaf.key == key:
            return leaf
        return None

    def find(self, key):
        leaf = self
        next_children = self.children
        last_child = self
        child = None
        parents = [self]
        found = False
        while found == False:
            next_children_changed = False
            for child in reversed(next_children):
                if key >= child.key:
                    # print("Inspecting {} <= {} ".format(child.key, key))
                    next_children = child.children
                    
                    last_child = leaf
                    parents.append(child)
                    leaf = child
                    next_children_changed = True
                    break
                    
                    
                        
                        
            if not next_children_changed:
                found = True

        return leaf, last_child, parents
                
        
        
    def insert(self, key, value, height=1, parent=None):
        
        leaf, last_child, parents = self.find(key) 
        leaf = last_child
        
        # print("Trying to insert {} at Found insertion leaf {}".format(key, leaf))
        # walk(leaf)
        
        
        if len(leaf.children) < leaf.M:

            leaf.insert_non_full(key, value, parents[-1])
            
        else:
            # we need to split
            current = leaf
            bottom = leaf

            inserted = False
            new_root = None
            
            
            while current != None:
                
                
                original_parent = current.parent
                bottom_is_too_big = current == bottom and len(current.children) >= current.M
                if bottom_is_too_big or len(current.children) > current.M:
                    


                    
                    new_left, new_right, separation_value = current.split()
                                      

                    if original_parent == None:
                        
                        new_root = BTree(False, self.M, 0, None)
                        
                        parent = new_root
                        

                        new_root.children.append(new_left)
                        
                        new_root.children.append(new_right)
                        
                        new_root.key = new_right.key
                        new_root.value = new_right.value
                        

                    else:
                        
                        parent = original_parent
                        print("Embedded split {}".format(current.key)) 
                        original_parent.children.remove(current)
                        original_parent.children.append(new_left)
                        
                        original_parent.children.append(new_right)
                        original_parent.sort()
                   
                        
                

                    new_left.parent = parent
                    new_right.parent = parent
                    
                    assert new_right.key > new_left.key
                        
                    

                



                
                current = original_parent

                
                
            
            if new_root != None:
                # split went to root
                print("Split went to root")
                
                # walk(new_root)
                return new_root.insert(key, value)
            else:
                
                return self.insert(key, value)
            return self
            
            
        
        return self
            
        
            

    def split(self):

        
        new_self = BTree(True, self.M, 0, None)
        new_self.key = self.key
        new_self.value = self.value
        new_left = BTree(False, self.M, 0, None)
        new_sibling = BTree(False, self.M, 0, None)
        midpoint = int((len(self.children)+1)/2)

                
        left_children = []
        if self.leaf:
            left_children = [new_self]

        left_children = left_children + self.children[0:midpoint]
        right_children = self.children[midpoint:]
        for child in left_children:
            child.parent = new_left
        for child in right_children:
            child.parent = new_sibling

        new_sibling.key = right_children[0].key
        new_sibling.value = right_children[0].value

        new_left.children = left_children
        new_sibling.children = right_children

        new_left.leaf = False

        new_left.key = left_children[0].key
        new_left.value = left_children[0].value

        return new_left, new_sibling, self.children[midpoint].key


                
        
    def insert_after_split(self, key, value, parent):
        height = height + 1
        
        
        insertion_point, index = self.find_location_for_key(key)

        if insertion_point == None:
            self.insert_non_full(key, value, parent)
        else:
            split = insertion_point.insert(key, value, parent=self)

            return split
        
        return self
    
    def insert_non_full(self, key, value, parent):
        values = [child.key for child in self.children]
        new_pos = bisect.bisect(values, key)
        self.children.insert(new_pos, BTree(True, self.M, key, value, parent))
        return self

    def sort(self):
        self.children.sort(key=lambda x: x.key)
    
    def find_location_for_key(self, key):
        index = None
        for child in self.children:
            if cmp(key, child.key) >= 0:
                  index = child, self.children.index(child)
        if index:
            return index
        else:
            return None, -1
    
    def search(self, greater_than_equal, less_than, comparisons=0):
         
            
        for child in self.children:
            if child.key <= less_than:
                if child.leaf:
                    if child.key >= greater_than_equal: 
                        yield comparisons + 1, child
                        yield from child.search(greater_than_equal, less_than, comparisons + 1)
                else:
                    yield from child.search(greater_than_equal, less_than, comparisons + 1)
    
    def delete(self, key):
        deletion_point, index = self.find_location_for_key(key)
        if deletion_point:
            if deletion_point.key == key:
                self.children.remove(deletion_point)
                return True
            else:
                return deletion_point.delete(key)
        else:
            return False
