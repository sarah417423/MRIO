import os
import numpy as np
import pandas as pd
import os
import pandas as pd
path="/Users/ceri/Documents/Research/OMPTEC/Data Descripter"
os.chdir(path)
ISO_list=pd.read_excel('Abbreviation.xlsx',sheet_name='Country')
ISO3=ISO_list['ISO3']
ISO2=ISO_list['ISO2']

# os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
nuts2_272=pd.read_excel('Abbreviation.xlsx',sheet_name='NUTS2')
index=pd.read_excel('Abbreviation.xlsx',sheet_name='index')

names=locals()
for s in range(len(index)):
    index_s=[x for x in range(index.start[s],index.end[s])]
    names['rgeo'+str(s)]=list(nuts2_272.iloc[index_s,1])

# National IO （NIO）
os.chdir(path)
# os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Regional account/NUTS2 transfer")
nuts2list=pd.read_excel('NUTS2_list.xlsx')
set0=nuts2list['geo']
# os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method")
industry_row=pd.read_excel('industry.xlsx',sheet_name='Sheet1')
industry_col=pd.read_excel('industry.xlsx',sheet_name='Sheet2')

#Step 1
os.chdir(path+"/ICIO")
icio=pd.read_csv('ICIO2021_'+'2018'+'.csv')#replace year
row_label=icio.iloc[:,0]
col_label=pd.Series(icio.columns)
rows=row_label.str.split('_',expand=True)
rows=pd.DataFrame(rows)
rows[0] = rows[0].replace("CN1","CHN")
rows[0] = rows[0].replace("CN2","CHN")
rows[0] = rows[0].replace("MX1","MEX")
rows[0] = rows[0].replace("MX2","MEX")
rows[1][3262]='VA'
rows[1][3263]='OUTPUT'

cols=col_label.str.split('_',expand=True)
cols[0] = cols[0].replace("CN1","CHN")
cols[0] = cols[0].replace("CN2","CHN")
cols[0] = cols[0].replace("MX1","MEX")
cols[0] = cols[0].replace("MX2","MEX")
cols=cols[1:3599]
cols[1][len(cols)]='TOTAL'
cols.index=range(3598)

