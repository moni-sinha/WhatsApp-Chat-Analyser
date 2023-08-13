from datetime import time
import streamlit as st
# import pandas as pd
import dataCleaning,analysis,plots
import matplotlib.pyplot as plt

gcolor="#112233"
subheadcolor="#88BDBC"
pcolor="#52BD78"
headcolor="#52BD78"

# pcolor=st.color_picker('Pick a color')
# st.image('anime1.jpg')
st.markdown('<h1 style="color:{};text-align: center;font-size: 42px;">WhatsApp Chat Analysis</h1>'.format(pcolor),unsafe_allow_html=True)
statement=st.markdown('<h6 style="text-align: center;">Browse and Select Chat files in the Sidebar to start!</h6> ',unsafe_allow_html=True)

data=""
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    statement.empty()
    gif= dataCleaning.Loading('gifs/gify.gif')
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    if(data==""):
     st.markdown('<p style="color:{};text-align:center;">The File is Empty ! Please Upload a Chat File to Continue!</p>'.format( subheadcolor),unsafe_allow_html=True)
    # android=st.radio("Chat Exported from: ",['Android','Iphone'])
    android='Android'
    df = dataCleaning.processText(data,android=="Android")

 
# file = open('Group1.txt','r',encoding='utf-8')
# data=file.read()
# df = dataCleaning.processText(data)


