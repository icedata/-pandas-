# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 12:57:24 2017

@author: bing
"""
import numpy as np
import pandas as pd

#一、创建数据
#1.通过传递一个list对象来创建一个Series，pandas会默认创建整型索引
s = pd.Series([1,3,np.nan,5,8])
#2.通过传递一个numpy array，时间索引以及列标签来创建一个DataFrame
dates = pd.date_range('20170301',periods = 6)
df1 = pd.DataFrame(np.random.randn(6,4),index = dates,columns = list('ABCD'))
#3.通过传递一个能够被转换成类似序列结构的字典对象来创建一个DataFrame
df2 = pd.DataFrame({'A':1.,
                    'B':pd.Timestamp('20130102'),
                    'C':pd.Series(1,index=list(range(6)),dtype = 'float32'),
                    'D':np.array([3]*6,dtype = 'int32'),
                    'E':'foo'
                    })
#4.查看不同列的数据类型
df2.dtypes

#二、查看数据
#1.查看frame中头部和尾部的行
df1.head()
df1.tail()
#2.显示索引、列和底层的numpy数据
df1.index
df1.columns
df1.values
#3.describe()函数对于数据的快速统计汇总
df1.describe()
#4.对数据的转置
df1.T
#5.按轴进行排序(如果按行则使用axis = 0)
df1.sort_index(axis = 1,ascending = False)
#6.按值进行排序
df1.sort(columns = 'B')
#7.在排序等操作之后重新生成索引(如果需要在原dataframe中直接修改需加入inplace=True)
df1.reset_index(drop=True)

#三、选择(通过索引或者位置进行选择)
#获取
#1.选择一个单独的列，这将会返回一个Series，等同于df1.A
df1['A']
#2.通过[]进行选择，这将会对行进行切片
df1[0:3]
df1['20170301':'20170303']
#通过标签选择(loc)
df1.loc[dates[0]]
df1.loc[:,['A','B']]
df1.loc['20170301':'20170303',['A','B']]
df1.loc['20170301',['A','B']]
df1.loc[dates[0],'A']
#通过位置选择(iloc)
df1.iloc[3]
df1.iloc[3:5,0:2]
df1.iloc[[1,2,4],[0,2]]
df1.iloc[1:3,:]
df1.iloc[1,1]
#布尔索引
#1.使用一个单独列的值来选择数据
df1[df1.A > 0]
#2. 使用where操作来选择数据
df1[df1>0]
#3. 使用isin()方法来过滤,按更复杂方式提取行列
df3 = df1.copy()
df3['E'] = ['one','one','two','three','four','three']
df3[df3['E'].isin(['two','four'])]
#设置
#1.设置一个新的列(新列为Series则必须设置和原DataFrame一致的索引)
s1 = pd.Series(range(1,7),index = pd.date_range('20170302',periods = 6))
df1['F'] = s1
#2.通过标签和索引设置新的值
df1.at[dates[0],'A'] = 0
df1.iat[0,1] = 0
#3.通过一个numpy数组设置一组新值
df1.loc[:,'D'] = np.array([5]*len(df1))
#4.通过where操作来设置新的值
df4 = df1.copy()
df4[df4>0] = -df4

#四、缺失值处理
#1.reindex()方法可以对指定轴上的索引进行改变/增加/删除操作，这将返回原始数据的一个拷贝
#仅需改变行列名称的话可以直接使用df.index=和df.columns=
df5 = df1.reindex(index = dates[0:4],columns = list(df1)+['E'])
df5.loc[dates[0]:dates[1],'E'] = 1
#2.去掉包含缺失值的行(axis=1表示列)
df5.dropna(how = 'any')
#3.对缺失值进行填充
df5.fillna(value = 5)
#4.去除重复值
df5.drop_duplicates('E') 
#5.对数据进行布尔填充
pd.isnull(df5)

#五、相关操作
#统计
#1.描述性统计分析（按列和行）
df1.mean()
df1.mean(1)
#2.对于拥有不同维度，需要对齐的对象进行操作。Pandas会自动的沿着指定的维度进行广播
s = pd.Series([1,3,5,np.nan,6,8],index = dates).shift(2)
df1.sub(s,axis = 'index') #df1-s
#Apply
#1.对数据应用函数
df1.apply(np.cumsum)
df1.apply(lambda x:x.max()-x.min())
s.value_counts()
#2.Series对象在其str属性中配备了一组字符串处理方法，可以很容易的应用到数组中的每个元素
s = pd.Series(['A','B','Aaba',np.nan,'cat'])
s.str.lower()

#六、合并,分组和reshaping
#1.concat(按列合并添加axis=1)
df = pd.DataFrame(np.random.randn(10,4))
pieces = [df[:3],df[3:7],df[7:]]
pd.concat(pieces)
#2.join
#案例1(key用法)
left = pd.DataFrame({'key':['foo','foo'],'lval':[1,2]})
right = pd.DataFrame({'key':['foo','foo'],'rval':[3,4]})
pd.merge(left,right,on = 'key')
#案例二(how用法)
df1=pd.DataFrame({'key':['a','b','b'],'data1':range(3)})  
df2=pd.DataFrame({'key':['a','b','c'],'data2':range(3)}) 
pd.merge(df1,df2)
right=pd.DataFrame({'key1':['foo','foo','bar','bar'],
                    'key2':['one','one','one','two'],'lval':[4,5,6,7]})
left=pd.DataFrame({'key1':['foo','foo','bar'],
                   'key2':['one','two','one'], 'lval':[1,2,3]}) 
pd.merge(left,right,on = ['key1','key2'],how = 'outer')
#3.Append(使用ignore_index重新生成索引)
df = pd.DataFrame(np.random.randn(8,4),columns = ['A','B','C','D'])
s = df.iloc[3]
df.append(s,ignore_index = True)
#4.group by
df = pd.DataFrame({'A':['foo','bar','foo','bar','foo','bar','foo','foo'],
                   'B':['one','one','two','three','two','two','one','three'],
                   'C':np.random.rand(8),
                   'D':np.random.rand(8)})
df.groupby('A').sum()
df.groupby(['A','B']).sum()
#5.Stack（堆积，index有几层的情况）
tuples = list(zip(*[['bar','bar','baz','baz','foo','foo','qux','qux'],
                    ['one','two','one','two','one','two','one','two']]))
index = pd.MultiIndex.from_tuples(tuples,names = ['first','second'])
df = pd.DataFrame(np.random.randn(8,2),index = index,columns=['A','B'])
df_t = df[:4]
stacked = df_t.stack()
stacked.unstack()
stacked.unstack(1)#把第2个分类项消除了
stacked.unstack(0)#把第2个分类项消除了
#6.数据透视表
df = pd.DataFrame({'A':['one','one','two','three']*3,
                   'B':['A','B','C']*4,
                   'C':['foo','foo','foo','bar','bar','bar']*2,
                   'D':np.random.randn(12),
                   'E':np.random.randn(12)})
pd.pivot_table(df,values = 'D',index = ['A','B'],columns = ['C'])