years=[str(x) for x in range(2008,2019)]
for t in range(len(years)):
    os.chdir(path+"/ICIO")
    icio=pd.read_csv('ICIO2021_'+years[t]+'.csv')#replace year
    for s in range(len(ISO3)):
        #get national IO and regionalize it 
        #selected_rows=(rows.iloc[:,0]==ISO3[s])#replace country
        selected_rows=(rows.iloc[:,0]==ISO3[s])
        sele_rows=[i for i, x in enumerate(selected_rows) if x]
        #add va, output row
        sele_rows.append(3262)
        sele_rows.append(3263)
        aut_io=icio.iloc[sele_rows,:]
        aut_io_t=aut_io.set_index('LAB_LAB').T
        aut_io_t.index=cols.index
        selected_cols=(cols.iloc[:,0]==ISO3[s])
        sele_cols=[i for i, x in enumerate(selected_cols) if x]
        # add total
        sele_cols.append(3597)
        aut_io_t=aut_io_t.iloc[sele_cols,:]
        sele_cols=[i for i, x in enumerate(selected_cols) if x]
        # add total
        sele_cols.append(3597)
        sele_cols=list(np.array(sele_cols)+1)
        aut_io_t.index=col_label[sele_cols]


        #add national export and import manually
        IM=aut_io_t['OUTPUT']-(aut_io_t.sum(axis=1)-aut_io_t['OUTPUT'])
        IM[45:52]=0
        aut_io_t=aut_io_t.assign(IM=list(IM))
        aut_io=aut_io_t.T
        EX=aut_io['TOTAL']-(aut_io.sum(axis=1)-aut_io['TOTAL'])
        EX[46:49]=0
        aut_io=aut_io.assign(EX=list(EX))

        #aggregate sectors to 10 sectors

        # industry_row=pd.read_excel('CHN.xlsx',sheet_name='Sheet1')
        # industry_col=pd.read_excel('CHN.xlsx',sheet_name='Sheet2')
        df2 = aut_io.assign(Industry = list(industry_row['Industry']))
        industry_sum=df2.groupby(['Industry']).sum()
        industry_sum=industry_sum.T
        df3=industry_sum.assign(Industry_=list(industry_col['Industry_']))
        industry_sum=df3.groupby(['Industry_']).sum()
        industry_sum=industry_sum.T
        reindex_r=[0,1,2,3,4,5,6,7,8,10,11,12,13,14,15,17,18,19,20,21,22,23,9,16]
        industry_sum=industry_sum.iloc[reindex_r,:]
        reindex_c=[0,1,2,3,5,7,8,11,13,15,16,17,18,19,21,22,23,24,25,26,12,20,10,9,14,4,6,27]
        industry_sum=industry_sum.iloc[:,reindex_c]
        industry_sum

        #aggregate some sectors (row side)
        b_e=[1,2,3,4]
        g_i=[6,7,8]
        m_n=[12,13]
        o_q=[14,15,16]
        r_u=[17,18,19]
        merge_b_e = pd.Series(industry_sum.iloc[b_e,:].sum(axis=0), name="B-E")
        merge_g_i=pd.Series(industry_sum.iloc[g_i,:].sum(axis=0),name='G-I')
        merge_m_n=pd.Series(industry_sum.iloc[m_n,:].sum(axis=0),name='M_N')
        merge_o_q=pd.Series(industry_sum.iloc[o_q,:].sum(axis=0),name='O-Q')
        merge_r_u=pd.Series(industry_sum.iloc[r_u,:].sum(axis=0),name='R-U')
        df_r = pd.concat([industry_sum.iloc[0,:],merge_b_e,industry_sum.iloc[5,:],merge_g_i,industry_sum.iloc[9,:],
                        industry_sum.iloc[10,:],industry_sum.iloc[11,:],merge_m_n,merge_o_q,merge_r_u,industry_sum.iloc[20,:],
                        industry_sum.iloc[21,:],industry_sum.iloc[22,:],industry_sum.iloc[23,:]], axis=1)

        df_r

        #aggregate some sectors(column side)

        b_e=[1,2,3,4]
        g_i=[6,7,8]
        m_n=[12,13]
        o_q=[14,15,16]
        r_u=[17,18,19]
        merge_b_e=pd.Series(df_r.iloc[b_e,:].sum(axis=0), name="B-E")
        merge_g_i=pd.Series(df_r.iloc[g_i,:].sum(axis=0),name='G-I')
        merge_m_n=pd.Series(df_r.iloc[m_n,:].sum(axis=0),name='M_N')
        merge_o_q=pd.Series(df_r.iloc[o_q,:].sum(axis=0),name='O-Q')
        merge_r_u=pd.Series(df_r.iloc[r_u,:].sum(axis=0),name='R-U')
        df_c = pd.concat([df_r.iloc[0,:],merge_b_e,df_r.iloc[5,:],merge_g_i,df_r.iloc[9,:],
                        df_r.iloc[10,:],df_r.iloc[11,:],merge_m_n,merge_o_q,merge_r_u,df_r.iloc[20,:],df_r.iloc[21,:],
                          df_r.iloc[22,:],df_r.iloc[23,:],df_r.iloc[24,:],df_r.iloc[25,:],df_r.iloc[26,:],df_r.iloc[27,:]], axis=1)
#         os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/NIO/"+str(t))
        savepath=path+"/NIO/"+years[t]
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        os.chdir(savepath)
        df_c.to_excel(ISO3[s]+'.xlsx')


