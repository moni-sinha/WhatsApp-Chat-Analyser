import re
import pandas as pd
import streamlit as st

def Loading(img):
    # st.markdown('',unsafe_allow_html=True)
    # gif=st.image('gifs/gify.gif',width=600)
    gif=st.empty()
    a,b,c=gif.columns([1,2.5,1])
    with b:
        st.image('gifs/gify.gif')
    return gif


def split_user(x):
    x=x.split(': ',1)
    if x[1:]:
        return x
    else:
        return(['group notification',x[0]])

def Reset_User(x):
    pat = '\+\d{2}\s\d{5}\s\d{5}'
    if(re.fullmatch(pat,x)):
        return x[4:]
    else:
        return x
    
def  processText(data,android):
    if android:
        pattern = '\n\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\W{0,1}\w{0,2}\s-\s'
        messages = re.split(pattern,data)[1:]
        dates=re.findall(pattern[:-3],data)
        df=pd.DataFrame({'Date':dates,'Messages':messages})
        
        df['Date']=df['Date'].apply(lambda x: x[1:-3])
        df['Datetime']=pd.to_datetime(df['Date'])
        df['Date']=df['Date'].apply(lambda x: x.split(', ')[0])
        
    else:
        pattern = '\n\W{0,1}\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s\w{0,2}\]\s'
        messages = re.split(pattern,data)[1:]
        dates=re.findall(pattern,data)
        df=pd.DataFrame({'Date':dates,'Messages':messages})
        
        def setDate(x):
            if(x[1]=='['):
                return x[2:-2]
            return x[3:-2]
        
        df['Date']=df['Date'].apply(setDate)
        df['Datetime']=pd.to_datetime(df['Date'])
        df['Date']=df['Date'].apply(lambda x: x.split(', ')[0])
   
    
    df['User']=df['Messages'].apply(lambda x: split_user(x)[0])
    df['Messages']= df['Messages'].apply(lambda x: split_user(x)[1])    
    df['User']=df['User'].apply(lambda x: Reset_User(x))
    
    
    dfirst=0
    for d in df.Date:
        x=d.split('/',2)[0:2]
        if(int(x[0])>12):
            dfirst=1
            break
        elif(int(x[1])>12):
            break
    
    if(dfirst):
        df['Date']=pd.to_datetime(df['Date'],format='%d/%m/%y')
    else:
        df['Date']=pd.to_datetime(df['Date'],format='%m/%d/%y')
           
    df['Date']=pd.to_datetime(df['Date']) # format('%d/%m/%y, %H:%M %p')   
    
    df['Day']=df['Date'].dt.day
    df['Month']=df['Date'].dt.month_name()
    df['Year']=df['Date'].dt.year
    df['Month_num'] = df['Date'].dt.month
    df['Week']=df['Date'].dt.isocalendar().week
    df['Day_name'] = df['Date'].dt.day_name()
    df['Time']=df['Datetime'].dt.time
    df['Hour'] = df['Datetime'].dt.hour
    df['Minute'] = df['Datetime'].dt.minute
    
    df.drop('Datetime',axis='columns')
    df=df.dropna()
    return df


def Remove_StopWords(x,links): 
    f=open('StopWords.txt','r')
    stopWords= f.read().split("\n")
    links=" ".join(links)
    y = []
    if x!="This message was deleted" and x!="<Media omitted>" and x!='You deleted this message' and x!="image omitted" and x!="sticker omitted":
        for word in x.split():
            if word.lower() not in stopWords and word not in links:
                y.append(word)
    return " ".join(y)
