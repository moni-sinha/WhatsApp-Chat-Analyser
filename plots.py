import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


bgcolor='#130B27'
pcolor="#52BD78"
Gcolor="#519259"
facecolor="#112233"

sns.set_style('darkgrid')
sns.set(rc={'figure.facecolor':bgcolor,"ytick.color": "white"},font_scale=1.4)

# sns.set(rc={'axes.facecolor':'cornflowerblue', 'figure.facecolor':'cornflowerblue'})


def BarPlot(X,Y,rotation=[0,0],label=["",""],gcolor=Gcolor,facecolor=facecolor,figsize=[10,10],orient='v'):

        fig,ax=plt.subplots()
        fig.patch.set_facecolor(bgcolor)
        # plt.figure(facecolor=facecolor)
        fig.set_figwidth(figsize[0])
        fig.set_figheight(figsize[1])
        if(orient=='h'):
            ax.barh(X,Y,color= gcolor)
        else:
            ax.bar(X,Y,color= gcolor) #width=0.5
        ax.set_facecolor(facecolor)
        plt.xlabel(label[0],fontsize=20,color='white')
        plt.ylabel(label[1],fontsize=20,color='white')
        plt.yticks(rotation=rotation[1],fontsize=20,color='white')
        plt.xticks(rotation=rotation[0],fontsize=15,color='white')              
        return fig,ax

def PiePlot(values,names,data=None,legend=False,size=[None,None],margin=[0,0,0,0],title=None,textinfo='percent+label',hoverdata=None):
    fig = px.pie(data,values=values,names=names,title=title,hover_data=hoverdata ) 
    fig.update_traces(textposition='inside', textinfo=textinfo)
    fig.update_layout(showlegend=legend,height=size[0],width=size[1],margin={
        'l':margin[0],'r':margin[1],'t':margin[2],'b':margin[3]})
    return fig


def TimePlot(datetime,x,y):
  fig = px.line(datetime, x=x, y=y,markers=True)
  return fig

def Heatmap(heattable,figsize=[2,8],cmap=None,annot=True,fmt="d",rotation=[0,0]):
    fig, ax = plt.subplots(figsize=(figsize[0],figsize[1]))
    plt.xlabel("",fontsize=20,color='white')
    plt.ylabel("",fontsize=20,color='white')
    plt.yticks(rotation=rotation[1],fontsize=20,color='white')
    plt.xticks(rotation=rotation[0],fontsize=15,color='white') 
    sns.heatmap(heattable,cmap=cmap,ax=ax,annot=annot,fmt=fmt)
    return fig