#!/usr/bin/env python
# coding: utf-8

# In[7]:


from tkinter import *
import tkinter.filedialog
import requests, re, time, csv   #導入 
root = Tk()
root.title("IM Automated Filter")    #視窗標題
root.geometry("750x500")             #視窗寬度高度
root.configure(bg='#81D8D0')         #背景顏色

def choosefile():
    global filename
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        lb.config(text = ""+filename);
    else:
        lb.config(text = "尚未選擇");


# In[8]:


#LINE的正規化   
def regLINEWIN10():
    global regex
    regex = r'''(
            from?[\"]?[\:]?[\"]+\w{1,33}\D\D\D+                      #傳送者
            to?[\"]?[\:]?[\"]+\w{1,33}\D\D\D+                        #接收者
            toType?[\"]?[\:]+\w{1}\D\D+                              #toType  
            id?[\"]?[\:]?[\"]+\w{13}\D\D\D+                          #id
            createdTime?[\"]?[\:]+\w{13}\D\D+                        #createdTime    <--可用unix timestamp 轉換成日期
            deliveredTime?[\"]?[\:]\w{1}..?                          #deliveredTime 
            text+[\"]?[\:]?[\"].+?                                   #聊天內容
            hasContent+[\"]?[\:].+?[\"]+                             #"hasContent":false,
            contentType+[\"]?[\:].+?[\"]+
            contentMetadata+[\"]?[\:].+?[\,]?["]+                    
            sessionId+[\"]?[\:].+?[\"]+                              #sessionId
            location+[\"]?[\:].+?[\"]+                               
            chunks+[\"]?[\:].+?[\"]+
            type+[\"]?[\:]\w{1,3}?[\,]?[\"]+
            status+[\"]?[\:]\w{1,3}?[\,]?[\"]+
            chatId+[\"]?[\:]?[\"]\w{1,33}?[\"]?[\,]?[\"]+
            readCount+[\"]?[\:]\w{1,3}?[\,]?[\"]+
            reqSeqV2+[\"]?[\:].+?[\"]+
            contentInfo+[\"]?[\:].+?[\"]+
            eventInfo+[\"]?[\:].+?[\"]+
            rev+[\"]?[\:].+?[\"]+                     
            errorCode+[\"]?[\:].+?[\"]+
            urlPreview+[\"]?[\:].+?[\"]+                             
            hasUrlPreview+[\"]?[\:].+?[\"]+                         
            syncToken+[\"]?[\:].+?[\"]?[\,]?[\"]+
            fromType
            )'''
    lb2.config(text = ""+regex)
    
def regLINEANDROID():
    global regex
    regex =  r'''(
            \w{33}.+?          #接受者ID+文字訊息
            \d{26}\\n\'\,.\'             #時間戳記
            MENTION\\t\\t?
            REPLACE\\t\\t
            STICON\\n\'\,.\'
            OWNERSHIP\\t\\t
            PREVIEW\\n\'\,.\'
            ENABLED\\t
            true\\t
            message\\n\'\,.....................................................
            )'''
    lb2.config(text = ""+regex) 


# In[9]:


#FB的正規化    
def regFBWIN10():
    global regex
    regex = r'''(
            offlineThreadingId\\n\'\,.\'?
            \d{19}\\n\'\,.\'?                   #ThreadingId 19個數字組成
            FBMSyncedThreadKey\\n\'\,.\'?
            FBMSyncedThreadKey\\n\'\,.\'?
            FBMCanonicalThreadKey\\n\'\,.\'?
            \d{15}\\n\'\,.\'?                   #userId     
            \d{15}\\n\'\,.\'?                   #senderId
            FBStringWithRedactedDescription\\n\'\,.\'?
            FBStringWithRedactedDescription\\n\'\,.\'?
            .+?                                 #訊息內容
            FBMMessageAttachment\\n\'\,.\'
            )'''
    lb2.config(text = ""+regex)
    
def regFBANDROID():
    global regex
    regex =  r'''(
            ONE\:\d{15}\:\d{15}                   #對話雙方ID
            .{0,200}                              #對話訊息 設定0~200個字元
            \\n\'\,.\'key\"\:\"FACEBOOK\:\d{15}   #傳送方ID
            \"\,\"name\"\:\"?.{1,30}              #傳送方名稱
            \"\,\"email.{1,30}
            )'''
    lb2.config(text = ""+regex)    


