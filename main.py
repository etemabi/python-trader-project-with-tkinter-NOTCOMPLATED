from tkinter import ttk
from tkinter import Button
from tkinter import Frame
from tkinter import PhotoImage
from ttkthemes import ThemedTk
import websocket
from websocket import *
import json
from threading import *
from os import path
from tkinter.messagebox import showerror
import re
import pymongo


cluster = pymongo.MongoClient("mongodb+srv://etemabifakmi:etemabifakmi@freetrader.1jb7c9v.mongodb.net/?retryWrites=true&w=majority")
db = cluster["account"]
collection = db["account"]
kayitli = False
bulundu = 0

print(open('account.txt').readlines()[1].strip())

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check(email):
    if(re.fullmatch(regex, email())):
        return True
 
    else:
        return False

open("account.txt", "a")

pencere = ThemedTk()
pencere.wm_overrideredirect(True)
pencere.wm_title("free trader")
pencere.configure(bg="#303030")
pencere.set_theme("equilux")

ws = pencere.winfo_screenwidth()
hs = pencere.winfo_screenheight()

SOCKET = "wss://stream.binance.com:9443/ws/dogeusdt@kline_1m"

photo4 = PhotoImage(file = "dogearti.png")
photo5 = PhotoImage(file = "dogeksi.png")
photo6 = PhotoImage(file ="dogesabit.png")

closes = []

coingosterge = ttk.Label(
    font=("Verdana 36 bold"),
    foreground="#B5B5B5",
    background="#303030"
)

coingosterge.place(rely=0.4, relx=0.15)

def on_open(webs):
    pass

def on_close(webs):
    pass

def on_message(webs, message):
    global closes
    global ekpara
    global dogesayi
    global baslangicdegeri

    json_mesasage = json.loads(message)
    mum = json_mesasage["k"]
    mumclosed = mum["x"]
    mumclose = mum["c"]
    muml = mum["l"]
    mumh = mum["h"]

    coinc.configure(text=(f"mevcut değer: {float(mumclose)}"))
    coinl.configure(text=(f"en düşük: {float(muml)}"))
    coinh.configure(text=(f"en yüksek:  {float(mumh)}"))

    print(json_mesasage)

    if mumclosed:
        closes.append(float(mumclose))
        print(closes)
        coingosterge.configure(text=float(mumclose))

        if float(mumclose) > closes[-2]:
                dogeresim.place(rely=4)
                dogeresimartis.place(relx=0.5, rely=0.35)
                dogeresimazalis.place(rely=4)

        if float(mumclose) == closes[-2]:
                dogeresim.place(relx=0.5, rely=0.35)
                dogeresimartis.place(rely=4)
                dogeresimazalis.place(rely=4)

        if float(mumclose) < closes[-2]:
                dogeresim.place(rely=4) 
                dogeresimartis.place(rely=4)
                dogeresimazalis.place(relx=0.5, rely=0.35)
        
        if len(mumclose) == 1:
            baslangicdegeri = float(mumclose)

            baslangicdegerilabel.configure(
                text=f"{baslangicdegeri}"
            )


def moveapp(e):
    pencere.geometry(f"+{e.x_root}+{e.y_root}")

def kapat():
    pencere.destroy()

def assa():
    pencere.geometry('%dx%d+%d+%d' % (700, 40, (ws/100)*85, (hs/100)*90))

def profilayar():
    hesabikapabutton = ttk.Button

def al():
    global dogesayi
    global ekpara

    try:
        cekilecekkatsayi = float(alentry.get())
    except:
        showerror(title="Lütfen Geçerli Bir Sayı Girin", message="Lütfen Geçecerli Bir Sayı Girin")
    
    cekileceksayi = cekilecekkatsayi*closes[-1]

    if ekpara >= cekileceksayi:
        ekpara += round(-cekileceksayi, 5)
        dogesayi += cekilecekkatsayi

        dogesayilabel.configure(
            text=f"Doge: {dogesayi}"
        )

        ekparalabel.configure(
            text=f"Ek: {float(ekpara)}"
        )

        if ekpara + (dogesayi*closes[-1]) > closes[-1]*100:
            cekilecekpara = round(ekpara + (dogesayi*closes[-1]) - closes[-1]*100, 5)

            cekilecekparalabel.configure(
                text=f"{float(cekilecekpara)}"
            )
        
        else:
            cekilecekparalabel.configure(
                text="0"
            )
        
        sorgual = {
            "email": f"{open('account.txt').readlines()[1].strip()}"
        }

        guncellemeal={
            "$set":{
                "doge": dogesayi,
                "ek": ekpara
            }
        }

        collection.update_one(sorgual, guncellemeal)
    
    else:
        showerror(
            title="Yetersiz Para!",
            message="Yetersiz Para!"
    )

