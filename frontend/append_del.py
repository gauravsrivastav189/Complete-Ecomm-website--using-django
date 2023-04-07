s='hackerhappy'
t='hackerrank'
k=9
for i in range(len(t)):
        if s[i]!=t[i]:
            a=i
            break;
#print(i)
#print(len(s))
for i in range(len(s)-i):
    s=s[0:len(s)-1]

#print(s)
b=len(t)
for i in range(a:b) :
    s=s[::] + t[i]
print(s)
s='abc'
print(s+'r')
