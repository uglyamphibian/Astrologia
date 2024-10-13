#%%
from tabulate import tabulate
from functions import *
from pprint import pprint
from flow_compute import *
import re



 

ex = life_dict['楊貴妃']
Z = combine_star(ex,'f')
 
#v = combine_flow(ex,'m',42)
#print(v)
#
#print(tabulate(v,tablefmt='psql'))
#u = combine_flow(ex, 'm', 67)
#pprint(tabulate(u,tablefmt='psql'))
#print(tabulate(u, tablefmt='simple'))
print('\n========================\n')
print(tabulate(Z,tablefmt='psql'))
#u = combine_flow(ex, 'm', 67)



# for jj in v:
#     if isinstance(jj,list):
#             new_txt = '\n'.join(jj)
#     else:
#             new_txt = jj
#     print(new_txt)
    





 