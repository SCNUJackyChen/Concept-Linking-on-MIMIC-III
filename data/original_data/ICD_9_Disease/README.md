# ICD-9-code
API for fast query for ICD-9 codes
## Introduction of ICD-9 code
>The International Classification of Diseases, Ninth Revision, Clinical Modification (ICD-9-CM) is based on the World Health Organization's Ninth Revision, International Classification of Diseases (ICD-9). ICD-9-CM is the official system of assigning codes to diagnoses and procedures associated with hospital utilization in the United States.
>
>from wiki

ICD-9 code contains about 17500 concepts in total, which are organized in a tree-like structure.                    
The relationship between a ancestor concept and its descendant concept is father-and-son, indicated by their IDs' length.                     
E.g '003' is the parent concept of '003.2' and so on, '003.2' is the parent concept of '003.28'
## How to use

This python library offers a convenient and fast method to inquiry any concept in ICD-9.                            
A concept mainly contains 4 attributes, which are:                     
       1) concept id                    
       2) concept description                     
       3) ancestor concept                        
       4) descendant concepts                        
                                   
                                          
All of the attributes have been encapsulated in the class object.
                                             
Initially, we need to build the ICD-9 Ontology:
```python
a = ICD_9_Ontology()

```
                        
Get a concept object by its cid:
```python
concept = a.get_concept_by_cid('001')
```

                    
Get a concept's information:
```python
concept.get() # return (cid, description)
```
                            
Get a concept's all ancestor:
```python
concept.get_all_ancestor() # return a list
```
                        
Get a concept's all descendants:
```python
concept.get_descendants()
```
                            
Check if a concept is a fine-grained concept:
*Definition*:*A fine-grained concept is a concept that has no descendant*
```python
concept.Is_fine_grained() # return True or False
```
                            
                            

                            
