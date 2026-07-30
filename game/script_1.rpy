    
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

    scene node_155

    ## Migration vers chat_window : tant que ce screen est affiché, tous les
    ## "say"/"menu:" ci-dessous s'affichent dans la fenêtre de discussion
    ## plutôt qu'en plein écran, sans changer une ligne de logique en dessous.
    show screen chat_window({
        "name": nomSupervisor,
        "statut": "En ligne",
    })

    h "[player_name], initialisation de la phase opérationnelle."
    h "On y est. "
    h "Aujourd'hui, je vais te confier ta première affaire."
    h "Nous avons suffisamment travaillé ensemble pour que je connaisse ta valeur."
    h "Tu fais partie des {a=indice:intro_anon_perseverant}rares{/a} profils qui ont tenu jusqu'au bout."
    menu:
        "Je suis génial !":
            t "C'est parce que je suis surpuissant !"
            h "Une conclusion audacieuse."
            h "Continue d'exploiter cette intelligence émotionnelle, elle sera précieuse."

        "J'ai eut un bon mentor":
            t "Probablement parce que j'ai eu un excellent mentor !"
            t "Flatteur, mais stratégique. Une hypothèse flatteuse."
            t "Veille simplement à ne pas surestimer tes résultats."

    "[player_name], je n'ai plus de doute sur tes capacités d'analyse. "
    h "Mais il reste une variable que je n'ai jamais pu mesurer. "
    h "Elle ne demande aucune compétence technique... et pourtant, elle fera toute la différence. "
    h "As-tu deviné de quoi je parle ?"

    menu:
        "Le charisme ?":
            t "Le charisme !"
            h "Une réponse inattendue. Intéressante, mais inexacte. "
        "L'éthique ?":
            t "L'éthique !"
            h "Exact. Tu as identifié la bonne variable. "
        "Je ne sais pas.":
            t "Je ne sais pas."
            h "Admettre une absence de données est le premier pas vers une analyse rigoureuse. C'est le début de la sagesse."

    h "Je parle de l'éthique, <player_pseudo>."
    h "Dans cette affaire, j'observerai tes décisions afin d'établir ton indice d'éthique. "
    h "Ce n'est ni un jugement ni une note. "
    h "Je cherche simplement à comprendre qui tu es lorsque personne ne te dit quoi faire. "
    h "Ton premier client s'appelle Jean Ranoud, sa fille a disparu."


    h "Retrouve la, [player_name], je te mets en contact."
    h "N'obéis pas. Comprends. Juge. Agis."

    hide screen chat_window

    jump mission1_sms_conversation


