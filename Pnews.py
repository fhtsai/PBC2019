import tkinter as tk
from tkinter import *
import webbrowser
import tkinter.font as tkFont
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image, ImageTk
import io 
from io import BytesIO
import ssl

# 這份檔案是NewsPage的初稿，未放入class的形式，存著以備不時之需

root = tk.Tk()
root.title("賽事下注")
root.geometry("1000x1000")

class news():
    def __init__(self):
        response = requests.get("https://nba.udn.com/nba/cate/6754/6780")
        soup = BeautifulSoup(response.text, 'html.parser')
        attr = {'id' : 'news_list_body'}
        news_tag = soup.find_all('div', attrs = attr)
        for i in news_tag:
            self.pa = str(i)
        self.data = list()

    def get_news(self):
        count = 0
        hend = 0
        tend = 0
        tiend = 0
        pend = 0
        piend = 0
        
        while count < 3:
            tmp = list()
            hstart = self.pa.find('/nba/story/', hend)
            hend = self.pa.find('">', hstart)
            href = 'https://nba.udn.com' + self.pa[hstart:hend]

            tstart = self.pa.find('<h3>', tend)
            tend = self.pa.find('</h3>', tstart)
            title = self.pa[tstart + 4:tend]

            tistart = self.pa.find('h24">', tiend)
            tiend = self.pa.find('</b>', tistart)
            time = self.pa[tistart + 5:tiend]

            pstart = self.pa.find('<p>', pend)
            pend = self.pa.find('</p>', pstart)
            p = self.pa[pstart + 3:pend]

            pistart = self.pa.find('data-src', piend)
            piend = self.pa.find('/><', pistart)
            html = self.pa[pistart + 10:piend - 1]

            count += 1
            tmp.append(title)
            tmp.append(time)
            tmp.append(p)
            tmp.append(href)
            tmp.append(html)
            self.data.append(tmp)

        return self.data

news = news()
final = news.get_news()

canvas=tk.Canvas(root, width=500, height=1200, bg="lemon chiffon")  #height調整canvas的長度，要手動調（或寫def）
canvas.pack(side=BOTTOM,fill=BOTH,expand=Y)

F1=tk.Frame(root,bg="misty rose",width=500, height=300)
F1.pack(side=TOP,fill=BOTH) 
frame=tk.Frame(canvas, bg="lemon chiffon",width=500, height=1200)
frame.pack(side=TOP, fill=BOTH)
functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
f1=tkFont.Font(size=20, family="標楷體")
f2=tkFont.Font(size=10, family="微軟正黑體")
for function in reversed(functions):
    btn=tk.Button(F1, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
    btn.pack(side=RIGHT, pady=30, anchor=N)

def callback(event):
    webbrowser.open_new(one_news[-2])
i=0
for one_news in final:
    title=one_news[0]
    time=one_news[1]
    intro=one_news[2]
    if 15<=len(intro)<=30:
        intro=intro[:15]+"\n"+intro[16:]
    elif 30<=len(intro):
        intro=intro[:15]+"\n"+intro[16:30]+"\n"+intro[31:]
    image_url=one_news[-1]
    ssl._create_default_https_context = ssl._create_unverified_context
    u = urlopen(image_url)
    raw_data = u.read()
    u.close()
    img = Image.open(BytesIO(raw_data))
    img=img.resize((200, 100), Image.ANTIALIAS) 
    img=ImageTk.PhotoImage(img)
    picLabel = tk.Label(frame,image=img)
    picLabel.image = img
    picLabel.pack(side=TOP, pady=10, padx=10,anchor=W)
    
    btn=tk.Label(frame, text=title, font=f1,bg="lemon chiffon",cursor="hand2")
    btnsmall=tk.Label(frame, text=time+"\n"+intro,font=f2, bg="lemon chiffon", justify=LEFT)
    btn.bind("<Button-1>", callback)
    btnsmall.bind("<Button-1>", callback)
    picLabel.bind("<Button-1>", callback)
    btn.pack(side=TOP, pady=10,padx=10, anchor=W)
    btnsmall.pack(side=TOP,pady=2,padx=10, anchor=W)
    i+=20

root.mainloop()

