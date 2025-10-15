def fibo(a,b,l,i):
    if(i<l):
        #print("\nbefore\na: ",a,"\tb: ",b)
        print(a+b)
        x=a+b
        a=b
        b=x
        i+=1
        #print("\nafter\na: ",a,"\tb: ",b)
        fibo(a,b,l,i)
l=int(input("\nenter the limit: "))
if l==0:
    print("\n0 limit")
elif l==1:
    print(0)
elif l==2:
    print(0)
    print(1)
else:
    print(0)
    print(1)
    fibo(0,1,l,2)