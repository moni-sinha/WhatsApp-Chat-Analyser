from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import dataCleaning
import pandas as pd
import calendar
import numpy as np
extract = URLExtract()

def fetch_stats(user,df):
    
    if(user=='Overall Analysis'):
        user_data=df
    else:
        user_data= df[df['User']==user]
        
    #media = user_data[user_data['Messages']=="<Media omitted>"].shape[0]    
    user_message= user_data['Messages']
    user_words = []
    links=[]
    media,deleted=0,0
    for message in user_message:
        if(message=="This message was deleted" or message=="You deleted this message"):
          deleted+=1
        elif(message!="<Media omitted>" and message!="image omitted" and message!="sticker omitted"):
          user_words.extend(message.split())
        else:
           media+=1
    for message in user_data['Messages']:
        links.extend(extract.find_urls(message))
       
    return user_data.shape[0],len(user_words),media,deleted,links.copy()
  
def busyUsers(df,l):
  busy_users= df['User'].loc[df['User']!='group notification'].value_counts().head(l)
  return busy_users

def LeastResponsive(df,l):
  least_responsive= df['User'].loc[df['User']!='group notification'].value_counts().tail(l)
  return least_responsive
  
  
def UserPercentage(df,n):
  User_percentage =round(df['User'].value_counts()/df.shape[0]*100,2).reset_index().rename(
    columns={'index':'Name','User':'Message %'})
  userprcnt=User_percentage.head(n)
  sum=0
  for i in range (0,User_percentage.shape[0]):
    if i>=n:
      sum+=User_percentage.loc[i,'Message %']
  if sum!=0:
    df2 = {'Name': 'Others', 'Message %': sum}
    userprcnt = userprcnt.append(df2, ignore_index = True)
  return userprcnt


def MostCommonWords(user,df,links):
  if(user=='Overall Analysis'):
    user_data=df[df['User']!='group notification']
  else:
    user_data= df[df['User']==user]
  user_data['Messages'] = user_data['Messages'].apply(lambda x : dataCleaning.Remove_StopWords(x,links))
  user_data = user_data[user_data['Messages']!=""]
  wc = WordCloud(collocations=False,width=400,height=300,min_font_size=5,background_color="white")
  combWords= user_data["Messages"].str.cat(sep=" ")
  df_wc = wc.generate(combWords)
  mostCommonWords=pd.DataFrame(Counter(combWords.split()).most_common(20),columns=['Word','Usage'])
  return df_wc,mostCommonWords 

def MostCommonEmojies(user,df):
  if(user=='Overall Analysis'):
    user_data=df[df['User']!='group notification']
  else:
    user_data= df[df['User']==user]
  emojis=[]
  for msg in user_data['Messages']:
      for c in msg:
          if c in emoji.UNICODE_EMOJI['en']:
              emojis.append(c)
  emojis=pd.Series(emojis,name="usage")
  emojis=pd.DataFrame({'Emoji':emojis.value_counts().index,'Usage':emojis.value_counts().values})
  return emojis


def GetPietable(data,n=30):
  PieTable= data.head(n-1)
  sum=0
  for i in range (0,data.shape[0]):
    if i>n-2:
      sum+=data.loc[i,'Usage']
  df2 = {'Emoji': 'Others', 'Usage': sum}
  PieTable = PieTable.append(df2, ignore_index = True)
  return PieTable
  
def showTimeline(df,user):
  if(user=='Overall Analysis'):
    user_data=df[df['User']!='group notification']
  else:
    user_data= df[df['User']==user]
    
  datetimeline=user_data.groupby(['Date']).count()['Messages'].reset_index()
  month_timeline=user_data.groupby(['Year','Month_num','Month']).count().Messages.reset_index()  
  monthTimeline=[]
  for i in range (len(month_timeline)):
      monthTimeline.append(month_timeline['Month'][i]+"-"+str(month_timeline['Year'][i]))
  month_timeline['Monthly-Timeline']=monthTimeline  
  
  weekly_timeline=user_data.groupby(['Week','Year']).count().Messages.reset_index()
  WeekTimeline=[]
  for i in range (len(weekly_timeline)):
      WeekTimeline.append(str(weekly_timeline['Week'][i])+"th "+str(weekly_timeline['Year'][i]))
  weekly_timeline['Week-Number']=WeekTimeline
  
  return datetimeline,month_timeline,weekly_timeline


def Activitymaps(df,user):
  if(user=='Overall Analysis'):
    user_data=df[df['User']!='group notification']
  else:
    user_data= df[df['User']==user]
  
  weekdf=user_data['Day_name'].value_counts().reset_index().rename(columns={'index':'Day','Day_name':'Messages'})
  weekdf=weekdf.pivot_table(index='Day', values='Messages',sort=False)
  
  values=[0]*12
  months = list(calendar.month_name)[1:]
  monthsdf=pd.DataFrame({'Month':months,'Messages':values})  
  mframe=user_data['Month_num'].value_counts().reset_index().rename(columns={'index':'Month','Month_num':'Messages'})
  for i in range(mframe.shape[0]):
    monthsdf.loc[mframe.Month[i]-1,['Messages']]=mframe.Messages[i]
  monthsdf=monthsdf.pivot_table(index='Month', values='Messages',sort=False)
  
  period=[]
  for Hour in user_data['Hour']:
    if Hour==23:
        period.append("23-00")
    elif Hour<9:
        period.append("0"+str(Hour)+"-0"+str(Hour+1))
    elif Hour==9:
        period.append("09-10")
    else:
        period.append(str(Hour)+"-"+str(Hour+1))
          
  Perioddf=pd.DataFrame({'DayName':user_data['Day_name'],'Period':period,'Message':user_data['Messages']})
  Perioddf=Perioddf.groupby(['DayName','Period']).count()
  Perioddf=Perioddf.pivot_table(index='DayName',columns='Period' ,values='Message',fill_value=0)
  
  return weekdf,monthsdf,Perioddf


def search(uWord,df):
  Chat=[]
  User=[]
  words=[x.split() for x in df['Messages']]
  for i in range(0,df.shape[0]):
      words[i]=list(map(lambda x:x.lower(),words[i]))
      if uWord.lower() in words[i]:
        # Chat+=(df.loc[i]['User']+" : "+df.loc[i]['Messages']+"\n")
        User.append(df.loc[i]['User'])
        Chat.append(df.loc[i]['Messages'])
  data=pd.DataFrame({'User':User,'Message':Chat})
        
  return data
 
 
            


