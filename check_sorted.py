n=int(input("\nenter size: "))
a=[]
for i in range(n):
    x=(input("\nenter array value: "))
    a.append(x)
sorted=True
for i in range(n-1):
    if a[i]>a[i+1]:
        sorted=False
        break
if sorted==True:
    print("\narray is sorted")
else:
    print("\narray NOT is sorted")