"""

ICD-9 Ontology

author: Jacky Chen
E-mail: jacky.c.top@gmail.com

"""
from Concept import Concept
import xlrd


class ICD_9_Ontology:
    """
    This class defines a partially ordered set of ICD-9 concepts.
    The concepts are organized into a concept tree, related by parent and descendant.

    """


    def __read(self):
        """
        Private function.
        Read data from xls file and store the data in list

        :return: non-fine-grained(list)
                fine-grained(list)
        """
        nfg_path = 'E:\pycharm\postgres-database-20180304\ICD_9\\nfg.xls'
        non_fine_grained = xlrd.open_workbook(nfg_path)
        fg_path = 'E:\pycharm\postgres-database-20180304\ICD_9\\fg.xls'
        fine_grained = xlrd.open_workbook(fg_path)
        sheet1 = non_fine_grained.sheets()[0]
        sheet2 = fine_grained.sheets()[0]
        nfg = []
        fg = []
        nrows1 = sheet1.nrows
        nrows2 = sheet2.nrows
        for i in range(nrows1):
            cid = sheet1.row_values(i)[0]
            cd = sheet1.row_values(i)[1]
            nfg.append((cid, cd))
        for i in range(nrows2):
            cid = sheet2.row_values(i)[0]
            cd = sheet2.row_values(i)[1]
            fg.append((cid, cd))
        return nfg, fg

    def __link(self, ancestor, descendant):
        """
        Private function
        link two concepts together
        :param ancestor:
        :param descendant:
        :return:
        """
        if descendant == None:
            ancestor.descendants = None
            return
        ancestor.descendants.append(descendant)
        descendant.ancestor = ancestor

    def __extract_code(self, concept):
        """
        Extract the ICD-9 code of a concept tuple (cid, description)
        :param concept:
        :return cid:
        """
        _cid = concept[0]
        cid = ''.join(_cid.split('.'))
        return cid

    def __duplicate_judge(self, concept):
        """
        Check if the concept has been in the list of record
        :param concept:
        :return ancestor:
        """
        if concept not in self.__record:
            # if not record, then record it
            ancestor = Concept(concept[0], concept[1])
            self.concepts.append(ancestor)
            self.__record.append(concept)
        else:
            # record, then return it
            ancestor = [obj for obj in self.concepts if obj.cid == concept[0]]
            ancestor = ancestor[0]
        return ancestor

    def __correct_token(self, concept):
        """
        For several cases, there exist dislocation of token.
        This function is used for token correction
        :param concept:
        :param token:
        :return token:
        """
        length_fg = len(self.fg)
        cid = self.__extract_code(concept)
        while True:
            if self.token >= length_fg:
                break
            next = self.fg[self.token]
            next_cid = self.__extract_code(next)
            if (len(cid) == 4 and len(next_cid) == 4 and cid[0:3] == next_cid[0:3]): # sibling nodes
                if next_cid[0] == 'E' and len(next_cid) == 4:
                    a = Concept(next[0], next[1])
                    self.concepts.append(a)
                    self.__record.append(next)
                    self.__link(self.Root, a)

                self.token += 1
            elif (len(cid) == 3 and len(next_cid) == 4 and cid > next_cid[0:3]): # previous concepts
                self.token += 1
            elif len(next_cid) == 3:  # fine-grained concept but has no parents except for root
                a = Concept(next[0], next[1])
                self.concepts.append(a)
                self.__record.append(next)
                self.__link(self.Root, a)
                self.token += 1
            elif next_cid[0] == 'E' and len(next_cid) == 4:
                a = Concept(next[0], next[1])
                self.concepts.append(a)
                self.__record.append(next)
                self.__link(self.Root, a)
                self.token += 1
            elif next_cid[0] == 'E' and len(next_cid) == 4: # fine-grained concept begun with E but has no parents
                self.token += 1
            else:
                break



    def __search_sub_concept_in_nfg(self, length_nfg, cid, ancestor):
        while True:
            self.token_1 += 1
            if self.token_1 >= length_nfg:
                break
            next = self.nfg[self.token_1]
            next_cid = self.__extract_code(next)
            if cid == next_cid[0:3]:
                descendant = Concept(next[0], next[1])
                self.concepts.append(descendant)
                self.__record.append(next)
                self.__link(ancestor, descendant)
            else:
                break

    def __search_sub_concept_in_fg(self, length_fg, cid, concept, ancestor):
        while True:
            self.__correct_token(concept)
            if self.token >= length_fg:
                self.token = self.back_point
                break

            next = self.fg[self.token]
            next_cid = self.__extract_code(next)

            if (len(cid) == 3 and len(next_cid) == 4 and cid == next_cid[0:3]) \
                    or (len(cid) == 4 and len(next_cid) == 5 and cid == next_cid[0:4]):
                descendant = Concept(next[0], next[1])
                self.concepts.append(descendant)
                self.__record.append(next)
                self.__link(ancestor, descendant)
                self.token += 1
            elif (len(cid) == 3 and len(next_cid) == 5 and cid == next_cid[0:3]):
                if self.flag == True:
                    self.back_point = self.token
                    self.flag = False
                self.token += 1
                continue
            else:
                if self.flag == False:
                    self.token = self.back_point
                break


    def __search_sub_concept(self, concept):
        """
        Search for sub-concept for each non-fine-grained concept
        :param concept:
        :return:
        """
        ancestor = self.__duplicate_judge(concept)
        self.token_1 = self.nfg.index(concept)
        cid = self.__extract_code(concept)
        length_nfg = len(self.nfg)
        length_fg = len(self.fg)
        self.__search_sub_concept_in_nfg(length_nfg, cid, ancestor)
        self.__search_sub_concept_in_fg(length_fg, cid, concept, ancestor)


    def __init__(self):
        """
        Initial function
        Generate the ontology.

        """

        """
        private members:
            1. concepts ----> concept list(elements are Concept object)
            2. __record ----> record list(elements are tuple)
            3. Root --------> Root node of the whole tree
        """
        self.concepts = []
        self.__record = []
        self.Root = Concept('0', None)

        self.nfg, self.fg = self.__read()
        self.token = 0
        self.token_1 = 0
        self.back_point = 0

        for concept in self.nfg:
            self.flag = True
            self.__search_sub_concept(concept)

        for concept in self.concepts:
            if concept.ancestor == None:
                self.__link(self.Root, concept)
        self.concepts.append(self.Root)
        self.__record.append(('0',None))

    def get_concept_by_cid(self, cid):
        select = [concept for concept in self.concepts if concept.cid == cid]
        return select[0]

    def get_concept_by_description(self, cd):
        select = [concept for concept in self.concepts if concept.description == cd]
        return select[0]
















