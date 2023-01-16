
import pandas as pd
import numpy as np
import random
import os
nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
# geo1=list(pd.read_excel('N_trade_sec_2010_A.xlsx',index_col=0).index)
s=0
geo1=list(pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[s],index_col=0).index)
path="/Users/ceri/Documents/Research/OMPTEC/Data Descripter/Code"
os.chdir(path)
nuts2_272=pd.read_excel('Abbreviation.xlsx',sheet_name='NUTS2')
geo2=list(nuts2_272['NUTS2'])
def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 

loc1=[]
for i in range(len(geo1)):
    t=index_of(geo1[i],geo2)
    if t!=-1:
        loc1.append(t)

loc2=[]
for i in range(len(geo2)):
    t=index_of(geo2[i],geo1)
    if t!=-1:
        loc2.append(t)

os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/MRIO")
#df_trade_flow_data=pd.read_excel('Trade Data EU 2013 ref.xlsx', sheet_name='B-E',index_col=0)
df_trade_flow_data=pd.read_excel('MRIO_2018 _272regions.xlsx', index_col=0)
nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
index_label=[]
rgeo_label=[]
nace_label=[]  
rows=pd.Series(df_trade_flow_data.index).str.split('-',expand=True)
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
final=pd.read_excel('final_list.xlsx')
final=list(final.iloc[:,1])         
for i in range(10):
    for j in range(len(final)):
        tmp=final[j]+'-'+nace[i]
        index_label.append(tmp)
        rgeo_label.append(final[j])
        nace_label.append(nace[i])
esti_label=pd.DataFrame({'label':index_label,'rgeo':rgeo_label,'nace':nace_label})
esti_loc=esti_label.sort_values('label').index
esti_label2=esti_label.iloc[esti_loc,:]    
     
df_trade_flow=df_trade_flow_data.T
df_trade_flow.index=list(range(len(df_trade_flow)))
df_trade_flow.columns=list(range(len(df_trade_flow)))
df_trade_flow=df_trade_flow.assign(rgeo=list(esti_label2['rgeo']))
agg=df_trade_flow.groupby(['rgeo']).sum()
agg=agg.T

os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
from scipy.stats import pearsonr
col_names = ['Sector','MAD','DISM','corr','p']
nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
corr_result=[]
df_corr = pd.DataFrame(corr_result,columns=col_names)

# df_trade_flow_data.index=list(np.arange(len(df_trade_flow_data)))
for s in range(10):
    s1=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[s],index_col=0)
    prior=s1.iloc[loc2,:].iloc[:,loc2]
    esti_label2.index=list(range(2720))
    matching1 = [k for k in esti_label2.index if esti_label2.nace[k]==nace[s]]
    esti=df_trade_flow_data.iloc[matching1,:].T
    esti_label2.index=esti.index
    esti=esti.assign(rgeo=esti_label2.rgeo)
    esti=esti.groupby(['rgeo']).sum()
    esti.columns=prior.columns
#     esti.index=prior.index
#     print(nace[s])
#     print(abs(esti-prior)/.mean().mean())
#     print((abs(esti-prior)/(esti+prior+0.0001)/2).mean().mean())
    esti=esti.fillna(0)
    prior=prior.fillna(0)
    
    MAD=abs(esti-prior).mean().mean()
    DISM=(abs(esti-prior)/(esti+prior+0.0001)/2).mean().mean()
    
    data1=np.array(esti).reshape(272*272,)
    data2=np.array(prior).reshape(272*272,)
    corr,p=pearsonr(data1,data2)
    
    new_data = pd.DataFrame({'Sector':nace[s],'MAD':MAD,'DISM':DISM,'corr':corr,'p':p},index=[str(s)]) 
    df_corr = pd.concat([df_corr,new_data],axis=0)  
    

os.chdir("/Users/ceri/Documents/Research/OMPTEC/Data descripter/Technical validation")
df_corr.to_excel('df_corr_0116.xlsx')

    


