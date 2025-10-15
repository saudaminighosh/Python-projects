'''def binarySearch(a,key,st,en):
    if st<=en:
        m=st+(en-st)//2
        print("\nValue of m is : ",m)
        if a[m]==key:
            return 1
        elif a[m]<key:
            return binarySearch(a,key,m+1,en)
        else:
            return binarySearch(a,key,st,m-1)
    else:
        return -1
n=int(input("\nenter size: "))
a=[]
for i in range(n):
    b=int(input("\nenter array value: "))
    a.append(b)
key=int(input("\nenter the element to search: "))
res=binarySearch(a,key,0,n-1)
if res==1:
    print("\nelement found")
else:
    print("\nelement not found ")'''

def binarySearch(a,key,st,end,size):
    if st==size or end==0 or st==end:
        return -1
    x=(end-st)
    m=st+(x//2)
    print("\nValue of m is : ",m)
    if a[m]==key:
        return 1
    elif a[m]>key:
        return binarySearch(a,key,st,m,size)
    else:
        return binarySearch(a,key,m+1,size,size)


n=int(input("\nenter size: "))
a=[]
for i in range(n):
    b=int(input("\nenter array value: "))
    a.append(b)
key=int(input("\nenter the element to search: "))
res=binarySearch(a,key,0,n,n)
if res==1:
    print("\nElement Found")
else:
    print("\nNot found")