# Step 2
names=locals()
years_blank=['2008 ', '2009 ', '2010 ', '2011 ', '2012 ', '2013 ', '2014 ','2015 ', '2016 ', '2017 ', '2018 ']
for t in range(0,len(years)):
    ex_vec=pd.DataFrame(np.zeros([14,1]),index=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N', 'O-Q', 'R-U', 'TAXSUB','VA', 'IM', 'OUTPUT'])
    im_vec=pd.DataFrame(np.zeros([17,1]),index=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N', 'O-Q', 'R-U', 'HFCE','NPISH','GGFC','GFCF','INVNT','EX','OUTPUT'])
    geo_list=['empty']
    print(years[t])
    for s in range(28):
        os.chdir(path+"/NIO/"+years[t])
        df_c=pd.read_excel(ISO3[s]+'.xlsx',index_col=0)
        os.chdir(path+"/Regional account/regional gross value added")    
        rgva=pd.read_csv('nama_10r_3gva_tabular.tsv',sep='\t')
        rows=rgva.iloc[:,0].str.split(',',expand=True)
        rows=pd.DataFrame(rows)
        rows.columns=['freq','currency','nace','geo']
        df=pd.concat([rows,rgva],axis=1)
        df.drop(df.columns[[4]],axis=1,inplace=True)
        mask=(df.currency=='MIO_EUR')&(df.geo.str.count(ISO2[s])==1)&(df.geo.str.len()==4)
        rgva=df[mask]
        if ISO2[s]=='UK':
            rgva=pd.read_excel('UK rgva.xlsx')
        
        rgeo_s=names['rgeo'+str(s)]
        rgeo=rgeo_s
            
        
        nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
        if ISO2[s]=='RO':
            nace=['A', 'B-E', 'F', 'G-I', 'J', 'K-N', 'K-N', 'K-N','O-Q', 'R-U']

        n=len(rgeo)
        m=len(nace)
        rgva_vl=np.zeros([n,m])
        
        for i in range(n):
            for j in range(m):
                mask=(rgva.geo==rgeo[i])&(rgva.nace==nace[j])
                if any(mask):
                    if len(rgva[mask])==1:
                        if len(str(rgva[mask][years_blank[t]].values[0]).split(" "))==1:
                            rgva_vl[i,j]=float(rgva[mask][years_blank[t]].values)
                        else:
                            rgva_vl[i,j]=float(str(rgva[mask][years_blank[t]].values[0]).split(" ")[0])
                    else:
                        rgva_vl[i,j]=float(rgva[mask].groupby(['nace']).sum()[years_blank[t]].values)

        rgva_frac=np.zeros([n,m])
        total=rgva_vl.sum(axis=0)
        for j in range(m):
            if total[j]>0:
                rgva_frac[:,j]=rgva_vl[:,j]/total[j]


        noutput=df_c.iloc[13,:]
        noutput=noutput.iloc[0:10]
        ninvnt=df_c.INVNT
        ninvnt=ninvnt[0:m]
        nva=df_c.iloc[11,:]
        nva=nva[0:10]
        ntaxsub=df_c.iloc[10,:]
        ntaxsub=ntaxsub[0:10]
        rva=np.zeros([n,m])
        rttl=np.zeros([n,m])
        # rim=np.zeros([n,m])
        rtaxsub=np.zeros([n,m])
        rinvnt=np.zeros([n,m])
        for j in range(m):
            rva[:,j]=nva[j]*rgva_frac[:,j]
            rttl[:,j]=noutput[j]*rgva_frac[:,j]
            rtaxsub[:,j]=ntaxsub[j]*rgva_frac[:,j]
            rinvnt[:,j]=ninvnt[j]*rgva_frac[:,j]
        nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
        rva=pd.DataFrame(rva,index=rgeo,columns=nace)
        rttl=pd.DataFrame(rttl,index=rgeo,columns=nace)
        rtaxsub=pd.DataFrame(rtaxsub,index=rgeo,columns=nace)
        rinvnt=pd.DataFrame(rtaxsub,index=rgeo,columns=nace)
        
        os.chdir(path+"/Regional account/investment or fixed capital formation")
        gfcf=pd.read_csv('nama_10r_2gfcf_tabular.tsv',sep='\t')
        rows=gfcf.iloc[:,0].str.split(',',expand=True)
        rows=pd.DataFrame(rows)
        rows.columns=['freq','currency','nace','geo']
        df=pd.concat([rows,gfcf],axis=1)
        df.drop(df.columns[[4]],axis=1,inplace=True)
        mask=(df.geo.str.count(ISO2[s])==1)&(df.geo.str.len()==4)&(df.currency=='MIO_EUR')
        rgfcf=df[mask]
        if ISO2[s]=='RO':
            nace=['A', 'B-E', 'F', 'G-I', 'J', 'K-N', 'K-N', 'K-N','O-Q', 'R-U']
        rgfcf_vl=np.zeros([n,m])
        for i in range(n):
            for j in range(m):
                mask=(rgfcf.geo==rgeo[i])&(rgfcf.nace==nace[j])
                if any(mask):
                    if len(rgfcf[mask][years_blank[t]].values)==1:
                        rgfcf_vl[i,j]=float(rgfcf[mask][years_blank[t]].values)
                    else:
                        rgfcf_vl[i,j]=float(str(rgfcf[mask][years_blank[t]].values[0]).split(" ")[0])
        
        rgfcf_frac=np.zeros([n,m])
        total=rgfcf_vl.sum(axis=0)
        for j in range(m):
            if total[j]>0:
                rgfcf_frac[:,j]=rgfcf_vl[:,j]/total[j]

        ngfcf=df_c.GFCF
        ngfcf=ngfcf[0:m]
        rgfcf=np.zeros([n,m])
        for j in range(m):
            rgfcf[:,j]=ngfcf[j]*rgfcf_frac[:,j]
        nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
        rgfcf=pd.DataFrame(rgfcf,index=rgeo,columns=nace)
        
        nhfce=df_c.HFCE
        nhfce=nhfce[0:m]
        nnpish=df_c.NPISH
        nnpish=nnpish[0:m]
        nggfc=df_c.GGFC
        nggfc=nggfc[0:m]
        rhfce=np.zeros([n,m])
        rnpish=np.zeros([n,m])
        rggfc=np.zeros([n,m])
        for j in range(m):
                rhfce[:,j]=nhfce[j]*rgva_frac[:,j]
                rnpish[:,j]=nnpish[j]*rgva_frac[:,j]
                rggfc[:,j]=nggfc[j]*rgva_frac[:,j]

        rhfce=pd.DataFrame(rhfce,index=rgeo,columns=nace)
        rnpish=pd.DataFrame(rnpish,index=rgeo,columns=nace)
        rggfc=pd.DataFrame(rggfc,index=rgeo,columns=nace)
        
        os.chdir(path+"/NIO/"+years[t])
        df_c=pd.read_excel(ISO3[s]+'.xlsx',index_col=0)
        national_output=df_c.iloc[len(df_c)-1,:]
        national_output=national_output[0:10]
        A=df_c.iloc[0:10,:].iloc[:,0:10]
        coeff=A/(A.sum(axis=0))
        rid=rttl-rtaxsub-rva
        
        X=np.array(rva)
        SLQ=np.zeros([len(rva),len(nace)])
        total=X.sum().sum()
        for i in range(len(X)):
            for j in range(len(nace)):
                country_total=X[i,:].sum()
                sector_total=X[:,j].sum()
                if (country_total!=0) & (sector_total!=0):
                    SLQ[i,j]=(X[i,j]/country_total)/(sector_total/total)
        SLQ=pd.DataFrame(SLQ,index=rgeo,columns=nace)
        SLQ[SLQ>1]=1
        
        savepath=path+"/SRIO/"+years[t]
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        os.chdir(savepath)
        zero=pd.DataFrame(np.zeros([7,]))
        if len(rgeo)==1:#the country has the only one region
            nuts2=df_c
            ex_vec=pd.concat([ex_vec,nuts2.EX],axis=1,ignore_index=True)
            im_vec=pd.concat([im_vec,nuts2.iloc[12,:].T],axis=1,ignore_index=True)           
            nuts2.to_excel(rgeo[i]+'.xlsx')
            geo_list.append(rgeo[i])
        else:
            for i in range(len(rgeo)):
                t_IIM=np.zeros([10,1])
                nuts2=pd.DataFrame(rid.iloc[i,:]*coeff*SLQ.iloc[i,:])
                nuts2=nuts2.assign(HFCE=list(rhfce.T.iloc[:,i]))
                nuts2=nuts2.assign(NPISH=list(rnpish.T.iloc[:,i]))
                nuts2=nuts2.assign(GGFC=list(rggfc.T.iloc[:,i]))
                nuts2=nuts2.assign(GFCF=list(rgfcf.T.iloc[:,i]))
                nuts2=nuts2.assign(INVNT=list(rinvnt.T.iloc[:,i]))
            #     nuts2=nuts2.assign(FEX=list(rfx.T.iloc[:,i]))
                IEX=rttl.iloc[i,:]-nuts2.sum(axis=1)
                if any(IEX<0):
                    mask=[i for i, x in enumerate(IEX<0) if x]
                    rttl.iloc[i,mask]=rttl.iloc[i,mask]+abs(IEX[mask])
                    t_IIM=0*IEX
                    t_IIM[mask]=abs(IEX[mask])
                    IEX[IEX<0]=0
                nuts2=nuts2.assign(EX=list(IEX))
                nuts2=nuts2.assign(TOTAL=list(rttl.iloc[i,:].T))
                tmp=pd.concat([rtaxsub.iloc[i,:],zero],axis=0,ignore_index=True)
                tmp.index=nuts2.columns
                nuts2=pd.concat([nuts2,tmp.T],axis=0,ignore_index=True)
                tmp=pd.concat([rva.iloc[i,:],zero],axis=0,ignore_index=True)
                tmp.index=nuts2.columns
                nuts2=pd.concat([nuts2,tmp.T],axis=0,ignore_index=True)
                IIM=rttl.iloc[i,:]-nuts2.iloc[:,0:10].sum(axis=0)
                tmp=pd.concat([IIM,zero],axis=0,ignore_index=True)
                tmp.index=nuts2.columns
            #     tmp.index=['A',   'B-E',     'F',   'G-I',     'J',     'K',     'L',   'M_N','O-Q',   'R-U',  'HFCE', 'NPISH',  'GGFC',  'GFCF', 'INVNT',   'EX', 'TOTAL']
                nuts2=pd.concat([nuts2,tmp.T],axis=0,ignore_index=True)
                tmp=pd.concat([rttl.iloc[i,:],zero],axis=0,ignore_index=True)
                tmp.index=nuts2.columns
                nuts2=pd.concat([nuts2,tmp.T],axis=0,ignore_index=True)
                nuts2.index=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N', 'O-Q', 'R-U', 'TAXSUB','VA', 'IM', 'OUTPUT']
                ex_vec=pd.concat([ex_vec,nuts2.EX],axis=1,ignore_index=True)
                im_vec=pd.concat([im_vec,nuts2.iloc[12,:].T],axis=1,ignore_index=True)
                nuts2.to_excel(rgeo[i]+'.xlsx')
                geo_list.append(rgeo[i])
    #ex_vec.drop(ex_vec.columns[[0]],axis=1,inplace=True)
    ex_vec.index=nuts2.index
    ex_vec.columns=geo_list
    ex_vec.to_excel('Export_Vector.xlsx')
    im_vec.columns=geo_list
    im_vec.to_excel('Import_Vector.xlsx')


#Step 3
os.chdir(path+"/Trucktraffic")
truck=pd.read_csv('01_Trucktrafficflow.csv')
nuts=pd.read_csv('02_NUTS-3-Regions.csv',index_col=1)

mask=(nuts.NUTS2!='NAN')
# nuts3_ID=nuts[mask].ETISPlus_Zone_ID
nuts2_ID=list(nuts[mask].NUTS2.unique())

os.chdir(path+"/REGIO")
df=pd.read_excel('Trade Data EU 2013 ref.xlsx',index_col=0)
geo267=list(df.index)

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 
    
loc=[]
for i in range(len(geo267)):
    t=index_of(geo267[i],nuts2_ID)
    if t!=-1:
        loc.append(t)

mask=(nuts.NUTS2!='NAN')
# nuts3_ID=nuts[mask].ETISPlus_Zone_ID
nuts3_ID=nuts[mask].index



# mask=(truck.ID_origin_region? nuts3_ID)&(truck.ID_destination_region?nuts3_ID)
# df=truck[mask]

nuts3_ID=list(nuts3_ID)
truck_flow_2010=np.zeros([len(nuts3_ID),len(nuts3_ID)])
truck_flow_2019=np.zeros([len(nuts3_ID),len(nuts3_ID)])
for k in truck.index:
    i=index_of(truck.ID_origin_region[k],nuts3_ID)
    j=index_of(truck.ID_destination_region[k],nuts3_ID)
    if i!=-1&j!=-1:
        truck_flow_2010[i][j]=truck.Traffic_flow_trucks_2010[k]
        truck_flow_2019[i][j]=truck.Traffic_flow_trucks_2019[k]
truck_flow_2010=pd.DataFrame(truck_flow_2010,index=nuts3_ID,columns=nuts3_ID)
truck_flow_2019=pd.DataFrame(truck_flow_2010,index=nuts3_ID,columns=nuts3_ID)


df2 = truck_flow_2010.assign(nuts2 = nuts.NUTS2[nuts3_ID])
nuts2_sum_2010=df2.groupby(['nuts2']).sum()
nuts2_sum_2010=nuts2_sum_2010.T
df3=nuts2_sum_2010.assign(nuts2_=nuts.NUTS2[nuts3_ID])
nuts2_sum_2010=df3.groupby(['nuts2_']).sum()
nuts2_sum_2010=nuts2_sum_2010.T
os.chdir(path+"/Trucktraffic")
nuts2_sum_2010.to_excel('road freight flows NUTS2 level 2010.xlsx')

df2 = truck_flow_2019.assign(nuts2 = nuts.NUTS2[nuts3_ID])
nuts2_sum_2019=df2.groupby(['nuts2']).sum()
nuts2_sum_2019=nuts2_sum_2019.T
df3=nuts2_sum_2019.assign(nuts2_=nuts.NUTS2[nuts3_ID])
nuts2_sum_2019=df3.groupby(['nuts2_']).sum()
nuts2_sum_2019=nuts2_sum_2019.T
os.chdir(path+"/Trucktraffic")
nuts2_sum_2019.to_excel('road freight flows NUTS2 level 2019.xlsx')



os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
s1=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[0],index_col=0)
s2=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[1],index_col=0)
s3=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[2],index_col=0)
s4=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[3],index_col=0)
s5=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[4],index_col=0)
s6=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[5],index_col=0)
s7=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[6],index_col=0)
s8=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[7],index_col=0)
s9=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[8],index_col=0)
s10=pd.read_excel('Trade Data EU 2013 ref.xlsx',sheet_name=nace[9],index_col=0)
ss=s1+s2+s3+s4+s5+s6+s7+s8+s9+s10

