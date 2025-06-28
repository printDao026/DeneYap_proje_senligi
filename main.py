import serial
import threading
import tkinter as tk
from tkinter import ttk
import time
import winsound
from tkinter import messagebox
import requests
from gtts import gTTS
import playsound
import os



ser = serial.Serial("COM6", 9600, timeout=1)
time.sleep(2)

son_veri = ""
tehlike_modu=0
seriport_durdur=0
def sesli_soyle(metin, dil="tr"):
    try:
        tts = gTTS(text=metin, lang=dil)
        tts.save("ses.mp3")
        playsound.playsound("ses.mp3")
        os.remove("ses.mp3")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def satir_baslarini_ekle(metin, karakter_sayisi=50):
    return '\n'.join(metin[i:i+karakter_sayisi] for i in range(0, len(metin), karakter_sayisi))
def ollama_cevap():
    giris = (
    "Sen bir Afet Botusun. Türkçe, kısa ve öz cevap ver. "
    "Her 30 karakterde satır başı yap. "
    "Bunu kullanıcı bilmeyecek. "
    "Soru: "
)
    prompt = yazi_kismi.get()
    prompt_s = giris + prompt

    url = "http://localhost:11434/api/generate"
    data = {
        "model": "deepseek-r1",
        "prompt": prompt_s,
        "stream": False
    }
    try:
        response = requests.post(url, json=data)
        cevap_json = response.json()
                
        cevap = cevap_json["response"]
        parca = cevap.split("</think>")[-1].strip()

        parca_duzenli = satir_baslarini_ekle(parca)

        yapay_zeka_cevap.config(text=parca_duzenli)
        print(parca_duzenli)

        print(parca)

    except Exception as e:
        print(f"Hata oluştu: {e}")

def uyari_deprem_var_mi():
    veri = requests.get("https://api.orhanaydogdu.com.tr/deprem/kandilli/live").json()
    deprem = veri["result"][0]
    baslik = deprem["title"].lower()
    sehirler = []
    yeni_pencere = tk.Toplevel()
    yeni_pencere.title("Deprem Durumu")
    try:
        for s in deprem["location_properties"]["closestCities"]:
            sehirler.append(s["name"].lower())

        if "adana" in baslik or "adana" in sehirler:
            label_analiz=tk.Label(yeni_pencere, text="analiz ediliyor...", font=("Arial", 14), padx=20, pady=20).pack()
            time.sleep(1)
            
            tk.Label(yeni_pencere, text="Adana veya Adananın yakınında deprem olmuştur", font=("Arial", 14), padx=20, pady=20).pack()
            
        else:
            label_analiz=tk.Label(yeni_pencere, text="analiz ediliyor...", font=("Arial", 14), padx=20, pady=20).pack()
            time.sleep(1)
            tk.Label(yeni_pencere, text="Adana yakınında deprem yok", font=("Arial", 14), padx=20, pady=20).pack()
    except:
        label_analiz=tk.Label(yeni_pencere, text="analizde hata verildi", font=("Arial", 14), padx=20, pady=20).pack()



def zil():
    try:
        winsound.Beep(2000,1000)
    except:
        print("Seste hata çıktı")
def uyari():
    messagebox.showerror(title="DEPREM UYARISI",message="DEPREM SENSORUMUZ BİR SALLANTI TESPİT ETMİŞTİR")

def veri_oku():
    global tehlike_modu
    global son_veri
    while True:
        try:
            if ser.in_waiting:
                veri = ser.readline().decode().strip()
                if veri != son_veri:
                    son_veri = veri
                    print(son_veri)
                    if "Yangin:" in son_veri:
                        print("merhaba")
                        print(son_veri)
                        yangin.config(text=son_veri)
                    if seriport_durdur==1:
                        seriport_button.config(text="🟢 Başlat")
                        seriport.config(state="disabled")
                    elif seriport_durdur==0:
                        seriport_button.config(text="🔴 Seri Portu \nDurdur")
                        seriport.config(state="normal")
                        seriport.insert(tk.END, f"{son_veri}\n")
                        seriport.see(tk.END)
                        seriport.config(state="disabled")
                if son_veri == "DEPREM":
                    threading.Thread(target=zil, daemon=True).start()
                    sesli_soyle("BU BİR DEPREM uyarısıdır")
                    time.sleep(1)
                    uyari()
                    time.sleep(1) 
                    threading.Thread(target=uyari_deprem_var_mi, daemon=True).start()
                    
   
                    

        except Exception as e:
            print("Hata var",e)
        time.sleep(0.1)



