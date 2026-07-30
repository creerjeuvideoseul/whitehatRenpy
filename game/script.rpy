# Vous pouvez placer le script de votre jeu dans ce fichier.

# Déclarez sous cette ligne les images, avec l'instruction 'image'
# ex: image eileen heureuse = "eileen_heureuse.png"

# Déclarez les personnages utilisés dans le jeu.
 

default cpu_usage = 40
default cpu_target = 40

default mem_usage = 20
default mem_target = 40

init:
    
    # variable pour le menu qui bouge.
    $ menu_office = ["gui/menu/_main_menu4.png", 1.03,"gui/menu/_main_menu1.png", 1.20,"gui/menu/namebox.png", 1.1]
    $ menu_meeting = ["gui/menu/_main_menu_office.png", 1.07, "gui/menu/_main_menu_claire2.png", 1.15,"gui/menu/_main_menu_cecilia.png", 1]
    $ menu_arr = [menu_office, menu_meeting]
    $ renpy.random.shuffle(menu_arr)
    
    
    $ steam_version = 1 # retire certaine option

    # variable pour les menus à choix limité
    $ timer_range = 0
    $ timer_jump = 0
    $ trigger_key_android = ""
    $ cont_android = 0
    
    $ nomSupervisor = "AnonGhost"
    
    # define config.image_cache_size_mb = 300
    # Declare characters used by this game.
    define n = Character(" ", color="#fff") # narrateur

    define t = DynamicCharacter("player_name", color="#ffff00", image="xSecretGame") # MC
    define k = Character('Kristell Delonay', color="#ff0099", image="xclaire") # Journaliste femme.
    define g = Character('Gilles de la Touret', color="#cc0000", image="xcecilia") # Journaliste homme.
    
    define c = Character('Christine Ranoud', color="#ffccff", image="xlucie") # Mère
    define m = Character('Marek Trodan', color="#FF0000", image="xmarek") # Petit ami
    define a = Character('Alizée Ranoud', color="#bc8f8f", image="xzoe") # Alizée
    define j = Character('Jean Ranoud', color = "#ff0000", image="xzoe") # Père
   
    define h = Character(nomSupervisor, color = "#ff0000", image="xzoe") # Henri
    
        
    define dtime = 0.15 # Dissolve time
    define sentence_already_talk = _("Je lui est déjà parlé aujourd'hui, je ne vais pas insister.")
    
    $ wet = ImageDissolve("gui/wipes/wet.jpg", 2.0, 8)
    $ glasswool = ImageDissolve("gui/wipes/glasswool.jpg", 1.0, 8)
    $ shot = ImageDissolve("gui/wipes/shot.png", 1.0, 8)
    $ shatter = ImageDissolve("gui/wipes/shatter.png", 1.0, 8)
    $ rain1 = ImageDissolve("gui/wipes/rain1.jpg", 1.0, 8)
    $ rain2 = ImageDissolve("gui/wipes/rain2.jpg", 1.0, 8)
    $ vitesse = ImageDissolve("gui/wipes/19.jpg", 1.0, 8)
    $ nuage = ImageDissolve("gui/wipes/12.jpg", 1.0, 8)
    $ peintureH = ImageDissolve("gui/wipes/17.png", 1.0, 8)
    $ peintureV = ImageDissolve("gui/wipes/18.png", 1.0, 8)
    $ pixel = ImageDissolve("gui/wipes/pix3.png", 1.0, 8)
    $ tcircle = ImageDissolve("gui/wipes/circlewipe-cw.jpg", 1.0, 8)
    $ zcircle = ImageDissolve("gui/wipes/18.png", 1.0, 8)
    # $ sshake = Shake((0, 0, 0, 0), 3, dist=5)    
    
    define circleirisout = ImageDissolve("images_png/circleiris.png", 3.0, 8) # How to use : with circleirisout + media.rpy
    define circleirisin = ImageDissolve("images_png/circleiris.png", 3.0, 8 , reverse=True) # How to use : with circleirisin + media.rpy
    define circlerandom = AlphaDissolve("spotlighteffect", delay=3.5) # How to use : with circlerandom + media.rpy
    
    define flashbulb = Fade(0.2, 0.0, 0.8, color='#fff') 
 
    define title2 = Text("Blooming Witches", font=gui.text_font, line_spacing=-230, color="#c90", size=240, outlines=[(5, '#c90', 0, 0), (0, '#fb0', -5, -5), (0, '#960', 5, 5)])

    transform splasher(maintime=3, xoff=0, offtime=.4, alph=0): # takes exactly maintime+offtime seconds, alph is boolean
        truecenter
        subpixel True
        zoom 0
        linear .1 zoom .5
        linear maintime zoom 1
        easeout offtime zoom 1000 xoffset xoff alpha alph

default heure_h = 12
default heure_m = 3
default heure_s = 0
default heure_system = "12h03"

init python:
    
    def update_heure_system():
        global heure_h, heure_m, heure_s

        store.heure_s += 1
        if store.heure_s >= 60:
            store.heure_s = 0
            store.heure_m += 1
            if store.heure_m >= 60:
                store.heure_m = 0
                store.heure_h = (store.heure_h + 1) % 24

        store.heure_system = "%02dh%02d" % (store.heure_h, store.heure_m)
        
        
