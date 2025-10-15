'''def fact(n):
    if n>0:
        return n*fact(n-1)
    else:
        return 1
n=int(input("\nenter value: "))
res=fact(n)
print(res)'''
def display(i,n):
    if i<=n:
        print("\t",i)
        display(i+1,n)
        print("\t",i)
n=int(input("\nenter value: "))
display(1,n)
