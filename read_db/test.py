from func import get_alpha, get_radius, get_area, get_distance
from fp import fixed_point
import csv

f = open("rssi_values (2).csv")

lst_p = []
lst_r = []
for line in f:
    lst_p.append(line[2])
    loc = fixed_point(line[3])
    lst_r.append(get_distance(loc[0], loc[1], int(line[6]), int(line[7])))

lst = zip(lst_p, lst_r)
lst = sorted(lst, key=lambda tup:tup[0], reverse=True)
lst = lst[0:3]
lst = zip(*lst)
lst_p = lst[0]
lst_r = lst[1]
print get_alpha(lst_p, lst_r)
