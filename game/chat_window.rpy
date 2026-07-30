################################################################################
## Module chat_window
##
## Fenêtre de discussion "en direct" centrée à l'écran, par-dessus le bureau.
##
## Contrairement à mission_sms (lecture d'archives JSON, en lecture seule),
## chat_window est piloté directement par les statements Ren'Py standards
## (`say` et `menu:`) : tant que ce screen est affiché, screens.rpy redirige
## l'affichage du dialogue et des choix vers cette fenêtre au lieu du
## textbox / menu plein écran habituel. Aucune logique de label à réécrire.
##
## Utilisation minimale :
##
##     show screen chat_window(chat_contact_henri)
##
##     h "Salut."
##     menu:
##         "Salut !":
##             "Salut !"
##
##     hide screen chat_window
################################################################################

init python:

    import time as _chat_time

    ## Délai avant qu'un message d'un contact (pas le joueur) ne se révèle,
    ## le temps d'afficher l'indicateur "en train d'écrire...".
    CHAT_TYPING_DELAY = 0.2

    def chat_get_scope():
        scr = renpy.get_screen("chat_window")
        return scr.scope if scr is not None else None

    def chat_is_open():
        return renpy.get_screen("chat_window") is not None

    def chat_say_revealed():
        """True si le dernier message ajouté au fil est déjà révélé (fin de
        l'indicateur "en train d'écrire..."), utilisé pour ne débloquer le
        clic de passage à la réplique suivante qu'une fois le texte visible.

        Utilise .get()/.setdefault() plutôt que scope["chat_messages"] :
        au tout premier rendu (show screen chat_window suivi immédiatement
        d'un say dans le même passage), le screen chat_window peut ne pas
        avoir encore exécuté ses "default" quand ce code s'exécute depuis
        le screen say — la clé n'existe alors pas encore dans le scope.
        """
        scope = chat_get_scope()
        if scope is None:
            return True
        messages = scope.get("chat_messages")
        if not messages:
            return True
        return messages[-1]["revealed"]

    def chat_is_player_line(who):
        """Le joueur (personnage "t" = DynamicCharacter("player_name")) est
        identifié en comparant who au pseudo courant, pas juste who is None
        (qui ne concerne que le narrateur sans personnage)."""
        if who is None:
            return False
        return who == getattr(renpy.store, "player_name", None)

    def chat_append_message(who, what):
        """Ajoute un message au fil de discussion.

        Si le message vient d'un contact (pas le joueur), il est d'abord
        masqué derrière un indicateur "en train d'écrire..." puis révélé
        après un court délai. S'il vient du joueur, il est affiché
        immédiatement.
        """
        scope = chat_get_scope()
        if scope is None:
            return
        messages = scope.setdefault("chat_messages", [])

        ## Idempotent : Ren'Py peut redéclencher "on show" (prédiction
        ## d'écran, redraw) pour la même réplique. Sans ce garde-fou, la
        ## même ligne était ajoutée deux fois (un doublon "en train
        ## d'écrire..." qui ne se révélait jamais, bloquant l'avancement).
        if messages and messages[-1]["who"] == who and messages[-1]["text"] == what:
            return

        is_player = chat_is_player_line(who)
        entry = {
            "is_player": is_player,
            "who": who,
            "text": what,
            "revealed": is_player,
        }
        messages.append(entry)
        if is_player:
            scope["chat_pending_entry"] = None
            scope["chat_reveal_at"] = None
        else:
            scope["chat_pending_entry"] = entry
            scope["chat_reveal_at"] = _chat_time.time() + CHAT_TYPING_DELAY
        renpy.restart_interaction()

    def chat_reveal_pending(scope):
        if scope is None:
            return
        entry = scope.get("chat_pending_entry")
        if entry is not None:
            entry["revealed"] = True
        scope["chat_pending_entry"] = None
        scope["chat_reveal_at"] = None
        renpy.restart_interaction()

    def chat_set_pending_choice(items):
        scope = chat_get_scope()
        if scope is None:
            return
        scope["chat_pending_choice"] = items
        renpy.restart_interaction()

    def chat_clear_pending_choice():
        scope = chat_get_scope()
        if scope is None:
            return
        scope["chat_pending_choice"] = None


################################################################################
## Écran principal
################################################################################