def sat():
    global dogesayi
    global ekpara

    try:
        cekilecekkatsayi = float(satentry.get())
    except:
        showerror(title="Lütfen Geçerli Bir Sayı Girin", message="Lütfen Geçecerli Bir Sayı Girin")
    
    cekileceksayi = cekilecekkatsayi*closes[-1]

    if dogesayi >= cekilecekkatsayi:
        ekpara += round(cekileceksayi, 5)
        dogesayi += -cekilecekkatsayi

        dogesayilabel.configure(
            text=f"Doge: {dogesayi}"
        )

        ekparalabel.configure(
            text=f"Ek: {float(ekpara)}"
        )

        if ekpara + (dogesayi*closes[-1]) > closes[-1]*100:
            cekilecekpara = ekpara + (dogesayi*closes[-1]) - closes[-1]*100

            cekilecekparalabel.configure(
                text=f"{float(cekilecekpara)}"
            )
        else:
            cekilecekparalabel.configure(
                text="0"
            )
        
        sorgusat = {
            "email": f"{open('account.txt').readlines()[1].strip()}"
        }

        guncellemesat={
            "$set":{
                "doge": dogesayi,
                "ek": ekpara
            }
        }

        collection.update_one(sorgusat, guncellemesat)
        
    else:
        showerror(
            title="Yetersiz Para!",
            message="Yetersiz Para!"
    )

frame = Frame(background="#303030",height=30)
frame.pack(fill="x")
frame.bind("<B1-Motion>", moveapp)

photo = PhotoImage(file = r"carpi.png")
kapatmabuton = Button(pencere,
 image = photo,
 background="#303030",
 borderwidth=0,
 command=kapat)

kapatmabuton.place(rely=0.02, relx=0.96)

photo2 = PhotoImage(file = r"assa.png")
assabuton = Button(pencere,
 image = photo2,
  background="#303030",
   borderwidth=0,
   command=assa)

assabuton.place(rely=0.02, relx=0.92)

ttk.Label(text="Free Trader By Etem",
 font=("Verdana", 10), 
 foreground="#C8B7EA",
  background="#303030").place(relx=0.04, rely=0.01)

butonstil = ttk.Style()

butonstil.configure(
    "buton.TButton",
    background = "#303030",
    foreground="#B5B5B5",
    font=("Verdana 18 bold")
)

