# --coding:utf8--
from __future__ import unicode_literals
import itertools

def f1(n):
    if n == 1:
        return 1
    return f1(n-1) * n

f1(10)
