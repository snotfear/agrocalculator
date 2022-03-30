import os
import os.path
import codecs
from tkinter import *
from tkinter.ttk import Combobox

# модуль codecs используется при открытии файлов с кирилицей для правльного декодирования

os.chdir('database')
spisok_kultur = []
predsh_list = []
predsh_list_for_combobox = []
plant_list = []
pochva_list = []
gruppa_kultury = 0

# Создаём список культур по файлам. Позже этот список будет использовться
# для подгрузки необходимых файлов, а так же выбора культуры.
# Из списка исклчается файл "Предшественники.txt", т.к. он будет использоваться потом напрямую
for i in os.listdir():
    if i != 'Предшественники.txt':
        spisok_kultur.append(i[:-4])

# считываем Предшественники и добавляем в таблицу predsh_list
with codecs.open('Предшественники.txt', encoding='utf-8') as pred_txt:
    pred = pred_txt.read().splitlines()
for i in pred:
    predsh_list.append(i.split('.'))
    predsh_list_for_combobox.append((i[:-2]))

# Часть ответственная за интерфейс.
window = Tk()
window.title('Агрокалькулятор v0.01')
window.geometry('450x300')

lbl_spisok_kultur = Label(window, text='Выберете культуру:')
lbl_spisok_kultur.grid(column=0, row=0)
combo_spisok_kultur = Combobox(window)
combo_spisok_kultur['values'] = spisok_kultur
combo_spisok_kultur.current(0)
combo_spisok_kultur.grid(column=1, row=0)


def click_kultura():
    plant = combo_spisok_kultur.get()
    with codecs.open(plant + '.txt', encoding='utf-8') as plant_txt:
        plant_temp = plant_txt.read().splitlines()
    for i in plant_temp:
        plant_list.append(i.split('.'))
    for i in range(1, len(plant_list)):
        pochva_list.append(plant_list[i][0])
    # Присваиваем культуре группу для применения индекса поправки от содержания элементов в почве
    global gruppa_kultury
    gruppa_kultury = int(plant_list[0][0])
    combo_spisok_pochv['values'] = pochva_list
    combo_spisok_pochv.current(0)


btn_kultur = Button(window, text='Подтвердить', command=click_kultura)
btn_kultur.grid(column=2, row=0)

lbl_spisokpochv = Label(window, text='Выберете почву:')
lbl_spisokpochv.grid(column=0, row=1)
combo_spisok_pochv = Combobox(window)
combo_spisok_pochv['values'] = pochva_list
combo_spisok_pochv.grid(column=1, row=1)

lbl_predsh = Label(window, text='Выберете предшественник:')
lbl_predsh.grid(column=0, row=2)
combo_predsh = Combobox(window)
combo_predsh['values'] = predsh_list_for_combobox
combo_predsh.current(0)
combo_predsh.grid(column=1, row=2)

chk_state = BooleanVar()
chk_state.set(False)
chk_button = Checkbutton(window, text='Есть анализ почвы', var=chk_state)
chk_button.grid(columns=2, row=4)

analyz_status = False


def chk():
    global analyz_status
    if chk_state.get() == True:
        azot_entry.configure(state='normal')
        fosfor_entry.configure(state='normal')
        kalij_entry.configure(state='normal')
        analyz_status = True
    else:
        azot_entry.configure(state='disabled')
        fosfor_entry.configure(state='disabled')
        kalij_entry.configure(state='disabled')
        analyz_status = False


btn_chk = Button(window, text='Подтвердить', command=chk)
btn_chk.grid(column=2, row=4)

lbl_azot_entry = Label(window, text='Азот')
lbl_azot_entry.grid(column=0, row=5)
lbl_fosfor_entry = Label(window, text='Фосфор')
lbl_fosfor_entry.grid(column=1, row=5)
lbl_kalij_entry = Label(window, text='Калий')
lbl_kalij_entry.grid(column=2, row=5)

azot_entry = Entry(window, width=5, state='disabled')
azot_entry.grid(column=0, row=6)
fosfor_entry = Entry(window, width=5, state='disabled')
fosfor_entry.grid(column=1, row=6)
kalij_entry = Entry(window, width=5, state='disabled')
kalij_entry.grid(column=2, row=6)

lbl_itog = Label(window)
lbl_itog.grid(columns=3, row=8)


