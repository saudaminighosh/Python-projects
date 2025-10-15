from collections import defaultdict
n=int(input("\nenter size: "))
a=[]
for i in range(n):
    x=(input("\nenter array value: "))
    a.append(x)
anagram=defaultdict(list)
res=[]
for i in range(n):
    b=[0]*26
    for j in range(len(a[i])):
        b[ord(a[i][j])-ord("a")]+=1
    anagram[tuple(b)].append(a[i])
print(list(anagram.values()))