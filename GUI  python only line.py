#!/usr/bin/env python
# coding: utf-8

from tkinter import *
import tkinter.filedialog
import requests, re, time, csv   #導入

root = Tk()
root.title("IM Automated Filter")    #視窗標題
root.geometry("700x400")             #視窗寬度高度
root.configure(bg='#81D8D0')         #背景顏色

def choosefile():
    global filename
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        lb.config(text = ""+filename);
    else:
        lb.config(text = "尚未選擇");

#LINE的正規化   
def regLINEWIN10():
    global regex
    regex = r'''(
            from?[\"]?[\:]?[\"]+\w{1,33}\D\D\D+                      #傳送者
            to?[\"]?[\:]?[\"]+\w{1,33}\D\D\D+                        #接收者
            toType?[\"]?[\:]+\w{1}\D\D+                              #toType    <--有 0,1,2
            id?[\"]?[\:]?[\"]+\w{13}\D\D\D+                          #id
            createdTime?[\"]?[\:]+\w{13}\D\D+                        #createdTime    <--可用unix timestamp 轉換成日期
            deliveredTime?[\"]?[\:]\w{1}..?                          #deliveredTime  <--全部都接0  (測試未傳送完成的差異)
            text+[\"]?[\:]?[\"].+?                                   #聊天內容
            hasContent+[\"]?[\:].+?[\"]+                             #"hasContent":false,
            contentType+[\"]?[\:].+?[\"]+
            contentMetadata+[\"]?[\:].+?[\,]?["]+                    #<--不確定其格式
            sessionId+[\"]?[\:].+?[\"]+                              #sessionId
            location+[\"]?[\:].+?[\"]+                               #<--這部可用在前半段最後一格˙
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
            urlPreview+[\"]?[\:].+?[\"]+                             #看傳連結是否會顯示網址
            hasUrlPreview+[\"]?[\:].+?[\"]+                         #看傳連結是否顯示為true
            syncToken+[\"]?[\:].+?[\"]?[\,]?[\"]+
            fromType
            )'''
    lb2.config(text = ""+regex)
    
def regLINEANDROID():
    global regex
    regex =  r'''(
            \w{33}.{1,50}?         #接受者ID+文字訊息
            \d{26}\\n\'\,.\'?            #時間戳記
            MENTION\\t\\t?
            REPLACE\\t\\t?
            STICON\\n\'\,.\'?
            OWNERSHIP\\t\\t?
            PREVIEW\\n\'\,.\'?
            ENABLED\\t?
            true\\t?
            message\\n\'\,.....................................................
            )'''
    lb2.config(text = ""+regex)

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

lbchoose = Label(root,text = 'Instant Messenger Automated Filter',bg="#81D8D0",font="Georgia 25 bold") 
lbchoose.place(x=40,y=10)
lb = Label(root,text = '選擇過濾檔案-請點選右邊按鈕------------>',font="Helvetic 12 bold",bg="white",width=58)
lb.place(x=30,y=80)
btn = Button(root,text=".....",command=choosefile,bg='#FFFFFF')
btn.place(x=625,y=80)
#LINE-button
LINEp = PhotoImage(file="line.png")
btnLINEWIN10 = Button(root,image=LINEp,text = 'LINE -Win10',command=regLINEWIN10,compound=TOP,bg="#81D8D0",font="Helvetic 10 bold")     #讀取WIN10正規
btnLINEWIN10.place(x=30,y=120)
btnLINEANDROID = Button(root,image=LINEp,text = 'LINE-Android',command=regLINEANDROID,compound=TOP,bg="#81D8D0",font="Helvetic 10 bold")     #讀取android正規
btnLINEANDROID.place(x=150,y=120)


lb2 = Label(root,text = '正規化演算法',bg="white",width=50,height=15)
lb2.place(x=275,y=120)
btnst = Button(root,text = 'START!',command=filter,width=12,height=1,fg='#FFFFFF',bg='#000000',font="Helvetic 20 bold")     
#開始正規化
btnst.place(x=30,y=260)


root.mainloop()