def itog():
    global analyz_status
    global azot_entry
    global fosfor_entry
    global kalij_entry
    koef_azot = 1
    koef_fosfor = 1
    koef_kalij = 1
    predshestv_group = 0
    navoz = int()
    azot = 0
    fosfor = 0
    kalij = 0
    predstv_get = combo_predsh.get()
    for i in predsh_list:
        if predstv_get == i[0]:
            predshestv_group = i[1]
    for i in plant_list:
        if i[0] == combo_spisok_pochv.get():
            if predshestv_group == str(0):
                navoz = int(i[2])
                azot = int(i[4])
                fosfor = int(i[6])
                kalij = int(i[8])
            elif predshestv_group == str(1):
                navoz = (int(i[1]) + int(i[2])) / 2
                azot = (int(i[3]) + int(i[4])) / 2
                fosfor = (int(i[5]) + int(i[6])) / 2
                kalij = (int(i[7]) + int(i[8])) / 2
            elif predshestv_group == str(2):
                if int(i[1]) == 0:
                    navoz = int(i[2]) * 0.3
                else:
                    navoz = int(i[1])
                if int(i[3]) == 0:
                    azot = int(i[4]) * 0.3
                else:
                    azot = int(i[3])
                if int(i[5]) == 0:
                    fosfor = int(i[6]) * 0.3
                else:
                    fosfor = int(i[5])
                if int(i[7]) == 0:
                    kalij = int(i[8]) * 0.3
                else:
                    kalij = int(i[7])

    chernozemy_vysheloch = {'Чернозём выщелоченный', 'Тёмно-каштановые', 'Каштановые', 'Светло-каштановые', 'Чернозем выщелоченный'}
    chernozemy_obyknoven = {'Чернозём обыкновенный', 'Чернозём типичный', 'Чернозём южный', 'Чернозем обыкновенный', 'Чернозем типичный', 'Чернозем южный'}
    if analyz_status == True:
        if combo_spisok_pochv.get() in chernozemy_vysheloch:
            if gruppa_kultury == 1:
                if int(azot_entry.get()) < 30:
                    koef_azot = 1
                if 30 < int(azot_entry.get()) < 45:
                    koef_azot = 0.5
                if 45 < int(azot_entry.get()) < 60:
                    koef_azot = 0.3
                if int(azot_entry.get()) > 60:
                    koef_azot = 0
                if int(fosfor_entry.get()) < 150:
                    koef_fosfor = 1
                if 150 < int(fosfor_entry.get()) < 200:
                    koef_fosfor = 0.6
                if 200 < int(fosfor_entry.get()) < 300:
                    koef_fosfor = 0.3
                if int(fosfor_entry.get()) > 300:
                    koef_fosfor = 0.2
                if int(kalij_entry.get()) < 90:
                    koef_kalij = 1
                if 90 < int(kalij_entry.get()) < 120:
                    koef_kalij = 0.5
                if int(kalij_entry.get()) > 120:
                    koef_kalij = 0
            if gruppa_kultury == 2:
                if int(azot_entry.get()) < 15:
                    koef_azot = 1.5
                if 15 < int(azot_entry.get()) < 30:
                    koef_azot = 1.25
                if 30 < int(azot_entry.get()) < 45:
                    koef_azot = 1
                if 45 < int(azot_entry.get()) < 60:
                    koef_azot = 0.66
                if int(azot_entry.get()) > 60:
                    koef_azot = 0.3
                if int(fosfor_entry.get()) < 100:
                    koef_fosfor = 1.5
                if 100 < int(fosfor_entry.get()) < 150:
                    koef_fosfor = 1.25
                if 150 < int(fosfor_entry.get()) < 200:
                    koef_fosfor = 1
                if 200 < int(fosfor_entry.get()) < 300:
                    koef_fosfor = 1
                if int(fosfor_entry.get()) > 300:
                    koef_fosfor = 0.5
                if int(kalij_entry.get()) < 60:
                    koef_kalij = 1.3
                if 60 < int(kalij_entry.get()) < 120:
                    koef_kalij = 1
                if 120 < int(kalij_entry.get()) < 180:
                    koef_kalij = 0.66
                if int(kalij_entry.get()) > 180:
                    koef_kalij = 0.3
            if gruppa_kultury == 3:
                if int(azot_entry.get()) < 30:
                    koef_azot = 1.5
                if 30 < int(azot_entry.get()) < 45:
                    koef_azot = 1.25
                if 45 < int(azot_entry.get()) < 60:
                    koef_azot = 1
                if int(azot_entry.get()) > 60:
                    koef_azot = 0.66
                if int(fosfor_entry.get()) < 150:
                    koef_fosfor = 1.5
                if 150 < int(fosfor_entry.get()) < 200:
                    koef_fosfor = 1.25
                if 200 < int(fosfor_entry.get()) < 300:
                    fosfor_entry = 1
                if int(fosfor_entry.get()) > 300:
                    fosfor_entry = 0.66
                if int(kalij_entry.get()) < 90:
                    koef_kalij = 1.5
                if 90 < int(kalij_entry.get()) < 120:
                    koef_kalij = 1.3
                if 120 < int(kalij_entry.get()) < 180:
                    kalij_entry = 1
                if int(kalij_entry.get()) > 180:
                    kalij_entry = 0.66
        if combo_spisok_pochv.get() in chernozemy_obyknoven:
            if gruppa_kultury == 1:
                if int(azot_entry.get()) < 15:
                    koef_azot = 1
                if 15 < int(azot_entry.get()) < 30:
                    koef_azot = 0.5
                if 30 < int(azot_entry.get()) < 60:
                    koef_azot = 0.3
                if int(azot_entry.get()) > 60:
                    koef_azot = 0
                if int(fosfor_entry.get()) < 30:
                    koef_fosfor = 1
                if 30 < int(fosfor_entry.get()) < 45:
                    koef_fosfor = 0.6
                if 45 < int(fosfor_entry.get()) < 60:
                    koef_fosfor = 0.3
                if int(fosfor_entry.get()) > 60:
                    koef_fosfor = 0.2
                if int(kalij_entry.get()) < 300:
                    koef_kalij = 1
                if 300 < int(kalij_entry.get()) < 400:
                    koef_kalij = 0.5
                if int(kalij_entry.get()) > 400:
                    koef_kalij = 0
            if gruppa_kultury == 2:
                if int(azot_entry.get()) < 8:
                    koef_azot = 1.5
                if 8 < int(azot_entry.get()) < 15:
                    koef_azot = 1.25
                if 15 < int(azot_entry.get()) < 30:
                    koef_azot = 1
                if 30 < int(azot_entry.get()) < 60:
                    koef_azot = 0.66
                if int(azot_entry.get()) > 60:
                    koef_azot = 0.3
                if int(fosfor_entry.get()) < 15:
                    koef_fosfor = 1.5
                if 15 < int(fosfor_entry.get()) < 30:
                    koef_fosfor = 1.25
                if 30 < int(fosfor_entry.get()) < 45:
                    koef_fosfor = 1
                if 45 < int(fosfor_entry.get()) < 60:
                    koef_fosfor = 1
                if int(fosfor_entry.get()) > 60:
                    koef_fosfor = 0.5
                if int(kalij_entry.get()) < 200:
                    koef_kalij = 1.3
                if 200 < int(kalij_entry.get()) < 400:
                    koef_kalij = 1
                if 400 < int(kalij_entry.get()) < 600:
                    koef_kalij = 0.66
                if int(kalij_entry.get()) > 600:
                    koef_kalij = 0.3
            if gruppa_kultury == 3:
                if int(azot_entry.get()) < 15:
                    koef_azot = 1.5
                if 15 < int(azot_entry.get()) < 30:
                    koef_azot = 1.25
                if 30 < int(azot_entry.get()) < 60:
                    koef_azot = 1
                if int(azot_entry.get()) > 60:
                    koef_azot = 0.66
                if int(fosfor_entry.get()) < 30:
                    koef_fosfor = 1.5
                if 30 < int(fosfor_entry.get()) < 45:
                    koef_fosfor = 1.25
                if 45 < int(fosfor_entry.get()) < 60:
                    fosfor_entry = 1
                if int(fosfor_entry.get()) > 60:
                    fosfor_entry = 0.66
                if int(kalij_entry.get()) < 300:
                    koef_kalij = 1.5
                if 300 < int(kalij_entry.get()) < 400:
                    koef_kalij = 1.3
                if 400 < int(kalij_entry.get()) < 600:
                    kalij_entry = 1
                if int(kalij_entry.get()) > 600:
                    kalij_entry = 0.66

    itog_txt = ('Навоз = ' + str(navoz) + 'т,', 'азот = ' + str(azot * koef_azot) + 'кг,', 'Фосфор = '
                + str(fosfor * koef_fosfor) + 'кг,', 'Калий = ' + str(kalij * koef_kalij) + 'кг')
    lbl_itog.configure(text=(itog_txt))


btn_itog = Button(window, text='Посчитать', command=itog)
btn_itog.grid(column=2, row=7)

combo_spisok_kultur.focus()

window.mainloop()