screen chat_window(contact):

    zorder 40
    modal True

    default chat_messages = []
    default chat_reveal_at = None
    default chat_pending_entry = None
    default chat_pending_choice = None

    ## chat_window est modal, donc le clic pour faire avancer un "say" ne
    ## peut jamais atteindre le mécanisme de dismiss intégré de Ren'Py (qui
    ## ne s'applique qu'aux écrans/au jeu SOUS ce screen modal). On le
    ## reproduit ici explicitement : cliquer termine l'interaction en cours
    ## (Return() = dismiss), mais seulement si le message affiché est déjà
    ## révélé (pas en pleine frappe) et qu'aucun choix n'est en attente
    ## (sinon on interromprait le menu au lieu du dialogue).
    key "mouseup_1" action (Return() if (chat_say_revealed() and not chat_pending_choice) else None)

    drag:
        ## Fenêtre déplaçable : seule la barre de titre (les ~50 premiers
        ## pixels en haut, ~7% de la hauteur) sert de poignée de glisser,
        ## le reste (bulles, boutons) reste cliquable normalement.
        drag_name "chat_window_drag"
        draggable True
        droppable False
        drag_handle (0.0, 0.0, 1.0, 0.07)
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 760

        frame:
            ## Liseré vert façon terminal autour de toute la fenêtre.
            background Solid("#66cc00")
            padding (2, 2)
            xfill True
            yfill True

            frame:
                style "chat_panel"
                xfill True
                yfill True

                fixed:
                    xfill True
                    yfill True

                    vbox:
                        xfill True
                        yfill True

                        frame:
                            style "chat_titlebar"
                            xfill True

                            hbox:
                                xfill True

                                text contact.get("name", "") style "chat_titlebar_text"

                                textbutton "×":
                                    style "chat_close_button"
                                    xalign 1.0
                                    action Hide("chat_window")

                        ## En-tête contact (nom, statut, contact, IP, localisation, logiciel)
                        frame:
                            style "chat_header"
                            xfill True

                            vbox:
                                xfill True
                                spacing 4

                                hbox:
                                    spacing 6
                                    yalign 0.5

                                    $ chat_online = "en ligne" in contact.get("statut", "").lower()
                                    add Solid("#66cc00" if chat_online else "#777777") xsize 10 ysize 10 yalign 0.5

                                    text (contact.get("statut", "")) style "chat_header_sub"

                                if contact.get("contact"):
                                    text ("Contact : " + contact.get("contact")) style "chat_header_sub"

                                if contact.get("ip"):
                                    text ("IP : " + contact.get("ip")) style "chat_header_sub"

                                if contact.get("localisation"):
                                    text ("Loc : " + contact.get("localisation")) style "chat_header_sub"

                                if contact.get("logiciel"):
                                    text ("Logiciel : " + contact.get("logiciel")) style "chat_header_sub"

                        ## Historique de messages, défilant, auto-scroll vers le bas.
                        viewport id ("chat_vp_%d" % len(chat_messages)):
                            xfill True
                            yfill True
                            scrollbars "vertical"
                            mousewheel True
                            yinitial 1.0

                            vbox:
                                xfill True
                                spacing 10
                                xmaximum 860

                                for chat_msg in chat_messages:
                                    if chat_msg["revealed"]:
                                        use chat_bubble(chat_msg)
                                    else:
                                        use chat_typing_bubble

                    ## Pied de page (choix du joueur), superposé et ancré en bas.
                    if chat_pending_choice:
                        vbox:
                            style "chat_choices"
                            xfill True
                            yalign 1.0

                            for chat_item in chat_pending_choice:
                                textbutton chat_item.caption:
                                    style "chat_choice_button"
                                    action [
                                        Function(chat_append_message, player_name, chat_item.caption),
                                        Function(chat_clear_pending_choice),
                                        chat_item.action,
                                    ]

    ## Timer de révélation du message en cours de "frappe".
    $ chat_now = _chat_time.time()
    $ chat_scope_ref = chat_get_scope()

    if chat_reveal_at is not None:
        timer max(0.02, chat_reveal_at - chat_now) action Function(chat_reveal_pending, chat_scope_ref)


screen chat_bubble(msg):

    hbox:
        xfill True
        xalign (1.0 if msg["is_player"] else 0.0)

        frame:
            style ("chat_bubble_player" if msg["is_player"] else "chat_bubble_contact")
            xmaximum 620

            text msg["text"] style "chat_bubble_text"


screen chat_typing_bubble():

    hbox:
        xalign 0.0

        frame:
            style "chat_bubble_contact"

            text "…" style "chat_bubble_text"


################################################################################
## Styles
################################################################################

style chat_panel:
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)
    padding (0, 0)

style chat_titlebar:
    background Solid("#0d0d0dF2")
    padding (16, 10)

style chat_titlebar_text is desk_text:
    size 22

style chat_close_button:
    background None
    padding (8, 0)

style chat_close_button_text is desk_text:
    size 24

style chat_header:
    background Solid("#161616F2")
    padding (16, 10)

style chat_header_sub is desk_text:
    size 16
    color "#9a9a9a"

style chat_bubble_player:
    background Solid("#2b6cb0")
    padding (12, 8)
    left_margin 60
    right_margin 8

style chat_bubble_contact:
    background Solid("#2a2a2a")
    padding (12, 8)
    left_margin 8
    right_margin 60

style chat_bubble_text is desk_text

style chat_choices:
    spacing 6
    padding (10, 10)
    background Solid("#0d0d0dF2")

style chat_choice_button:
    background Solid("#1f1f1f")
    padding (10, 8)
    xfill True

style chat_choice_button_text is desk_text
