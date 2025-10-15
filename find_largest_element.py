def largest(a,i):
    if i==len(a)-1:
        return a[i]
    x=largest(a,i+1)
    return max(a[i],x)

def find(a):
    return largest(a,0)

n=int(input("\nenter size: "))
a=[]
for i in range(n):
    b=int(input("\nenter array value: "))
    a.append(b)
print("\nlargest value is:\n")
print(find(a))