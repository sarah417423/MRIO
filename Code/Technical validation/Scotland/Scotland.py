import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
path="/Users/ceri/Documents/Research/OMPTEC/test_code/MRIO-main/Code"
os.chdir(path+'Technical validation/Scotland')
fin=pd.read_excel('Scotland_2008.xlsx',sheet_name='IxI_2008')
sector_index=pd.read_excel('Scotland_2008.xlsx',sheet_name='sector_index',header=None)
sector_columns=sector_index
fin.index=list(range(len(fin)))
fin=fin.assign(nace=list(sector_index[0]))
agg_fin=fin.groupby(['nace']).sum()
agg_fin=agg_fin.T
agg_fin=agg_fin.assign(nace_=list(sector_columns[0]))
agg_fin=agg_fin.groupby(['nace_']).sum()
target_sum=agg_fin

fi1b=pd.read_excel('UKM-.xlsx',index_col=0)
ours_sum=fi1b
MAD=abs(ours_sum-target_sum).mean().mean()
DISM=(abs(ours_sum-target_sum)/(ours_sum+target_sum+0.0001)/2).mean().mean()
    
data1=np.array(agg_fin).reshape(10*10,)
data2=np.array(fi1b).reshape(10*10,)
print('MAD:'+str(MAD))
print('DISM'+str(DISM))
print(pearsonr(data1,data2))