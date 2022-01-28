import pyglet
#KONSTANTY OKNA
import random
from pyglet import gl
from pyglet.window import key
from pyglet.window import Window
import time
import datetime
w1 = pyglet.window.Window()
w1.set_visible(False)
w2 = pyglet.window.Window()
w2.set_visible(False)





SIRKA = 1000
VYSKA = 700

#LOPTA
VELKOST_LOPTY= 20
RYCHLOST = 2000 #pixely za sekundu

#PALKY
TLSTKA_PALKY = 10
VYSKA_PALKY = 100
RYCHLOST_PALKY =  RYCHLOST * 1.5


#PROSTREDNA CIARA
CIARA_HRUBKA = 20

#FONT
VELKOST_FONTU = 42
ODSADENIE_TEXTU = 30

#STAVOVE PREMENEN
pozicia_palok = [VYSKA //2, VYSKA//2]
pozicia_lopty = [SIRKA//2,VYSKA//2]
rychlost_lopty =[0,0]
stisknute_klavesy = set()
skore = [0,0]

w1.label1 = pyglet.text.Label("Vyhral hráč 1",
                            font_name='Times New Roman',
                            font_size=36,
                            x=w1.width/2, y=w1.height/2,
                            anchor_x='center', anchor_y='center')

w2.label2 = pyglet.text.Label("Vyhral hráč 2",
                            font_name='Times New Roman',
                            font_size=36,
                            x=w2.width/2, y=w2.height/2,
                            anchor_x='center', anchor_y='center')

window = pyglet.window.Window(width=SIRKA,height=VYSKA)


def reset():
    pozicia_lopty[0] = SIRKA//2
    pozicia_lopty[1] = VYSKA//2

    #x-ova rychlost
    if random.randint(0,1):
        rychlost_lopty[0] = RYCHLOST
    else:
        rychlost_lopty[0] = -RYCHLOST

    #y-ova rychlost
    rychlost_lopty[1] = random.uniform(-1,1) * RYCHLOST


def vykresli_obdlznik(x1,y1, x2,y2):
    gl.glBegin(gl.GL_TRIANGLE_FAN)  
    gl.glVertex2f(int(x1), int(y1))  
    gl.glVertex2f(int(x1), int(y2))  
    gl.glVertex2f(int(x2), int(y2))  
    gl.glVertex2f(int(x2), int(y1))  
    gl.glEnd()  

def nakresli_text(text, x, y, pozice_x):
    napis = pyglet.text.Label(text,font_size=VELKOST_FONTU,x=x,y=y,anchor_x=pozice_x)
    napis.draw()


def stisk_klavesnice(symbol, modifikatory):
    if symbol == key.W:
        stisknute_klavesy.add(("hore", 0))
    if symbol == key.S:
        stisknute_klavesy.add(("dole", 0))
    if symbol == key.UP:
        stisknute_klavesy.add(("hore", 1))
    if symbol == key.DOWN:
        stisknute_klavesy.add(("dole", 1))

def pusti_klavesnice(symbol, modifikatory):
    if symbol == key.W:
        stisknute_klavesy.discard(("hore", 0))
    if symbol == key.S:
        stisknute_klavesy.discard(("dole", 0))
    if symbol == key.UP:
        stisknute_klavesy.discard(("hore", 1))
    if symbol == key.DOWN:
        stisknute_klavesy.discard(("dole", 1))

def vykresli():
    """Vykresli stav hry"""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  
    gl.glColor3f(1, 1, 1)  

    
    vykresli_obdlznik(
       pozicia_lopty[0] - VELKOST_LOPTY //2,
       pozicia_lopty[1] - VELKOST_LOPTY //2,
       pozicia_lopty[0] + VELKOST_LOPTY //2,
       pozicia_lopty[1] + VELKOST_LOPTY //2
    )

    for x, y in [(0, pozicia_palok[0]), (SIRKA, pozicia_palok[1])]:
        vykresli_obdlznik(
            x - TLSTKA_PALKY,
            y - VYSKA_PALKY // 2,
            x + TLSTKA_PALKY,
            y + VYSKA_PALKY // 2,
        )

    for y in range(CIARA_HRUBKA // 2, VYSKA, CIARA_HRUBKA * 2):
        vykresli_obdlznik(
            SIRKA // 2 - 1,
            y,
            SIRKA // 2 + 1,
            y + CIARA_HRUBKA
        )
    #CAS
    Cas = datetime.datetime.now().time()

    #vykreslit score
    nakresli_text(str(skore[0]),x=ODSADENIE_TEXTU,y = VYSKA- ODSADENIE_TEXTU - VELKOST_FONTU,pozice_x='left')
    nakresli_text(str(skore[1]),x=SIRKA-ODSADENIE_TEXTU,y = VYSKA- ODSADENIE_TEXTU - VELKOST_FONTU,pozice_x='right')
    #vykresli cas
    nakresli_text(Cas.strftime("%H:%M:%S"), x =(SIRKA/2), y = VYSKA-ODSADENIE_TEXTU - VELKOST_FONTU, pozice_x='center')
    



def obnov_stav(dt):

    #pohyb palok
    for cislo_palky in (0,1):
        if ("hore", cislo_palky) in stisknute_klavesy:
            pozicia_palok[cislo_palky] += RYCHLOST_PALKY * dt
        if ("dole", cislo_palky) in stisknute_klavesy:
            pozicia_palok[cislo_palky] -= RYCHLOST_PALKY * dt
    #dolna zarazka
        if pozicia_palok[cislo_palky] < VYSKA_PALKY /2:
            pozicia_palok[cislo_palky] = VYSKA_PALKY /2
        if pozicia_palok[cislo_palky] > VYSKA - VYSKA_PALKY /2:
            pozicia_palok[cislo_palky] = VYSKA - VYSKA_PALKY /2

    # pohyb lopty
    pozicia_lopty[0] += rychlost_lopty[0] * dt
    pozicia_lopty[1] += rychlost_lopty[1] * dt

    #odrazenie lopty
    if pozicia_lopty[1] < VELKOST_LOPTY //2:
        rychlost_lopty[1] = abs(rychlost_lopty[1])
    if pozicia_lopty[1] > VYSKA - VELKOST_LOPTY //2:
        rychlost_lopty[1] = -abs(rychlost_lopty[1])
    #zistenie borderov palky
    palka_min = pozicia_lopty[1] - VELKOST_LOPTY / 2 - VYSKA_PALKY / 2
    palka_max = pozicia_lopty[1] + VELKOST_LOPTY / 2 + VYSKA_PALKY / 2       

    # odraz zlava
    if pozicia_lopty[0] < TLSTKA_PALKY + VELKOST_LOPTY / 2:
        if palka_min < pozicia_palok[0] < palka_max:
            #odrazenie lopty
            rychlost_lopty[0] = abs(rychlost_lopty[0])
            #palka je inde ako lopta, hrac prehral
        else:
            skore[1] += 1
            reset()
    #odraz zprava
    if pozicia_lopty[0] > SIRKA - VELKOST_LOPTY / 2:
        if palka_min < pozicia_palok[1] < palka_max:
            #odrazenie lopty
            rychlost_lopty[0] = -abs(rychlost_lopty[0])
            #palka je inde ako lopta, hrac prehral
        else:
            skore[0] += 1
            reset()
    def vyhral_hrac_1():
        window.close()
        w1.clear()
        w1.label1.draw()
        w1.set_visible(True)

    if skore[0] >= 10:
        vyhral_hrac_1()


    def vyhral_hrac_2():
        window.close()
        w2.clear()
        w2.label2.draw()
        w2.set_visible(True)

    if skore[1] >= 10:
        vyhral_hrac_2()

        
    
    
    
    
    
    
    



reset()




window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesnice,
    on_key_release=pusti_klavesnice,
)
pyglet.clock.schedule(obnov_stav)


pyglet.app.run()




