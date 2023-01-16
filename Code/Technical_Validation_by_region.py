# by country
import os
import numpy as np
import pandas as pd
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Data collection/EuroStats/PBL-EUREGIO-2000-2010-XLSB")

regio=pd.read_excel("RegionalIOtable_2008.xlsx",sheet_name='2008',header=None)

rows=regio.iloc[:,0:3]
labels=rows.iloc[3:3727]
labels[1]

prior=regio.iloc[3:3727,:]
prior=prior.iloc[:,3:3736]
#prior.assign(geo=labels[1])
#index_label=labels[1]+'-'+labels[2]
# prior.index=index_label
# prior.columns=index_label

os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method")
target=pd.read_excel("SRIO_compare.xlsx",sheet_name='target')
ours=pd.read_excel("SRIO_compare.xlsx",sheet_name='ours')
sector_1=target.sector
sector_2=ours.Sector
# os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/MRIO")
# esti13=pd.read_excel('MRIO_2008 _272regions_0712.xlsx',index_col=0)

geo1=list(labels[1].unique())
#geo2=list(pd.read_excel('N_trade_sec_2010_A.xlsx',index_col=0).index)
#geo1=list(s.index)
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
esti=pd.read_excel('MRIO_2008 _272regions_0712.xlsx', index_col=0)
nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
index_label=[]
rgeo_label=[]
nace_label=[]  
rows=pd.Series(esti.index).str.split('-',expand=True)
final=rows[0].unique()             
for i in range(10):
    for j in range(len(final)):
        tmp=final[j]+'-'+nace[i]
        index_label.append(tmp)
        rgeo_label.append(final[j])
        nace_label.append(nace[i])
esti_label=pd.DataFrame({'label':index_label,'rgeo':rgeo_label,'nace':nace_label})
esti_loc=esti_label.sort_values('label').index
esti_label2=esti_label.iloc[esti_loc,:]    
     
df_trade_flow=esti.T
df_trade_flow.index=list(range(len(df_trade_flow)))
df_trade_flow.columns=list(range(len(df_trade_flow)))
df_trade_flow=df_trade_flow.assign(rgeo=list(esti_label2['rgeo']))
agg=df_trade_flow.groupby(['rgeo']).sum()
agg=agg.T


col_names = ['rgeo','MAD','MEAN','MRAD','MPE','SD','DISM','corr','p']
corr_result=[]
df_corr = pd.DataFrame(corr_result,columns=col_names)
from scipy.stats import pearsonr
import math
for n in range(len(loc1)):
    print(n)
    matching1=labels[1]==geo1[loc2[n]]
    matching=[i for i,x in enumerate(matching1) if x]
    target=prior.iloc[matching,:].iloc[:,matching]
    target=target.assign(Sector=list(sector_1))
    industry_sum=target.groupby(['Sector']).sum()
    industry_sum=industry_sum.T
    df3=industry_sum.assign(Industry_=list(sector_1))
    industry_sum=df3.groupby(['Industry_']).sum()
    target_sum=industry_sum.T/1.47
    
    matching2=esti_label.rgeo==geo2[loc1[n]]
    matching=[i for i,x in enumerate(matching2) if x]
    ours=esti.iloc[matching,:].iloc[:,matching]
    ours=ours.assign(Sector=list(sector_2))
    industry_sum=ours.groupby(['Sector']).sum()
    industry_sum=industry_sum.T
    df3=industry_sum.assign(Industry_=list(sector_2))
    industry_sum=df3.groupby(['Industry_']).sum()
    ours_sum=industry_sum.T
    

    MAD=abs(ours_sum-target_sum).mean().mean()
    MEAN=(ours_sum-target_sum).mean().mean()
    MRAD=(abs(ours_sum-target_sum)/target_sum).mean().mean()
    MPE=((ours_sum-target_sum)/target_sum).mean().mean()
    STPE=(ours_sum-target_sum).sum().sum()/(target_sum.sum().sum())
    #RAD
   
    
    SD=pow((abs(ours_sum-target_sum)/target_sum-MRAD).mean().mean(),0.5)

#     AED=abs(ours_sum*math.log(ours_sum)-target_sum*math.log(target_sum))
    DISM=(abs(ours_sum-target_sum)/(ours_sum+target_sum+0.0001)/2).mean().mean()
    
    data1=np.array(target_sum).reshape(7*7,)
    data2=np.array(ours_sum).reshape(7*7,)
    corr,p=pearsonr(data1,data2)
    
    new_data = pd.DataFrame({'rgeo':geo1[loc2[n]],'MAD':MAD,'MEAN':MEAN,'MRAD':MRAD,'MPE':MPE,'SD':SD.real,'DISM':DISM,'corr':corr,'p':p},index=[str(n)]) 
    df_corr = pd.concat([df_corr,new_data],axis=0)   

  
os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Technical validation")
#df_corr.to_excel('df_corr_2008_0712.xlsx')
df_corr_.to_excel('df_corr_'+yesr+'.xlsx',index_col=0)