# In[10]:


#IG的正規化   
def regIGWIN10():
    global regex
    regex = r'''(
            id\"\:.\"\d{35}\"\,.\"                #item id
            user\\n\'\,.\'id\"\:.\d{10}\,.\"      #user id
            timestamp\"\:.\d{16}\,.\"             #timestamp
            item\\n\'\,.\'type\"\:.\"text\"\,.\"  #item type
            text\"\:.\".{150}                     #text後接續之150字元
            )'''
    lb2.config(text = ""+regex)
    
def regIGANDROID():
    regex = r'''(
            text.{1,50}\\n\'\,.\'                      #text 取1~50字元
            type\"\:\"TEXT\"\,\"                       #type text
            status\"\:\"UPLOADED\"\,\"
            item\\n\'\,.\'type\"\:\"text\"\,\"         #item type text
            item\\n\'\,.\'id\"\:\"\d{35}\"\,\"         #item id
            client\\n\'\,.\'context\"\:\".{36}\"\,\"
            timestamp\"\:\"\d{16}\"\,\"                #timestamp
            timestamp\\n\'\,.\'micro\"\:\d{16}\,\"     #timestamp micro 時間戳記
            user\\n\'\,.\'id\"\:\"\d{10}?\"\,\"?       #接收者user id
            text\"\:\".{50}                            #text 後接續50字元
            )'''
    lb2.config(text = ""+regex)


# In[11]:


def filter():
    fp = open(filename)
    string = fp.readlines()
    strings = str(string)
    starttime = time.clock()    #計算開始時間
    fo = open(filename+"new.txt","w")
    emails = re.findall(regex,strings, re.VERBOSE)  #以pattern找尋要找的資料 並印出
    for email in emails:
        fo.write( "%s\n" %email )
    fp.close()
    fo.close()
    endtime = time.clock()             # 輸出執行時間


# In[12]:


lbchoose = Label(root,text = 'Instant Messenger Automated Filter',bg="#81D8D0",font="Georgia 25 bold") 
lbchoose.place(x=40,y=10)
lb = Label(root,text = '選擇過濾檔案-請點選右邊按鈕------------>',font="Helvetic 12 bold",bg="white",width=58)
lb.place(x=30,y=80)
btn = Button(root,text=".....",command=choosefile,bg='#FFFFFF')
btn.place(x=625,y=80)
#LINE-button
LINEp = PhotoImage(file="line.png")
btnLINEWIN10 = Button(root,image=LINEp,text = 'LINE -Win10',command=regLINEWIN10,compound=TOP,bg="#81D8D0",font="Helvetic 10 bold")     
btnLINEWIN10.place(x=30,y=120)
btnLINEANDROID = Button(root,image=LINEp,text = 'LINE-Android',command=regLINEANDROID,compound=TOP,bg="#81D8D0",font="Helvetic 10 bold")     
btnLINEANDROID.place(x=150,y=120)
#FB-button
FBp = PhotoImage(file="FB.png")
btnFBWIN10 = Button(root,image=FBp,text = ' FB - Win10 ',command=regFBWIN10,compound=TOP,bg="#81D8D0",font="Helvetic 10 bold")     
btnFBWIN10.place(x=30,y=260)
btnFBANDROID = Button(root,image=FBp,text = ' FB - Android ',command=regFBANDROID,compound=TOP,bg="#81D8D0",font="Helvetic 10 bold")     
btnFBANDROID.place(x=150,y=260)
#IG-button
IGp = PhotoImage(file="IG.png")
btnIGWIN10 = Button(root,image=IGp,text = ' IG - Win10 ',command=regIGWIN10,compound=TOP,bg="#81D8D0",font="Helvetic 10 bold")     
btnIGWIN10.place(x=30,y=400)
btnIGANDROID = Button(root,image=IGp,text = ' IG - Android ',command=regIGANDROID,compound=TOP,bg="#81D8D0",font="Helvetic 10 bold")     
btnIGANDROID.place(x=150,y=400)

lb2 = Label(root,text = '正規化演算法',bg="white",width=50,height=15)
lb2.place(x=275,y=120)
btnst = Button(root,text = 'START!',command=filter,width=10,height=1,fg='#FFFFFF',bg='#000000',font="Helvetic 20 bold")     
#開始正規化
btnst.place(x=350,y=400)


root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




