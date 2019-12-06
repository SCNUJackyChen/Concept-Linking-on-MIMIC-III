"""

ICD-9 code concept

author: Jacky Chen
E-mail: jacky.c.top@gmail.com

"""



class Concept:
    """
    This class defines a single concept in ICD-9 code.
    The set of these concepts is organized by a tree structure.


    private member:
        1. cid -----------> concept's ID
        2. description ---> description of this concept
        3. ancestor ------> the parent concept of this concept
        4. descendants ---> the descendant concepts of this concept

    """

    def __init__(self, cid, description):
        self.cid = cid
        self.description = description
        self.ancestor = None
        self.descendants = []

    def get(self):
        return self.cid, self.description

    def get_ancestor(self):
        if self.ancestor != None:
            return self.ancestor
        else:
            return None
    def get_descendants(self):
        if self.descendants != None:
            return self.descendants
        else:
            return None


    # Definition: A fine grained concept is a concept which has no descendant concept


    def Is_fine_grained(self):
        if self.descendants == []:
            return True
        else:
            return False

    def Is_ancestor(self, check_concept):
        if check_concept == self.ancestor:
            return True
        else:
            return False

    def Is_descendants(self, check_concept):
        if check_concept in self.descendants:
            return True
        else:
            return False

    def Is_root(self):
        if self.cid == '0':
            return True
        else:
            return False

    def get_all_ancestor(self):
        lis = []
        cur = self
        while not cur.ancestor.Is_root():
            lis.append(cur.get_ancestor())
            cur = cur.ancestor
        return lis
