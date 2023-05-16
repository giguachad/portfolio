#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *

import webbrowser
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandastable import Table

# Creating table

url = "https://www.investing.com/indices/investing.com-us-500-components"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
soup

table1 = soup.find("table", class_="genTbl closedTbl crossRatesTbl elpTbl elp25")
headers = table1.find_all("th")
titles = []
for i in headers:
    title = i.text
    titles.append(title)

df_d = pd.DataFrame(columns=titles)
rows = table1.find_all("tr")

for i in rows[1:]:
    data = i.find_all("td")
    row = [tr.text for tr in data]
    l = len(df_d)
    df_d.loc[l] = row

# model's table

url_git = "https://raw.githubusercontent.com/giguachad/portfolio/main/df.csv"
df = pd.read_csv(url_git)
df.head()

# program

root = Tk()
frame = Frame(root)
frame.pack(side=LEFT)
rightframe = Frame(root)
rightframe.pack(side=RIGHT)
rightframe2 = Frame(root)
rightframe2.pack(side=RIGHT)
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)
root.geometry("1400x600")

# Link GitHub 10
def openlink():
    webbrowser.open("https://github.com/giguachad/portfolio")

gitbutton = Button(frame, text="GitHub", command=openlink)
gitbutton.pack(side=BOTTOM)

# Text bar 1

ourMessage = 'Вітаю! Ця програма створена для допомоги Вам у створенні інвестиційного портфелю. Допомогу буде здійснювати моя модель, яка проаналізувала ціни та загальну тенденцію конкретних акцій, та буде давати Вам поради, у які саме акції варто інвестувати. Удачі! Зворотній контакт Tg: @giguachad'
messageVar = Message(frame, text=ourMessage)
messageVar.config(bg='gray')

messageVar.pack(side=TOP)

# Table 8
rightlabel = Message(rightframe2, text="Тут показана таблиця з сайту investing.com. Ви можете переглянути останні тенденції всіх компаній з S&P500.")
rightlabel.pack()

pt = Table(rightframe, dataframe=df_d, weight=600, height=300)

pt.show()

# input money 3
label1 = Label(root, text="Введіть кількість коштів, які б Ви хотіли інвестувати:")
label1.pack()
e1 = Entry(root)

e1.pack()

def save_money():
    money = e1.get()
    return money

btn = Button(root, text="Зберегти значення", command=save_money)
btn.pack()

# period of investment 6
selected = StringVar()

def select():
    chosed_label = selected.get()
    return chosed_label


txt = ["Короткостроковий(1 день - 1 тиждень)", "Середньостроковий(1 місяць - декілька місяців)",
       "Довгостроковий(1 рік - 3 роки"]
values_t = ["DWLabel", "MYTDLabel", "MYYLabel"]

label2 = Label(root, text="Оберіть період, протягом якого плануєте утримувати акції:")
label2.pack()
for i in range(3):
    rdbutton = Radiobutton(root, text=txt[i], value=values_t[i], variable=selected, command=select)
    rdbutton.pack()

# % max investment

label3 = Label(root, text="Введіть максимальний % присутності однієї з компаній портфелі:")
label3.pack()
e2 = Entry(root)

e2.pack()

def max_perc():
    perc = e2.get()
    return perc


btn1 = Button(root, text="Зберегти значення", command=max_perc)
btn1.pack()

showdf=pd.DataFrame()

# Main table
# Count of investing companies
def working():
    count_comp = 100 / float(max_perc())
    count_comp = np.around(count_comp, 2)
    newdf = df.copy()
    newdf["Last"] = df_d["Last"]
    newdf["Last"] = newdf["Last"].str.replace(",","")
    newdf["Last"] = newdf["Last"].astype("float64")
    if select() == "MYYLabel":
        newdf = newdf[["Name", "Last", select(), "Year_1", "Years_3"]]
    elif select() == "MYTDLabel":
        newdf = newdf[["Name", "Last", select(), "Month_1", "YTD"]]
    elif select() == "DWLabel":
        newdf = newdf[["Name", "Last", select(), "Daily", "Week_1"]]
    count_comp = int(count_comp)

    newdf = newdf.sort_values(by=[newdf.columns[-2], newdf.columns[-1]], ascending=False)

    sm_value = int(save_money())
    mp = float(max_perc())
    sm = float(save_money())
    newdf = newdf.reset_index()
    newdf["Num of stocks"] = 0
    multiply = sm*mp/100
    print(multiply)
    for j in range(count_comp):
        separator = 0
        while sm_value // newdf["Last"][j] >= 1 and newdf["Num of stocks"][j]*newdf["Last"][j]<=multiply:
            separator += 1
            newdf["Num of stocks"][j] = separator
        sm_value = sm_value - newdf["Num of stocks"][j]*int(newdf["Last"][j])
    newdf = newdf.sort_values("Num of stocks", ascending=False)
    return newdf
def showtable():
    table1 = Table(bottomframe, dataframe=working())
    table1.show()
    print(working())

btn1 = Button(root, text="Створити портфель", command=working)
btn1.pack()
btn2 = Button(root, text="Виведення таблиці з портфоліо", command=showtable)
btn2.pack()

root.mainloop()
