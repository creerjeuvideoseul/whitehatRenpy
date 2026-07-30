    
label introduction:
    
    $ player_name = renpy.input(__("Quel doit être votre nom de personnage ?"), default="WhiteHat", length=15) or "WhiteHat"
    $ player_name = player_name.strip()
    if player_name == "":
        $ player_name = "WhiteHat"
        
    scene wh_intro_fille_tele2 with Dissolve(dtime)
    k "300%% d'augmentation !"
    scene wh_show_television_triste3 with Dissolve(dtime)
    k "Et non je ne parle pas de mon salaire, mais bien de la {color=#ffa500}cybercriminalité{/color}"
    scene wh_intro_femme_colere2 with Dissolve(dtime)
    k "Nous ne sommes plus à l'abri nulle part, les systèmes financiers sont au bord de la rupture."
    scene wh_intro_fille_tele2 with Dissolve(dtime)
    k "Mais heureusement nos bien aimés gouvernements travaillent conjointement depuis des années sur une solution miracle : {color=#ffa500}Sentinelle{/color}."
    k "Gilles, notre expert en technologie, pouvez-vous nous en dire plus ?"
    
    
    scene wh_show_television_homme1 with Dissolve(dtime)
    g "En effet, Karine, Sentinelle est LA solution à tous nos malheurs. C’est la première intelligence…"
    scene wh_avec_ordi_quantique with Dissolve(dtime) 
    g "... établie sur des serveurs {color=#ffa500}quantiques !{/color}"
    scene wh_show_television_homme1 with Dissolve(dtime)
    g "C'est-à-dire qu'elle peut être partout à la fois... et en même temps, c'est comme si elle n'était pas là !"
    scene wh_intro_femme_tourne_oeil with Dissolve(dtime)
    k "Je n'y comprends rien Gilles !"
    scene wh_show_television_homme1 with Dissolve(dtime) 
    g "C'est normal, Karine..."
    scene wh_show_television_homme3 with Dissolve(dtime) 
    g "... c'est quantique !"
    scene wh_show_television_enerve2 with Dissolve(dtime)
    k "En clair, Sentinelle surveille tout le monde, partout, et tout le temps, Gilles ?"
    scene wh_show_television_homme2 with Dissolve(dtime)
    g "Oui ! Et si nous n'agissons pas bien, Sentinelle nous attrape et nous punit !"
    scene wh_intro_femme_tourne_oeil with Dissolve(dtime)
    k "Ça fait froid dans le dos, Gilles !"
    scene wh_show_television_homme_enerve with Dissolve(dtime) 
    g "Vous avez quelque chose à cacher, Karine ?"
    scene wh_intro_femme_colere2 with Dissolve(dtime) 
    k "Ce n'est pas la question ! Et notre {color=#ffa500}vie privée{/color} Gilles?"
    scene wh_show_television_homme1 with Dissolve(dtime)
    g "Ça n'existe pas pour Sentinelle !"
    g "On peut leur faire confiance pour une utilisation responsable, un comité de contrôle des demandes a été formé quand même !"
    scene wh_intro_fille_tele2 with Dissolve(dtime)
    k "Ah, dans ce cas, je ne vois pas comment ça pourrait mal tourner."
    
    jump load_desk_linux





