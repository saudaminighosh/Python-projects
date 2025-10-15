n=int(input("\nenter size: "))
a=[]
for i in range(n):
    x=int(input("\nenter array value: "))
    a.append(x)
maxi=a[n-1]
res=[]
for i in range(n-1,-1,-1):
    if i==n-1:
        res.append(a[i])
    else:
        if a[i]>=maxi:
            maxi=a[i]
            res.append(a[i])
res.reverse()
print(res)