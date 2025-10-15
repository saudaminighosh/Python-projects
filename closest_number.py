import math
n=int(input("\nenter n: "))
m=int(input("\nenter m: "))
a=n//m
b=a*m
c=math.ceil(n/m)
d=c*m
if (abs(n-b) < abs(n-d)):
    print(b)
elif (abs(n-b) > abs(n-d)):
    print(d)
else:
    if abs(b) > abs(d):
        print(b)
    else:
        print(d)