label mission1_sms_conversation:

    ## Conversation SMS de la mission 1. L'écran est modal : le récit
    ## principal reste en pause tant que le joueur n'a pas fermé le
    ## téléphone (bouton "Fermer" -> Hide("mission_sms")).

    window hide

    show screen mission_sms("json/mission1_dialogue_1 1.json")
    pause

    hide screen mission_sms

    scene node_1
    k "Allo ?"

    # --- Noeud 6 ---
    scene node_6
    k "C'est White Hat."
    menu:
        "Et vous, vous êtes le boomer en détresse ?":
            jump node_6_choice_0
        "Que puis-je pour vous?":
            jump node_6_choice_1


    # --- Noeud 17 ---
    scene node_17
    k "C'est une honte."
    menu:
        "Rassurez-vous monsieur, nous allons la retrouver.":
            jump node_17_choice_0
        "C'est terrible. Avez-vous reçu une demande de rançon ?":
            jump node_17_choice_1


    # --- Noeud 19 ---
    scene node_19
    k "Rassurez vous monsieur, nous allons la retrouver."

    # --- Noeud 20 ---
    scene node_20
    k "C'est terrible. Avez-vous reçu une demande de rançon ?"

    # --- Noeud 22 ---
    scene node_22
    k "Une rançon ? Non, rien, quelle idée."

    # --- Noeud 27 ---
    scene node_27
    k "Vous avez une idée de l'endroit où elle pourrait être ?"

    # --- Noeud 28 ---
    scene node_28
    k "Si je le savais, je ne paierais pas un hacker."

    # --- Noeud 29 ---
    scene node_29
    k "Ces derniers temps, elle était sur les nerfs. Quelqu'un lui a retourné le cerveau, c'est sûr."

    # --- Noeud 30 ---
    scene node_30
    k "Vous vous y connaissez..."
    menu:
        "Vous êtes hacker ?":
            jump node_30_choice_0
        "Un débutant ?":
            jump node_30_choice_1


    # --- Noeud 33 ---
    scene node_33
    k "J'ai trouvé un gars sur le darkweb qui m'a vendu une clé USB magique."

    # --- Noeud 34 ---
    scene node_34
    k "Ça a marché direct, j'ai aspiré tout le contenu du téléphone d'Alizée !"

    # --- Noeud 35 ---
    scene node_35
    k "Vous avez installé un logiciel inconnu acheté à un inconnu sur le téléphone de votre fille ?"

    # --- Noeud 36 ---
    scene node_36
    k "Évidemment ! C'est pas un inconnu d'ailleurs, je lui ai déjà acheté un système de caméras discrètes."

    # --- Noeud 37 ---
    scene node_37
    k "Par contre, le {color=#ffa500}téléphone est étonnamment vide{/color}, peu de sms, mail, ou images."

    # --- Noeud 38 ---
    scene node_38
    # k "Et y'a un truc {color=#ffa500}crypté{/color} que j'ai pas réussi à lire."

    # --- Noeud 40 ---
    scene node_40
    k "Bref, à vous de jouer."

    # --- Noeud 41 ---
    scene node_41
    k "Envoyez-moi les données."

    # --- Noeud 44 ---
    scene node_44
    k "L'argent n'est pas un problème."

    # --- Noeud 46 ---
    scene node_46
    k "J'ai une bonne retraite. J'ai travaillé pour ça !"

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
    k "Ça me va, mais dépêchez-vous."

    # --- Noeud 50 ---
    scene node_50
    k "Voilà l'archive."

    # --- Noeud 51 ---
    scene node_51
    k "Merci, je vous ferais un rapport complet dès que possible."

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
    k "En revanche, vous savez que ce n’est pas gratuit ? Payable en crypto-monnaie."

    # --- Noeud 109 ---
    scene node_109
    k "J'ai désormais accès aux archives du téléphone d'Alyzée."

    # --- Noeud 110 ---
    scene node_110
    k "Je dois trouver pourquoi elle a disparu, si elle va bien, qui est au courant.. et à quel endroit elle se trouve."

    e "Vous venez de créer un nouveau jeu Ren'Py."

    e "Après avoir ajouté une histoire, des images et de la musique, vous pourrez le présenter au monde entier !"

    return
    
    
    j "Allo ?"
    j "C'est vous le Taïe What ?"
    t "C'est White Hat."
    menu:    
        "Et vous, vous êtes le boomer en détresse ?":
            t "Et vous, vous êtes le boomer en détresse ?"
            j "Oh, un peu de respect. Je paye, j'ai le droit de me tromper de nom ! "
        "Que puis-je pour vous?":
            t "Que puis-je pour vous?"
            j "Bon... enfin quelqu'un qui va servir à quelque chose."
    
    j "Ma fille Alizée a disparu {a indice:alyzee_disparu_18}le jour de ses dix-huit ans.{/a}"
    j " Je lui avais préparé un gâteau."
    j "Deux jours plus tard, toujours rien ! Et la police refuse de bouger sous prétexte qu'elle est majeure."
    
    j "C'est une honte."
    
    menu:
        "Rassurez-vous monsieur, nous allons la retrouver.":
            t "Rassurez vous monsieur, nous allons la retrouver."
            j "J'espère bien."
        "C'est terrible. Avez-vous reçu une demande de rançon ?":
            t "C'est terrible. Avez-vous reçu une demande de rançon ?"
            j "Une rançon ? Non, rien, quelle idée."
            
    t "Vous avez une idée de l'endroit où elle pourrait être ?"
    j "Si je le savais, je ne paierais pas un hacker."
    j "Ces derniers temps, elle était sur les nerfs. Quelqu'un lui a retourné le cerveau, c'est sûr. "
    j "Elle contestait tout : les règles, les horaires, mes décisions... Je l'élève seul depuis 10 ans ! Je fais tout pour son bien. "
    j "Je sais que je ne suis pas parfait, mais qui l'est ? Enfin bref."
    j "J'ai déjà avancé sur l'enquête. Je suis un peu hacker moi-même. "
    
    j "Vous vous y connaissez..."
    menu: 
        "Vous êtes hacker ?":
            t "Vous êtes hacker ?"
        "Un débutant ?":
            t "Un débutant ?"
    
    j "J'ai trouvé un gars sur le darkweb qui m'a vendu une clé USB magique."
    j "Ça a marché direct, j'ai aspiré tout le contenu du téléphone d'Alizée ! "
    t "Vous avez installé un logiciel inconnu acheté à un inconnu sur le téléphone de votre fille ?"
    j "Évidemment ! C'est pas un inconnu d'ailleurs, je lui ai déjà acheté un système de caméras discrètes."
    
    menu:
        "C'est d'une imprudence totale.":
            "Ben quoi ? Ça a marché."
        "Il s'est passé quoi ensuite ?":
            "Merci. Mais j'attends une ristourne, vu que j'ai fait le plus gros. "
        "Impressionnant, vous êtes un vrai hacker !":
            ""
    
    j "Par contre, le {a indice:M1_phone_empty}téléphone est étonnamment vide{/a}, peu de sms, mail, ou images. "
    j "Et y'a un truc {a indice:M1_crypted}crypté{/a} que j'ai pas réussi à lire."
    j "Bref, à vous de jouer."
    
    
    t "Envoyez-moi les données. "
    
    t "En revanche, vous savez que ce n’est pas gratuit ? Payable en crypto-monnaie."
        
    j "L'argent n'est pas un problème."
    j " J'ai une bonne retraite. J'ai travaillé pour ça !"
    
    menu:
        "Ce sera 2 000 € en cas de succès uniquement.":
            j "Ça me va, mais dépêchez-vous."
        "Vu la complexité et l'urgence, ce sera 4 000 € en cas de succès uniquement.":
            j "C'est cher payé pour ouvrir un fichier, mais j'ai pas le choix. Dépêchez-vous. "
            
    j "Voilà l'archive."
    t "Merci, je vous ferais un rapport complet dès que possible."
    j "J'attend votre rapport !"
    
    # deconnnexion
    
    n "J'ai désormais accès aux archives du téléphone d'Alyzée."
    n "Je dois trouver pourquoi elle a disparu, si elle va bien, qui est au courant.. et à quel endroit elle se trouve."
    

    