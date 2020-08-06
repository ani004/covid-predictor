import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import pickle


df = pd.read_csv(r"C:/Users/ANISH/Desktop/covid_predictor/covid.csv",  low_memory = False)

df['covid_res']=df['covid_res'].map({1:0,2:1,97:2,99:2,98:2})
df['sex']=df['sex'].map({1:0,2:1,97:2,99:2,98:2})
df['intubed']=df['intubed'].map({1:0,2:1,97:2,98:2,99:2})
df['pneumonia']=df['pneumonia'].map({1:0,2:1,97:2,98:2,99:2})
df['diabetes']=df['diabetes'].map({1:0,2:1,97:2,98:2,99:2})
df['copd']=df['copd'].map({1:0,2:1,97:2,98:2,99:2})
df['asthma']=df['asthma'].map({1:0,2:1,97:2,98:2,99:2})
df['inmsupr']=df['inmsupr'].map({1:0,2:1,97:2,98:2,99:2})
df['hypertension']=df['hypertension'].map({1:0,2:1,97:2,98:2,99:2})
df['other_disease']=df['other_disease'].map({1:0,2:1,97:2,98:2,99:2})
df['cardiovascular']=df['cardiovascular'].map({1:0,2:1,97:2,98:2,99:2})
df['obesity']=df['obesity'].map({1:0,2:1,97:2,98:2,99:2})
df['renal_chronic']=df['renal_chronic'].map({1:0,2:1,97:2,98:2,99:2})
df['tobacco']=df['tobacco'].map({1:0,2:1,97:2,98:2,99:2})
df['contact_other_covid']=df['contact_other_covid'].map({1:0,2:1,97:2,98:2,99:2})
df['body_temparature']=df['body_temparature'].map({1:0,2:1,97:2,98:2,99:2})

indexnames=df[df['covid_res']==3].index
df.drop(indexnames,inplace=True)

#df['pregnancy']=df['pregnancy'].map({1:1,2:2,97:3,98:3})

df.drop(['id','patient_type','pregnancy','intubed'],axis=1,inplace=True)
df.drop(['entry_date','date_symptoms','date_died'],axis=1,inplace=True)

df=df.dropna()

X = df.drop('covid_res',axis=1)
y = df['covid_res']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=101)

scaler = MinMaxScaler()
X_train= scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

rfc = RandomForestClassifier(n_estimators=200)
rfc.fit(X_train, y_train)

file=open('model.pkl','wb')
pickle.dump(rfc,file)

inp_f=[1,1,30,1,1,1,1,1,0,1,1,1,1,1,1]
inp_prob=rfc.predict_proba([inp_f])[0][1]
print(inp_prob)