geo267=list(s1.index)
geo282=list(nuts2_sum_2010.index)

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 
    
loc1=[]
for i in range(len(geo267)):
    t=index_of(geo267[i],geo282)
    if t!=-1:
        loc1.append(t)

loc2=[]
for i in range(len(geo282)):
    t=index_of(geo282[i],geo267)
    if t!=-1:
        loc2.append(t)

freight_sum_2010=nuts2_sum_2010.iloc[loc1,:].iloc[:,loc1]
freight_sum_2019=nuts2_sum_2010.iloc[loc1,:].iloc[:,loc1]
# ss=ss.iloc[loc2,:].iloc[:,loc2]

os.chdir(path+'/Trucktraffic')
for i in range(len(nace)):
    names['s'+str(i+1)]=names['s'+str(i+1)].iloc[loc2,:].iloc[:,loc2]
    P_trade_sec=names['s'+str(i+1)]/ss
    N_trade_sec_2010=freight_sum_2010.multiply(P_trade_sec)
    N_trade_sec_2010=N_trade_sec_2010.fillna(0)
    N_trade_sec_2010.to_excel('N_trade_sec_2010_'+nace[i]+'.xlsx')
    N_trade_sec_2019=freight_sum_2019.multiply(P_trade_sec)
    N_trade_sec_2019=N_trade_sec_2019.fillna(0)
    N_trade_sec_2019.to_excel('N_trade_sec_2019_'+nace[i]+'.xlsx')