def kayit():
    global kayitli
    global bulundu

    bulundu = 0

    def kayitonay():
        global kayitli

        if check(emailentry.get):#sorun çıkarsa burda
            if adsoyadentry.get() != "":
                if sifreentry.get() != "":
                    arama = collection.find({"email": f"{emailentry.get()}"})

                    for element in arama:
                        global bulundu

                        if element["email"] == emailentry.get():
                            showerror(title="e posta hatası", message="bu e posta zaten kayıtlı")
                            bulundu = 1
                    
                    if bulundu != 1:
                        eklenecekdata = {
                            "email": f"{emailentry.get()}",
                            "adsoyad": f"{adsoyadentry.get()}",
                            "sifre": f"{sifreentry.get()}",
                            "doge": 100,
                            "ek": 0
                        }

                        collection.insert_one(eklenecekdata)

                        open("account.txt", "w").write(f"""
{emailentry.get()}
{adsoyadentry.get()}
{sifreentry.get()}
                        """)
                        
                        
                        kayitli = True

                        kayitstarbuton.destroy()
                        emailentry.destroy()
                        adsoyadentry.destroy()
                        sifreentry.destroy()
                        emailyazi.destroy()
                        sifreyazi.destroy()
                        adsoyadyazi.destroy()
                        pencere.quit()
    
    x = (ws/2) - (400/2)
    y = (hs/2) - (400/2)

    pencere.geometry('%dx%d+%d+%d' % (400, 400, x, y))
    pencere.minsize(width=400, height=400)

    girisstarbuton.destroy()

    kayitstarbuton.place(rely=0.85, relx=0.4)
    kayitstarbuton.configure(
        command=kayitonay
    )

    emailentry = ttk.Entry(
        font="Verdana 16",
        style="entry.TEntry"
    )

    emailentry.place(rely=0.3, relx=0.2, relwidth=0.4)

    emailyazi = ttk.Label(
        text="Email",
        font="Verdana 12",
        background="#303030"
    )
    
    emailyazi.place(rely=0.24, relx=0.2)

    adsoyadentry = ttk.Entry(
        font="Verdana 16",
        style="entry.TEntry"
    )

    adsoyadentry.place(rely=0.51, relx=0.2, relwidth=0.4)

    adsoyadyazi = ttk.Label(
        text="Ad Soyad",
        font="Verdana 12",
        background="#303030"
    )
    
    adsoyadyazi.place(rely=0.45, relx=0.2)

    sifreentry = ttk.Entry(
        font="Verdana 16",
        style="entry.TEntry",
        show="●"
    )

    sifreentry.place(rely=0.72, relx=0.2, relwidth=0.4)

    sifreyazi = ttk.Label(
        text="Şifre",
        font="Verdana 12",
        background="#303030"
    )
    
    sifreyazi.place(rely=0.66, relx=0.2)


def giris():
    global kayitli

    def girisonay():
        global kayitli

        arama = collection.find({"email": f"{emailentry.get()}"})

        for element in arama:
            if element["email"] == emailentry.get():
                if element["sifre"] == sifreentry.get():
                
                    open("account.txt", "w").write(f"""
{emailentry.get()}
{element["adsoyad"]}
{sifreentry.get()}
                        """)

                    kayitli = True
                    emailentry.destroy()
                    sifreentry.destroy()
                    emailyazi.destroy()
                    sifreyazi.destroy()
                    girisstarbuton.destroy()
                    dogegirisresim.destroy()
                    pencere.quit()

    kayitstarbuton.destroy()

    girisstarbuton.place(rely=0.85, relx=0.4)
    girisstarbuton.configure(
        command=girisonay
    )

    sifreentry = ttk.Entry(
        font="Verdana 16",
        style="entry.TEntry",
        show="●"
    )

    sifreentry.place(rely=0.51, relx=0.2, relwidth=0.4)

    sifreyazi = ttk.Label(
        text="Şifre",
        font="Verdana 12",
        background="#303030"
    )
    
    sifreyazi.place(rely=0.45, relx=0.2)

    emailentry = ttk.Entry(
        font="Verdana 16",
        style="entry.TEntry"
    )

    emailentry.place(rely=0.3, relx=0.2, relwidth=0.4)

    emailyazi = ttk.Label(
        text="Email",
        font="Verdana 12",
        background="#303030"
    )
    
    emailyazi.place(rely=0.24, relx=0.2)

    dogegirisresim = ttk.Label(
        image=photo4,
        background="#303030"
    )

    dogegirisresim.place(rely=0.29, relx=0.75)

kayitstarbuton = ttk.Button(
    style="buton.TButton",
    text="Kayıt Ol",
    command=kayit
    )

girisstarbuton = ttk.Button(
    style="buton.TButton",
    text="Giriş Yap",
    command=giris
    )

entrystil = ttk.Style()

entrystil.configure(
    "entry.TEntry",
    background = "#303030",
    foreground="#B5B5B5",
    font=("Verdana 18 bold")
)

if path.getsize("account.txt") == 0:
    x = (ws/2) - (700/2)
    y = (hs/2) - (400/2)

    pencere.geometry('%dx%d+%d+%d' % (700, 400, x, y))
    pencere.minsize(width=700, height=400)

    kayitstarbuton.place(rely=0.4, relx=0.2)

    girisstarbuton.place(rely=0.4, relx=0.6)

    pencere.mainloop()

