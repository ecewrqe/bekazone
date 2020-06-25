import re
res = re.sub("[0-9]+", "4444", "aaa,222,ccc,333,ppp", 1)
print(res)