geo272=list(nuts2_272.iloc[:,1])
# os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
# trade=pd.read_excel('N_trade_sec_2010_'+nace[0]+'.xlsx',index_col=0)
nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
index_label=[]
rgeo_label=[]
nace_label=[]
#final=list(freight_sum.index)
# final=list(final)
for i in range(10):
    for j in range(len(geo272)):
        tmp=geo272[j]+'-'+nace[i]
        index_label.append(tmp)
        rgeo_label.append(geo272[j])
        nace_label.append(nace[i])
esti_label=pd.DataFrame({'label':index_label,'rgeo':rgeo_label,'nace':nace_label})
esti_loc=esti_label.sort_values('label').index
esti_label2=esti_label.iloc[esti_loc,:]


t0=tuple(range(9))#AT
t1=tuple(range(9,20))#BE
t2=tuple(range(20,26))#BG
t3=26#CY
t4=tuple(range(27,35))#CZ
t5=tuple(range(35,72))#DE
t6=tuple(range(72,77))#DK
t7=77#EE
t8=tuple(range(78,91))#EL
t9=tuple(range(91,110))#ES
t10=tuple(range(110,115))#FI
t11=tuple(range(115,137))#FR
t12=tuple(range(137,141))#HRV
t13=tuple(range(141,149))#HU
t14=tuple(range(149,152))#IE
t15=tuple(range(152,173))#IT
t16=tuple(range(173,175))#LT
t17=175#LU
t18=176#LV
t19=177#MT
t20=tuple(range(178,190))#NL
t21=tuple(range(190,206))#PL
t22=tuple(range(206,213))#PT
t23=tuple(range(213,221))#RO
t24=tuple(range(221,229))#SE
t25=tuple(range(229,231))#SI
t26=tuple(range(231,235))#SK
t27=tuple(range(235,272))#UK