#  st.dataframe(df)
if(data!=""):
    # if st.sidebar.button("Show Analysis"):  
    Option=st.sidebar.radio("Choose an Option",['View Chat Analytics','Search Keywords'])
    if(Option=='View Chat Analytics'):
        if(df.shape[0]==0):
            st.markdown('<p style="color:{};text-align:center;">The File is Not a Chat File Please Enter a WhatsApp Chat File to Continue!</p>'.format( subheadcolor),unsafe_allow_html=True)
        else:        
            listusers = df['User'].unique()
            listusers=listusers.tolist()
            if 'group notification' in listusers:
                listusers.remove('group notification')
            listusers.sort()
            listusers.insert(0,'Overall Analysis')
            
            user = st.sidebar.selectbox("Show analysis of: ",listusers)
            
            messages,words,media,deleted,links= analysis.fetch_stats(user,df) 
            emojies=analysis.MostCommonEmojies(user,df)  
            datetimeline,monthtimeline,weektimeline=analysis.showTimeline(df,user)
            Weekdf,Monthsdf,Perioddf=analysis.Activitymaps(df,user)
            display_users=min(10,int((len(listusers)-1)/2))
            busy_users=analysis.busyUsers(df,display_users)
            lazy_users=analysis.LeastResponsive(df,display_users)
            wc,mostCommon= analysis.MostCommonWords(user,df,links)
            
            gif.empty()  #* Loading Gif removed
            
            expander = st.expander("Show Chat")
            with expander:
                    st.text(data)
                     
            if(user!="Overall Analysis"):
                st.markdown('<h2 style="color:{}; text-align: center;">Top Statistics of {}</h2>'.format(pcolor,user),unsafe_allow_html=True)
            else:
                st.markdown('<h2 style="color:{}; text-align: center;">Top Overall Statistics</h2>'.format(pcolor),unsafe_allow_html=True)


            c1,c2= st.columns(2)
            with c1:
                st.markdown('<div style="display:flex;justify-content:space-between;"><h3>Total Messages  -  {}</h3></div>'.format(str(messages)),unsafe_allow_html=True)
                # st.markdown("""<hr style="height:5px;background-color:"green"/>""",unsafe_allow_html=True)
            with c2:
                st.markdown('<div style="display:flex;justify-content:space-between;"><h3>Total Words  -  {}</h3></div>'.format(str(words)),unsafe_allow_html=True)
            st.markdown('<hr style="height=5px; color:"green";>',unsafe_allow_html=True)   
            col1, col2 = st.columns([3, 4])
            with col1:       
                st.markdown('<div style="display:flex;justify-content:space-between"><h4>Emojies Shared</h4><h4>{}</h4></div>'.format(str(emojies.shape[0])),unsafe_allow_html=True)    
                st.markdown('<div style="display:flex;justify-content:space-between"><h4>Links Shared</h4><h4>{}</h4></div>'.format(str(len(links))),unsafe_allow_html=True)
                st.markdown('<div style="display:flex;justify-content:space-between"><h4>Deleted Messages</h4><h4>{}</h4></div>'.format(str(deleted)),unsafe_allow_html=True)
                st.markdown('<div style="display:flex;justify-content:space-between"><h4>Media Shared</h4><h4>{}</h4></div>'.format(str(media)),unsafe_allow_html=True)
  
            with col2:
                fig,ax=plots.BarPlot(["MS","DM","LS","ES"],[media,deleted,len(links),emojies.shape[0]],[0,0],orient='h',figsize=[8,5])
                st.pyplot(fig,orientation="h")
                # text = (messages - len(links)  - deleted - media)/10
                # fig=plots.PiePlot(values=[len(links),media,deleted,text],names=["Links Shared","Media Shared","Deleted Messages","text Messages"],
                #                   size=[250,250],margin=[30,0,30,0],textinfo='label',hoverdata=[])
                # st.plotly_chart(fig)
                
            # if st.button("Show Links"):
            #     st.table(links)     
                
            st.markdown('<hr>',unsafe_allow_html=True) 
            st.markdown('<h6 style="color:aliceblue; padding:0; text-align: center;"><span style="color:{}; font-size:2em;">TimeLine of Messages  </span> <br/>(Zoom over an area for clear view!)</h6>'.format(headcolor),unsafe_allow_html=True)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content:space-around;}div.row-widget.stRadio > label{min-height:0px;}</style>', unsafe_allow_html=True)
            timeline=st.radio("",['Daily','Weekly','Monthly'])
            config = {
                    'displayModeBar': True,
                    'displaylogo': False
                    }

            st.write('<style>.js-plotly-plot .plotly .modebar{left:50%;transform: translate(-50%, 0px);}</style>', unsafe_allow_html=True)
            # datetimeline,monthtimeline,weektimeline=analysis.showTimeline(df,user)
            hbox=st.container()
            box=st.container()
            if(timeline=='Daily'):
                hbox.markdown('<h6 style="color:{};text-align:center;">Average Messages per Day: {}</h6>'.format( subheadcolor,str(round(datetimeline['Messages'].sum()/datetimeline.shape[0]))),unsafe_allow_html=True)
                fig=plots.TimePlot(datetimeline,x='Date',y='Messages')
                box.plotly_chart(fig, config=config)
            if(timeline=='Weekly'):
                hbox.markdown('<h6 style="color:{};text-align:center;">Average Messages per Week : {}</h6>'.format( subheadcolor,str(round(weektimeline['Messages'].sum()/weektimeline.shape[0]))),unsafe_allow_html=True)
                fig = plots.TimePlot(weektimeline, x='Week-Number', y="Messages")
                box.plotly_chart(fig, config=config)
            if(timeline=='Monthly'):
                hbox.markdown('<h6 style="color:{};text-align:center;">Average Messages per Month : {}</h6>'.format( subheadcolor,str(round(monthtimeline['Messages'].sum()/monthtimeline.shape[0]))),unsafe_allow_html=True)          
                fig = plots.TimePlot(monthtimeline, x='Monthly-Timeline', y="Messages")
                box.plotly_chart(fig, config=config)


            st.markdown('<h3 style="color:{}; text-align: center;">Activity Map</h3>'.format(headcolor),unsafe_allow_html=True)        
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content:space-around;}div.row-widget.stRadio > label{min-height:0px;}</style>', unsafe_allow_html=True)
            activity=st.radio("",['Day wise','Month Wise'])
            # Weekdf,Monthsdf,Perioddf=analysis.Activitymaps(df,user)
            if(activity=='Day wise'):
                c1,c2=st.columns([3,5])
                with c1:
                    fig=plots.Heatmap(Weekdf,[2,5],'Greens')
                    st.pyplot(fig)

                with c2:
                    fig,ax=plots.BarPlot(Weekdf.index,Weekdf['Messages'],[45,0],orient='v',figsize=[8,6])
                    st.pyplot(fig,orientation="h")
                
                
            elif(activity=='Month Wise') :
                c1,c2=st.columns([3,5])
                with c1:
                    fig=plots.Heatmap(Monthsdf,[2,6],'Greens')
                    st.pyplot(fig)

                with c2:
                    fig,ax=plots.BarPlot(Monthsdf.index,Monthsdf['Messages'],[45,0],orient='v',figsize=[8,6])
                    st.pyplot(fig,orientation="h")


            st.markdown('<h4 style="color:{}; text-align: center;">Hourly Activity Map</h4>'.format(subheadcolor),unsafe_allow_html=True)        
            fig=plots.Heatmap(Perioddf,[20,8],'Greens',rotation=[45,0])
            st.pyplot(fig)
            st.markdown('<hr>',unsafe_allow_html=True)



            if(user=="Overall Analysis"):
                
                st.markdown('<h4 style="color:{}; text-align: center;">Users Message Percentage</h4>'.format(headcolor),unsafe_allow_html=True)
                top_n =st.text_input("How many users you wanna see?",len(listusers))
                top_n = int(top_n)
                
                c1,c2= st.columns(2)        
                User_percentage = analysis.UserPercentage(df,top_n)
                with c1:
                    c1.dataframe(User_percentage)
                with c2:
                    # st.markdown('<center>Hover for details!</center>',unsafe_allow_html=True)
                    fig = plots.PiePlot(data=User_percentage,values='Message %',names = 'Name',margin=[3,0.1,0,0],size=[300,300]) 
                    st.plotly_chart(fig) 
                
                st.markdown('<br>',unsafe_allow_html=True)
                # display_users=min(10,int((len(listusers)-1)/2))
                # busy_users=analysis.busyUsers(df,display_users)
                # lazy_users=analysis.LeastResponsive(df,display_users)
                if len(listusers)>5:
                    c1,c2= st.columns(2)
                    with c1:
                        st.markdown('<h4 style="color:{}; text-align: center;">Most Responsive Users</h4>'.format(subheadcolor),unsafe_allow_html=True)
                        fig,ax= plots.BarPlot(busy_users.index,busy_users.values,[75,0],["","No. of Messages"])
                        # ax.plot(busy_users,'black')  
                        st.pyplot(fig)
                    with c2:
                        st.markdown('<h4 style="color:{}; text-align: center;">Least Responsive Users</h4>'.format(subheadcolor),unsafe_allow_html=True)    
                        fig,ax= plots.BarPlot(lazy_users.index,lazy_users.values,[75,0],["","No. of Messages"],figsize=[10,10])
                        # ax.plot(lazy_users,'black')
                        st.pyplot(fig)
                else:
                    c1,c2= st.columns(2)
                    with c1:
                        st.markdown('<h4 style="color:{}; text-align: center;">Most Active Users</h4>'.format(subheadcolor),unsafe_allow_html=True)
                        busy_users = busy_users.reset_index().rename(columns={'index':'Names','User':'Messages'})
                        st.dataframe(busy_users)
                    with c2:
                        st.markdown('<h4 style="color:{}; text-align: center;">Least Active Users</h4>'.format(subheadcolor),unsafe_allow_html=True)  
                        lazy_users= lazy_users.reset_index().rename(columns={'index':'Names','User':'Messages'})
                        st.dataframe(lazy_users) 
                        
                st.markdown('<hr>',unsafe_allow_html=True)

            # wc,mostCommon= analysis.MostCommonWords(user,df,links)
            st.markdown('<h4 style="color:{}; text-align: center;">Word Cloud Image</h4>'.format(headcolor),unsafe_allow_html=True)
            fig,ax=plt.subplots()
            plt.axis("off")
            plt.tight_layout(pad = 0)
            ax.imshow(wc)
            st.pyplot(fig)
                
            st.markdown('<br>',unsafe_allow_html=True)
            st.markdown('<h4 style="color:{}; text-align: center;">Top Used Words</h4>'.format(headcolor),unsafe_allow_html=True)   
            c1,c2=st.columns([3,4])  
            with c1:              
                st.dataframe(mostCommon)#height=400
            with c2:       
                    fig,ax= plots.BarPlot(mostCommon.Word,mostCommon.Usage,[10,0],["Usage","Word"],orient='h')          
                    st.pyplot(fig) 


            st.markdown('<br>',unsafe_allow_html=True)
            st.markdown('<h4 style="color:{}; text-align: center;">Top Used Emojies</h4>'.format(headcolor),unsafe_allow_html=True) 
            c1,c2=st.columns([3,4])
            with c1:
                # emojies=analysis.MostCommonEmojies(user,df)
                st.dataframe(emojies)
            with c2:
                PieTable=analysis.GetPietable(data=emojies,n=30)
                fig = plots.PiePlot(data=PieTable,values='Usage',names='Emoji',size=[300,300],margin=[0.1,0.1,0.1,15])
                st.plotly_chart(fig)
                

    if(Option=="Search Keywords") :
        
        gif.empty()
        uWord=st.text_input('Please enter a Keyword to search in Chat : ','')
        if(uWord==""):
              st.markdown('<p style="color:{};text-align:center;">No KeyWord Entered!</p>'.format( subheadcolor),unsafe_allow_html=True)
        else:
            st.write('The current word is : ', uWord)
            gif=dataCleaning.Loading('gifs/gify.gif')
            data=analysis.search(uWord,df)
            gif.empty()
            if(data.shape[0]==0):
              st.markdown('<p style="color:{};text-align:center;font-size:26px">This Keyword was not Found in Chat!</p>'.format( subheadcolor),unsafe_allow_html=True)
            else:
                # leastUsed,MostUsed=analysis.
                st.table(data )


                


            
    
            
             
             








# !Todos:
# -no. of emojees                  ----------------done
# -avag response time              -----------done

# *Backgroud colors change:          ------------done
# ? st.markdown("""<style> 
# ?                 .reportview-container { }
# ?                 .css-1d391kg { }
# ?           </>""", unsafe_allow_html=True)


#st.markdown('<p style="font-family:sans-serif; color:Green; font-size: 42px;">of {}</p>'.format(user),unsafe_allow_html=True)
# st.image('anime1.jpg')



# * LOADING GIf
# start_execution = st.button('Run model')
# if start_execution:
#     gif_runner = st.image(gif_path)
#     result = run_model(args)
#     gif_runner.empty()
#     display_output(result)