window = tk.Tk()
window.title("")

window.geometry("1080x720")

def led_ac():
    ser.write(bytes([1]))
def led_kapa():
    ser.write(bytes([0]))

tabs=ttk.Notebook(window,width=720,height=540)
tabs.place(x=170,y=50)

tab1=ttk.Frame(tabs,width=50,height=50)
tab2=ttk.Frame(tabs,width=50,height=50)
tab3=ttk.Frame(tabs,width=50,height=50)
tab4=ttk.Frame(tabs,width=50,height=50)
tk.Label(tab1,text="🚨 Led Aç/kapa", font=("Segoe UI", 20, "bold"), fg="#222").pack()


tabs.add(tab1,text="Led")
tabs.add(tab2,text="Yapay Zeka")
tabs.add(tab3,text="Sensor Veri")
tabs.add(tab4,text="Seri Port")

led_ac_but = tk.Button(tab1, text="Ledi Aç", width=20, height=2, fg="white", bg="green", command=led_ac)
led_ac_but.pack(pady=30)

led_kapa_but = tk.Button(tab1, text="Ledi Kapa", width=20, height=2, fg="white", bg="red", command=led_kapa)
led_kapa_but.pack(pady=10)


tk.Label(tab2,text="🤖 Yapay Zeka",font=("Segoe UI", 20, "bold"),fg="#222").grid(row=0,column=0,padx=275)
yazi_kismi=tk.Entry(tab2,state="normal",width=70,bd=3, relief="solid",font=("Segoe UI", 12),bg="#020202", fg="#FFFFFF")
yazi_kismi.insert(index=0,string="Yapay Zekaya bir soru sor")
yazi_kismi.grid(row=1,column=0)

yapay_zeka_cevap=tk.Label(tab2,text="",font=("Segoe UI", 12, "italic"))
yapay_zeka_cevap.grid(row=2,column=0)

tiklama_buton=tk.Button(tab2,text="Gönder",font=("Segoe UI", 12, "bold"),bg="#4CAF50",fg="white",activebackground="#45a049",activeforeground="white",bd=0,relief="flat",command=ollama_cevap)
tiklama_buton.grid(row=3,column=0)

tk.Label(tab3,text="🔌Sensör durumları",font=("Segoe UI", 20, "bold")).grid(row=0,column=0,padx=250)


def seriport_button_com():
    global seriport_durdur
    if seriport_durdur == 0:
        seriport_durdur=1
    elif seriport_durdur==1:
        seriport_durdur=0

tk.Label(tab4, text="💻Seri Port Ekranı", font=("Segoe UI", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=250)

seriport = tk.Text(tab4, width=40, height=20, wrap="word",state="disabled") 
seriport.grid(row=1, column=0, pady=10)

scroll = tk.Scrollbar(tab4, orient=tk.VERTICAL, command=seriport.yview)
scroll.grid(row=1, column=1, sticky=tk.N + tk.S, pady=10)

seriport.config(yscrollcommand=scroll.set)

seriport_button = tk.Button(tab4, text="🔴 Seri Portu Durdur", font=("Segoe UI", 12, "bold"),width=15, height=2, relief="raised", bd=3, command=seriport_button_com)
seriport_button.grid(row=2,column=0)

yangin=tk.Label(tab3,text="Yangin: ",font="Times 25")
yangin.grid(row=1,column=0)


threading.Thread(target=veri_oku,daemon=True).start()
window.mainloop()
ser.close()
