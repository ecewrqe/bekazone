import logging
def b1(num):
    if num>=10:
        print("大")
    else:
        print("小")
    pass
def al(num):
    print("hello,%s"%num)
    num += 1
    if num < 10:
        al(num)
    print("good bye, %s"%num)
def factor(max,):
    if max==1:
        return 1
    return max*factor(max-1)
a=factor(3)
print(a)