#%%
from tabulate import tabulate
from functions import *
from pprint import pprint
df = pd.read_excel('basic/example.xlsx',sheet_name='其他', index_col='姓名')
life_dct2 = {ii: df.loc[ii,:].to_list() for ii in df.index}
#pprint(life_dct2.keys())
#print(life_dct2['李建佑'])

print(tabulate(combine_star(life_dct2['陳韻旻']),  tablefmt='psql'))


#def flow_star():
#    """
    
#    """
#    pass


# year_span
# annual_span #小限 ## (要配合流年)
# decade_span #大限 ## (要配合流年)