else:
    kayitli = True

if kayitli:
    dogesayi = 100
    ekpara = 0
    baslangicdegeri = 0
    arama = collection.find({"email": f"{open('account.txt').readlines()[1].strip()}"})

    for element in arama:
        dogesayi = element["doge"]
        ekpara = element["ek"]

    pencere.minsize(width=700, height=400)
    x = (ws/2) - (700/2)
    y = (hs/2) - (400/2)

    pencere.geometry('%dx%d+%d+%d' % (700, 400, x, y))

    photo3 = PhotoImage(file = r"ayar.png")
    ayarbuton = Button(pencere,
    image = photo3,
    background="#303030",
    borderwidth=0,
    command=profilayar)

    ayarbuton.place(rely=0.02, relx=0.88)

    dogeresim = ttk.Label(text="",
    image = photo6,
    font=("Verdana", 10), 
    foreground="#C8B7EA",
    background="#303030")

    dogeresimartis = ttk.Label(text="",
    image = photo4,
    font=("Verdana", 10), 
    foreground="#C8B7EA",
    background="#303030")

    dogeresimazalis = ttk.Label(text="",
    image = photo5,
    font=("Verdana", 10), 
    foreground="#B5B5B5",
    background="#303030")

    dogeresim.place(relx=0.5, rely=0.35)
    dogeresimartis.pack_forget()
    dogeresimazalis.pack_forget()

    albuton = ttk.Button(
        text="Al",
        style="buton.TButton",
        command= al
    )

    albuton.place(rely=0.35, relx=0.7, relwidth=0.15)

    satbuton = ttk.Button(
        text="Sat",
        style="buton.TButton",
        command=sat
    )

    satbuton.place(rely=0.50, relx=0.7, relwidth=0.15)

    satentry = ttk.Entry(
        style="entry.TEntry",
        font=("Verdana 18 bold")
    )

    satentry.place(rely= 0.5, relx= 0.86, relwidth=0.11, relheight=0.11)

    alentry = ttk.Entry(
        style="entry.TEntry",
        font=("Verdana 18 bold")
    )

    alentry.place(rely= 0.35, relx= 0.86, relwidth=0.11, relheight=0.11)

    cekbuton = ttk.Button(
        text="Çek",
        style="buton.TButton"   
    )

    cekbuton.place(rely=0.67, relx=0.7, relwidth=0.15)

    coinc = ttk.Label(
        font=("Verdana 10 bold"),
        foreground="#B5B5B5",
        background="#303030")

    coinc.place(rely=0.56, relx=0.15)

    coinh = ttk.Label(
        font=("Verdana 10 bold"),
        foreground="#B5B5B5",
        background="#303030")

    coinh.place(rely=0.61, relx=0.15)

    coinl = ttk.Label(
        font=("Verdana 10 bold"),
        foreground="#B5B5B5",
        background="#303030")

    coinl.place(rely=0.66, relx=0.15)

    baslangicdegerilabel = ttk.Label(
        font=("Verdana 10 bold"),
        foreground="#B5B5B5",
        background="#303030",
        text=f"açılış:")

    baslangicdegerilabel.place(rely=0.27, relx=0.7)

    dogesayilabel = ttk.Label(
        font=("Verdana 10 bold"),
        foreground="#B5B5B5",
        background="#303030",
        text=f"Doge: {dogesayi}")

    dogesayilabel.place(rely=0.18, relx=0.7)

    ekparalabel = ttk.Label(
        font=("Verdana 10 bold"),
        foreground="#B5B5B5",
        background="#303030",
        text=f"Ek: {ekpara}")

    ekparalabel.place(rely=0.23, relx=0.7)

    cekilecekparalabel = ttk.Label(
        font=("Verdana 18 bold"),
        foreground="#B5B5B5",
        background="#303030",
        text="0"
    )

    cekilecekparalabel.place(rely=0.685, relx=0.86)


    def connection():
        enableTrace(True)
        webs = websocket.WebSocketApp(SOCKET,
            on_open=on_open,
            on_close= on_close, 
            on_message=on_message)

        webs.run_forever()
        return

    t = Thread(target=connection)
    t.start()

pencere.mainloop()