from ipfn import ipfn
for t in range(len(years)):
    os.chdir(path+"/ICIO")
    icio=pd.read_csv('ICIO2021_'+years[t]+'.csv')#replace year
    row_label=icio.iloc[:,0]
    col_label=pd.Series(icio.columns)
    rows=row_label.str.split('_',expand=True)
    rows=pd.DataFrame(rows)
    rows[0] = rows[0].replace("CN1","CHN")
    rows[0] = rows[0].replace("CN2","CHN")
    rows[0] = rows[0].replace("MX1","MEX")
    rows[0] = rows[0].replace("MX2","MEX")
    rows[1][3262]='VA'
    rows[1][3263]='OUTPUT'

    cols=col_label.str.split('_',expand=True)
    cols[0] = cols[0].replace("CN1","CHN")
    cols[0] = cols[0].replace("CN2","CHN")
    cols[0] = cols[0].replace("MX1","MEX")
    cols[0] = cols[0].replace("MX2","MEX")
    cols=cols[1:3599]
    cols[1][len(cols)]='TOTAL'
    cols.index=range(3598)

    nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
    sec0=['01T02', '03']
    sec1=['05T06', '07T08', '09', '10T12', '13T15', '16','17T18', '19', '20', '21', '22', '23', '24', '25', '26', '27',
           '28', '29', '30', '31T33', '35', '36T39']
    sec2=['41T43']
    sec3=['45T47', '49','50', '51', '52', '53', '55T56']
    sec4=['58T60', '61', '62T63']
    sec5=['64T66']
    sec6=['68']
    sec7=['69T75', '77T82']
    sec8=['84', '85', '86T88']
    sec9=['90T93', '94T96','97T98']

    ISO=['AUT','BEL','BGR','CYP','CZE','DEU','DNK','EST','GRC','ESP','FIN','FRA','HRV','HUN','IRL','ITA','LTU','LUX','LVA','MLT','NLD',
        'POL','PRT','ROU','SWE','SVN','SVK','GBR','ARG','AUS','BRA','BRN','CAN','CHE','CHL','CHN','COL','CRI','HKG',
         'IDN','IND','ISL','ISR','JPN','KAZ','KHM','KOR','LAO','MAR','MEX','MMR','MYS','NOR','NZL','PER',
         'PHL','RUS','SAU','SGP','THA','TUN','TUR','TWN','USA','VNM','ZAF','ROW']
    names=locals()
    nation=28
    for s in range(len(nace)):
        sec_set_i=names['sec'+str(s)]
        os.chdir(path+"/Trucktraffic")
        if t<5:
            trade=pd.read_excel('N_trade_sec_2010_'+nace[s]+'.xlsx',index_col=0)
        else:
            trade=pd.read_excel('N_trade_sec_2019_'+nace[s]+'.xlsx',index_col=0)
        print(nace[s])
        for p in range(len(nace)):
    #         print(p)
            sec_set_j=names['sec'+str(p)]
            F=np.zeros([nation,nation])
            for c in range(len(F)):
                index_i=names['t'+str(c)]
                matching1 = [k for k in rows.index if rows[0][k]==ISO[c]]
                matching2 = [k for k in rows.index if rows[1][k] in sec_set_i]
                matching=list(set(matching1).intersection(set(matching2)))
                df=icio.iloc[matching,:]
                for d in range(len(F)):
                    index_j=names['t'+str(d)]
                    matching1 = [k for k in cols.index if cols[0][k]==ISO[d]]
                    matching2 = [k for k in cols.index if cols[1][k] in sec_set_j]
                    matching=list(set(matching1).intersection(set(matching2)))
                    df2=df.iloc[:,matching]
                    F[c][d]=df2.sum(numeric_only=True).sum()
                    if isinstance(index_i, tuple)&isinstance(index_j,tuple):
                        freight_nuts=trade.iloc[list(index_i),:].iloc[:,list(index_j)]
                        P_trade=freight_nuts/freight_nuts.sum().sum()
                        est=P_trade*(F[c][d])
                    elif isinstance(index_i,int)&isinstance(index_j,tuple):
                        freight_nuts=trade.iloc[index_i,:][list(index_j)]
                        P_trade=freight_nuts/freight_nuts.sum()
                        est=np.array(P_trade*(F[c][d])).reshape([1,len(index_j)])
                    elif isinstance(index_j, int)&isinstance(index_i,tuple):
                        freight_nuts=trade.iloc[list(index_i),:].iloc[:,index_j]
                        P_trade=freight_nuts/freight_nuts.sum()
                        est=np.array(P_trade*(F[c][d])).reshape([len(index_i),1])
                    else:
                        est=np.array(F[c][d]).reshape([1,1])
                    if (d==0):
                        dim1=est
                    else:
                        dim1=np.hstack((dim1,est))                   
                if (c==0):
                    dim2=dim1
                else:
                    dim2=np.vstack((dim2,dim1))
            if (p==0):
                dim3=dim2
            else:
                dim3=np.hstack((dim3,dim2))                   
        if (s==0):
            dim4=dim3
        else:
            dim4=np.vstack((dim4,dim3))

    esti=pd.DataFrame(dim4,index=index_label,columns=index_label)
    esti=esti.fillna(0)
    #esti=esti.iloc[esti_loc,:].iloc[:,esti_loc]
    os.chdir(path+"/Prior")
    esti.to_excel('MRIO_'+years[t]+'prior.xlsx')
    print("mission completed!"+years[t])       