label load_desk_linux:
    
    # ecran de bureau, fond 
    show screen desk_linux
    ""
    
    show screen telephone_sms
    
    scene node_155
    f "<player_pseudo>, je n'ai plus de doute sur tes capacités d'analyse."

    scene node_156
    f "Mais il reste une variable que je n'ai jamais pu mesurer."

    scene node_158
    f "Dans cette affaire, j'observerai tes décisions afin d'établir ton indice d'éthique."

    scene node_160
    f "Ce n'est ni un jugement ni une note."

    scene node_161
    f "Ton premier client s'appelle Jean Ranoud, sa fille a disparu."

    scene node_162
    f "Retrouve la, <player_pseudo>, je te mets en contact."
    
    
    
    
    
    
    
    
    
    
    
    scene node_1
    f "Allo ?"

    # --- Noeud 6 ---
    scene node_6
    f "C'est White Hat."
    menu:
        "Et vous, vous êtes le boomer en détresse ?":
            jump node_6_choice_0
        "Que puis-je pour vous?":
            jump node_6_choice_1


    # --- Noeud 17 ---
    scene node_17
    f "C'est une honte."
    menu:
        "Rassurez-vous monsieur, nous allons la retrouver.":
            jump node_17_choice_0
        "C'est terrible. Avez-vous reçu une demande de rançon ?":
            jump node_17_choice_1


    # --- Noeud 19 ---
    scene node_19
    f "Rassurez vous monsieur, nous allons la retrouver."

    # --- Noeud 20 ---
    scene node_20
    f "C'est terrible. Avez-vous reçu une demande de rançon ?"

    # --- Noeud 22 ---
    scene node_22
    f "Une rançon ? Non, rien, quelle idée."

    # --- Noeud 27 ---
    scene node_27
    f "Vous avez une idée de l'endroit où elle pourrait être ?"

    # --- Noeud 28 ---
    scene node_28
    f "Si je le savais, je ne paierais pas un hacker."

    # --- Noeud 29 ---
    scene node_29
    f "Ces derniers temps, elle était sur les nerfs. Quelqu'un lui a retourné le cerveau, c'est sûr."

    # --- Noeud 30 ---
    scene node_30
    f "Vous vous y connaissez..."
    menu:
        "Vous êtes hacker ?":
            jump node_30_choice_0
        "Un débutant ?":
            jump node_30_choice_1


    # --- Noeud 33 ---
    scene node_33
    f "J'ai trouvé un gars sur le darkweb qui m'a vendu une clé USB magique."

    # --- Noeud 34 ---
    scene node_34
    f "Ça a marché direct, j'ai aspiré tout le contenu du téléphone d'Alizée !"

    # --- Noeud 35 ---
    scene node_35
    f "Vous avez installé un logiciel inconnu acheté à un inconnu sur le téléphone de votre fille ?"

    # --- Noeud 36 ---
    scene node_36
    f "Évidemment ! C'est pas un inconnu d'ailleurs, je lui ai déjà acheté un système de caméras discrètes."

    # --- Noeud 37 ---
    scene node_37
    f "Par contre, le {color=#ffa500}téléphone est étonnamment vide{/color}, peu de sms, mail, ou images."

    # --- Noeud 38 ---
    scene node_38
    f "Et y'a un truc {color=#ffa500}crypté{/color} que j'ai pas réussi à lire."

    # --- Noeud 40 ---
    scene node_40
    f "Bref, à vous de jouer."

    # --- Noeud 41 ---
    scene node_41
    f "Envoyez-moi les données."

    # --- Noeud 44 ---
    scene node_44
    f "L'argent n'est pas un problème."

    # --- Noeud 46 ---
    scene node_46
    f "J'ai une bonne retraite. J'ai travaillé pour ça !"

    # --- Noeud 47 ---
    scene node_47
    # NOEUD VIDE (nodeId 47) : pas de texte dans le JSON source
    menu:
        "Ce sera 2 000 € en cas de succès uniquement.":
            jump node_47_choice_0
        "Vu la complexité et l'urgence, ce sera 4 000 € en cas de succès uniquement.":
            jump node_47_choice_1


    # --- Noeud 49 ---
    scene node_49
    f "Ça me va, mais dépêchez-vous."

    # --- Noeud 50 ---
    scene node_50
    f "Voilà l'archive."

    # --- Noeud 51 ---
    scene node_51
    f "Merci, je vous ferais un rapport complet dès que possible."

    # --- Noeud 90 ---
    scene node_90
    # NOEUD VIDE (nodeId 90) : pas de texte dans le JSON source

    # --- Noeud 91 ---
    scene node_91
    # NOEUD VIDE (nodeId 91) : pas de texte dans le JSON source

    # --- Noeud 96 ---
    scene node_96
    # NOEUD VIDE (nodeId 96) : pas de texte dans le JSON source

    # --- Noeud 98 ---
    scene node_98
    f "En revanche, vous savez que ce n’est pas gratuit ? Payable en crypto-monnaie."

    # --- Noeud 109 ---
    scene node_109
    f "J'ai désormais accès aux archives du téléphone d'Alyzée."

    # --- Noeud 110 ---
    scene node_110
    f "Je dois trouver pourquoi elle a disparu, si elle va bien, qui est au courant.. et à quel endroit elle se trouve."

    e "Vous venez de créer un nouveau jeu Ren'Py."

    e "Après avoir ajouté une histoire, des images et de la musique, vous pourrez le présenter au monde entier !"

    return