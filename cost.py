n=int(input("\nenter size: "))
a=[]
for i in range(n):
    x=int(input("\nenter array value: "))
    a.append(x)
a.sort()
cost=int(input('\nenter the cost: '))
sum1=0
res=0
count=0
for i in range(n):
    if sum1<cost:
        sum1+=a[i]
        if res<cost:
            res+=sum1
            count+=1
        print("\nres: ",res)
    else:
        break
print("\nThe length is: ",count)