from ipfn import ipfn

os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
final=pd.read_excel('final_list.xlsx',index_col=0)
final=list(final.iloc[:,0])

# os.chdir("/Users/ceri/Documents/Research/OMPTEC/Mark's method/Trade matrix within nuts")
# trade=pd.read_excel('N_trade_sec_2010_'+nace[0]+'.xlsx',index_col=0)
nace=['A', 'B-E', 'F', 'G-I', 'J', 'K', 'L', 'M_N','O-Q', 'R-U']
index_label=[]
rgeo_label=[]
nace_label=[]
#final=list(freight_sum.index)
# final=list(final)
for i in range(10):
    for j in range(len(final)):
        tmp=final[j]+'-'+nace[i]
        index_label.append(tmp)
        rgeo_label.append(final[j])
        nace_label.append(nace[i])
esti_label=pd.DataFrame({'label':index_label,'rgeo':rgeo_label,'nace':nace_label})
esti_loc=esti_label.sort_values('label').index
esti_label2=esti_label.iloc[esti_loc,:]

n=10
names=locals()
# years=['2008 ', '2009 ', '2010 ', '2011 ', '2012 ', '2013 ', '2014 ','2015 ', '2016 ', '2017 ', '2018 ']
years=[str(x) for x in range(2008,2019)]
for t in range(len(years)):
# for t in range(8,len(years)):
    os.chdir(path+"/Prior")
    esti2=pd.read_excel('MRIO_'+years[t]+'prior.xlsx',index_col=0)#sector-region
    esti2=esti2.iloc[esti_loc,:].iloc[:,esti_loc]#region-sector
    os.chdir(path+"/SRIO/"+years[t])
    ex_vec=pd.read_excel('Export_Vector.xlsx',index_col=0)
    im_vec=pd.read_excel('Import_Vector.xlsx',index_col=0)
    im_vec=im_vec.iloc[0:10,:]
    ex_vec=ex_vec.iloc[0:10,:]
    print(years[t])
    for i in range(len(final)):
        for j in range(len(final)):
            if i!=j:
                pattern=esti2.iloc[i*10:(i*10)+10,:].iloc[:,j*10:(j*10)+10]
                row_relative=pattern.sum(axis=1)/(esti2.iloc[i*10:(i*10)+10,:].sum(axis=1)-esti2.iloc[i*10:(i*10)+10,:].iloc[:,i*10:(i*10)+10].sum(axis=1))
                row_sum=np.array(ex_vec[final[i]])*np.array(row_relative)
                col_relative=pattern.sum(axis=0)/(esti2.iloc[:,j*10:(j*10)+10].sum(axis=0)-esti2.iloc[j*10:(j*10)+10,:].iloc[:,j*10:(j*10)+10].sum(axis=0))
                col_sum=np.array(im_vec[final[j]])*np.array(col_relative)
                seed = np.ones([n,n])   
                aggregates = [row_sum, col_sum]
                dimensions = [[0], [1]]
                IPF = ipfn.ipfn(seed, aggregates, dimensions, convergence_rate=1e-3)
                seed = IPF.iteration()
                dim1=np.array(pd.DataFrame(seed))
            else:
                seed=pd.read_excel(final[i]+'.xlsx',index_col=0)
                dim1=np.array(seed.iloc[0:10,:].iloc[:,0:10])
            if (j==0):
                dim2=dim1
            else:
                dim2=np.hstack((dim2,dim1))
        if i==0:
            dim3=dim2
        else:
            dim3=np.vstack((dim3,dim2))
    #esti=pd.DataFrame(dim3,index=esti_label.label,columns=esti_label.label)
    esti=pd.DataFrame(dim3)
    esti=esti.fillna(0)
    esti=esti.iloc[esti_loc,:].iloc[:,esti_loc]
    esti.index=esti_label.label
    esti.columns=esti_label.label
    os.chdir(path+"/MRIO")
    esti.to_excel('MRIO_'+years[t]+'_272regions.xlsx')


           