###############################################
# MENU2:  fonction zoom pour le menu qui bouge.
################################
init 499 image spr_bg:
    menu_arr[0][0] with Dissolve(0.2, alpha=True)
    zoom 1.0
    xalign 0.0 yalign 0.0
    linear 10.0 zoom menu_arr[0][1]
    menu_arr[1][0] with Dissolve(0.2, alpha=True)
    zoom 1.0
    xalign 0.0 yalign 0.0
    linear 10.0 zoom menu_arr[0][1] 
    repeat
init 499 image spr_mid:
    menu_arr[0][2] with Dissolve(0.2, alpha=True)
    zoom 1.0
    xalign 0.0 yalign 0.0
    linear 10.0 zoom menu_arr[0][3]
    menu_arr[1][2] with Dissolve(0.2, alpha=True)
    zoom 1.0
    xalign 0.0 yalign 0.0
    linear 10.0 zoom menu_arr[1][3] 
    repeat
init 499 image spr_top:
    menu_arr[0][4] with Dissolve(0.2, alpha=True)
    zoom 1.0
    xalign 0.0 yalign 0.0
    linear 10.0 zoom menu_arr[0][5]
    menu_arr[1][4] with Dissolve(0.2, alpha=True)
    zoom 1.0
    xalign 0.0 yalign 0.0
    linear 10.0 zoom menu_arr[1][5] 
    repeat

transform fullsize: # change de tailler d'ecran.
    size (2560,1440)
    on show:
        yalign 0.5 xalign 0.5

transform flougaussien(child):
    contains:
        child
        alpha 0.7
    contains:
        child
        alpha 0.2 zoom 1.03
    contains:
        child
        alpha 0.2 zoom 1.015
    contains:
        child
        alpha 0.2 zoom 0.990
    contains:
        child
        alpha 0.2 zoom 0.980
        

#########################################
#'''
#"Function" button à cliquer par le joueur.
#calls the qte screen
#parameters are:
#    - amount of time given
#    - total amount of time (is usually the same as above)
#    - timer decreasing interval
#    - the key/keyboard input to hit in the quick time event
#    - the x alignment of the bar/box
#    - the y alignment of the bar/box
#'''
################################

label qte_setup(time_start, time_max, interval, typebutton, x_align, y_align):

    $ time_start = time_start
    $ typebutton = typebutton
    $ time_max = time_max
    $ interval = interval
    $ trigger_key = []
    $ trigger_key_display = ""

    $ x_align = random.randint(1, 9) * 0.1
    $ y_align = random.randint(1, 9) * 0.1

    $ arr_keys         = ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_SPACE"] #list of keyboard inputs to be selected from. See https://www.pygame.org/docs/ref/key.html for more keys
    $ arr_keys_display = [__("Gauche"), __("Droite"), __("Haut"), __("Bas"), __("Barre espace")] #list of keyboard inputs to be selected from. See https://www.pygame.org/docs/ref/key.html for more keys
    $ trigger_key = random.choice(arr_keys)
 
    $ trigger_key_display = arr_keys_display[arr_keys.index(trigger_key)]

    if typebutton == "alttab":
        call screen qte_button_alttab()
    elif typebutton == "keypress":
        call screen qte_button_keypress(trigger_key_display)
    else:
        play sound "sound/gui/correct-answer-marimba-02.mp3"
        call screen qte_button

    # can change to "call screen qte_button" to switch to button mode
    
    if cont_android == 1 or _return == 1:
        if typebutton == "keypress":
            play sound "sound/gui/correct-answer-marimba-02.mp3"
        $ cont += 1
    else:
        play sound "sound/gui/wrong-answer-fall-03.mp3" # wrong-answer-trombone-02.mp3

    # 1 if key was hit in time, 0 if key not

    return
        
init python:
    
    def update_cpu_usage():
        global cpu_usage, cpu_target

        # De temps en temps, on tire une nouvelle cible aléatoire entre 20 et 60%
        if renpy.random.random() < 0.1:  # ~10% de chance à chaque tick de changer de cible
            store.cpu_target = renpy.random.randint(20, 60)

        # On avance doucement la valeur actuelle vers la cible (pas de saut brutal)
        if store.cpu_usage < store.cpu_target:
            store.cpu_usage = min(store.cpu_usage + 1, store.cpu_target)
        elif store.cpu_usage > store.cpu_target:
            store.cpu_usage = max(store.cpu_usage - 1, store.cpu_target)
        
    def update_mem_usage():
        global mem_usage, mem_target

        # De temps en temps, on tire une nouvelle cible aléatoire entre 20 et 60%
        if renpy.random.random() < 0.1:  # ~10% de chance à chaque tick de changer de cible
            store.mem_target = renpy.random.randint(20, 60)

        # On avance doucement la valeur actuelle vers la cible (pas de saut brutal)
        if store.mem_usage < store.mem_target:
            store.mem_usage = min(store.mem_usage + 1, store.mem_target)
        elif store.mem_usage > store.mem_target:
            store.mem_usage = max(store.mem_usage - 1, store.mem_target)


# Gestion des indices :
default indices_debloques = set()     

init python:
    
    def indice_hyperlink(cible):
        """Appelé quand le joueur clique sur un lien {a=indice:xxx}...{/a}"""
        if cible not in indices_debloques:
            indices_debloques.add(cible)
            renpy.notify("Nouvel indice débloqué !")

    config.hyperlink_handlers["indice"] = indice_hyperlink
    
style hyperlink_text:
    color "#ff9900"
    hover_color "#ffcc66"
    underline True
    
    
    
    
# Le jeu commence ici
label start:
    
    jump introduction

