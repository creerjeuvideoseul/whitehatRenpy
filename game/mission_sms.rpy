################################################################################
## Module mission_sms
##
## Écran "téléphone SMS" empilé par-dessus le bureau (desk_linux) pour jouer les
## conversations de mission (JSON avec branchement, choix, pièces jointes...).
## Panneau fixe en bande verticale à droite de l'écran 
##
## show screen mission_sms("json/mission1_dialogue_1 1.json")
################################################################################

init python:

    import time as _mission_sms_time
    import re as _mission_sms_re
    import json

    ## Cache des JSON déjà parsés : {chemin: (data, id_index)}
    _mission_sms_cache = {}

    MISSION_SMS_DEFAULT_TYPING_DELAY = 0.6
    MISSION_SMS_DEFAULT_AUTO_ADVANCE_DELAY = 1.0

    ## Les balises du JSON sont écrites en chevrons (<color=..>, <i>) alors que
    ## Ren'Py attend des accolades ({color=..}, {i}). On convertit à l'affichage.
    _mission_sms_tag_re = _mission_sms_re.compile(r"<(/?[a-zA-Z0-9_]+(?:=[^<>]*)?)>")

    # gestion des tags Unity vs Renpy
    def mission_sms_tags(text):
        if not text:
            return ""
        return _mission_sms_tag_re.sub(lambda m: "{" + m.group(1) + "}", text)

    # Lecture du JSON et indexation des id pour le branchement
    def mission_sms_load(json_path):
        if json_path not in _mission_sms_cache:
            with renpy.file(json_path) as f:
                data = json.load(f)
            id_index = {}
            for i, entry in enumerate(data.get("conversation", [])):
                if "id" in entry and entry["id"] not in id_index:
                    ## Les id peuvent se répéter dans le JSON source ; les cibles
                    ## de branchement ("next") sont en pratique uniques, donc on
                    ## garde la première occurrence pour rester déterministe.
                    id_index[entry["id"]] = i
            _mission_sms_cache[json_path] = (data, id_index)
        return _mission_sms_cache[json_path]

    # Récupération de la portée du screen
    def mission_sms_scope():
        scr = renpy.get_screen("mission_sms")
        return scr.scope if scr is not None else None

    # Résolution de l'index de l'entrée suivante à afficher (branchements)
    def mission_sms_resolve_next(scope, entry, index):
        next_id = entry.get("next")
        if next_id:
            id_index = scope["mission_sms_id_index"]
            if next_id in id_index:
                return id_index[next_id]
        return index + 1

    # Gestion de l'apparition d'une entrée (typing) et de la suite (auto_next/auto_advance)
    def mission_sms_start_reveal(scope, index):
        """Programme l'apparition (après typing_delay) de l'entrée à index."""
        conv = scope["mission_sms_data"].get("conversation", [])
        scope["mission_sms_advance_at"] = None
        scope["mission_sms_pending_next"] = None
        if index is None or index >= len(conv):
            scope["mission_sms_typing"] = False
            scope["mission_sms_wait_click"] = False
            scope["mission_sms_reveal_at"] = None
            return
        entry = conv[index]
        scope["mission_sms_index"] = index
        scope["mission_sms_typing"] = True
        scope["mission_sms_wait_click"] = False
        delay = entry.get("typing_delay", MISSION_SMS_DEFAULT_TYPING_DELAY)
        scope["mission_sms_reveal_at"] = _mission_sms_time.time() + delay

    def mission_sms_reveal_now(scope):
        """Fait apparaître l'entrée en attente et programme la suite."""
        conv = scope["mission_sms_data"].get("conversation", [])
        index = scope["mission_sms_index"]
        if index >= len(conv):
            return
        entry = conv[index]
        scope["mission_sms_typing"] = False
        scope["mission_sms_reveal_at"] = None

        etype = entry.get("type", "text")

        if etype == "choice":
            scope["mission_sms_displayed"].append(entry)
            scope["mission_sms_waiting_choice"] = True
            return

        if etype == "finish":
            scope["mission_sms_displayed"].append(entry)
            scope["mission_sms_finished"] = True
            return

        scope["mission_sms_displayed"].append(entry)

        next_index = mission_sms_resolve_next(scope, entry, index)
        auto_next = entry.get("auto_next")
        auto_advance = entry.get("auto_advance")

        if isinstance(auto_next, (int, float)):
            scope["mission_sms_pending_next"] = next_index
            scope["mission_sms_advance_at"] = _mission_sms_time.time() + auto_next
        elif auto_advance:
            scope["mission_sms_pending_next"] = next_index
            scope["mission_sms_advance_at"] = _mission_sms_time.time() + MISSION_SMS_DEFAULT_AUTO_ADVANCE_DELAY
        else:
            scope["mission_sms_pending_next"] = next_index
            scope["mission_sms_wait_click"] = True

    def mission_sms_open(json_path):
        scope = mission_sms_scope()
        if scope is None:
            return
        data, id_index = mission_sms_load(json_path)
        scope["mission_sms_data"] = data
        scope["mission_sms_id_index"] = id_index
        scope["mission_sms_displayed"] = []
        scope["mission_sms_waiting_choice"] = False
        scope["mission_sms_finished"] = False
        mission_sms_start_reveal(scope, 0)
        renpy.restart_interaction()

    def mission_sms_on_timer(scope):
        """Appelé par le timer du screen à l'échéance programmée."""
        now = _mission_sms_time.time()
        if scope["mission_sms_typing"] and scope["mission_sms_reveal_at"] is not None:
            if now >= scope["mission_sms_reveal_at"]:
                mission_sms_reveal_now(scope)
        elif scope["mission_sms_advance_at"] is not None:
            if now >= scope["mission_sms_advance_at"]:
                next_index = scope.get("mission_sms_pending_next")
                mission_sms_start_reveal(scope, next_index)
        renpy.restart_interaction()

    def mission_sms_advance_click():
        scope = mission_sms_scope()
        if scope is None:
            return
        if scope["mission_sms_typing"] or scope["mission_sms_waiting_choice"] or scope["mission_sms_finished"]:
            return
        if not scope["mission_sms_wait_click"]:
            return
        next_index = scope.get("mission_sms_pending_next")
        scope["mission_sms_wait_click"] = False
        mission_sms_start_reveal(scope, next_index)
        renpy.restart_interaction()

    def mission_sms_eval_condition(expr):
        if not expr:
            return True
        try:
            return bool(eval(expr, store.__dict__))
        except Exception:
            return True

    def mission_sms_exec_consequence(expr):
        if not expr:
            return
        try:
            exec(expr, store.__dict__)
        except Exception:
            pass

    def mission_sms_choose(choice):
        scope = mission_sms_scope()
        if scope is None:
            return

        mission_sms_exec_consequence(choice.get("consequence"))

        scope["mission_sms_displayed"].append({
            "sender": "player",
            "type": "text",
            "content": choice.get("text", ""),
        })
        scope["mission_sms_waiting_choice"] = False

        id_index = scope["mission_sms_id_index"]
        next_index = id_index.get(choice.get("next"), scope["mission_sms_index"] + 1)
        mission_sms_start_reveal(scope, next_index)
        renpy.restart_interaction()

    def mission_sms_copy(key, value):
        copied_data[key] = value
        renpy.notify(_("Copié : %s") % value)


## Variable globale, réutilisable par d'autres écrans (navigateur, recherche...).
default copied_data = {}


################################################################################
## Écran principal
################################################################################

screen mission_sms(json_path):

    zorder 50
    modal True

    default mission_sms_data = {"conversation": []}
    default mission_sms_id_index = {}
    default mission_sms_index = 0
    default mission_sms_displayed = []
    default mission_sms_waiting_choice = False
    default mission_sms_finished = False
    default mission_sms_typing = False
    default mission_sms_wait_click = False
    default mission_sms_reveal_at = None
    default mission_sms_advance_at = None
    default mission_sms_pending_next = None

    on "show" action Function(mission_sms_open, json_path)

    ## Le téléphone est modal donc tous les clics du joueur lui reviennent de
    ## toute façon : on capte le clic gauche n'importe où pour faire avancer
    ## la conversation (au lieu de forcer un clic sur un petit bouton dédié).
    key "mouseup_1" action Function(mission_sms_advance_click)

    $ mission_sms_interlocutor = mission_sms_data.get("participants", {}).get("interlocutor", {})
    $ mission_sms_online = "en ligne" in mission_sms_interlocutor.get("statut", "").lower()

    frame:
        style "mission_sms_panel"
        xanchor 1.0
        xpos config.screen_width
        ypos 0
        ysize config.screen_height
        xsize 400

        ## "fixed" (et non "vbox") pour que le pied de page (choix / bandeau
        ## de fin / indicateur de clic) soit ancré en bas du panneau via
        ## yalign, indépendamment de la hauteur prise par le viewport
        ## au-dessus (un vbox seul poussait ce pied de page hors écran).
        fixed:
            xfill True
            yfill True

            vbox:
                xfill True
                yfill True

                ## En-tête fixe (ne défile pas)
                frame:
                    style "mission_sms_header"
                    xfill True

                    vbox:
                        xfill True
                        spacing 4

                        hbox:
                            xfill True

                            text mission_sms_interlocutor.get("name", "") style "mission_sms_header_name"

                            # Bouton de fermeture du téléphone
                            textbutton "×":
                                style "mission_sms_close_button"
                                xalign 1.0
                                action Hide("mission_sms")

                        hbox:
                            spacing 6
                            yalign 0.5

                            add Solid("#3ddc71" if mission_sms_online else "#777777") xsize 10 ysize 10 yalign 0.5

                            text (mission_sms_interlocutor.get("statut", "")) style "mission_sms_header_sub"

                        if mission_sms_interlocutor.get("contact"):
                            text ("Contact : " + mission_sms_interlocutor.get("contact")) style "mission_sms_header_sub"

                        if mission_sms_data.get("mission_info"):
                            text mission_sms_tags(mission_sms_data.get("mission_info")) style "mission_sms_header_sub"

                ## Bandeau de debug (visible seulement en mode développeur SDK).
                ## À retirer une fois le flux de la conversation stabilisé.
                if config.developer:
                    text (
                        "DEBUG idx=%r typing=%r wait_click=%r waiting_choice=%r finished=%r displayed=%d" % (
                            mission_sms_index,
                            mission_sms_typing,
                            mission_sms_wait_click,
                            mission_sms_waiting_choice,
                            mission_sms_finished,
                            len(mission_sms_displayed),
                        )
                    ):
                        style "mission_sms_header_sub"
                        size 12
                        color "#ff5555"

                ## Zone de conversation, défilante, auto-scroll vers le bas.
                viewport id ("mission_sms_vp_%d" % len(mission_sms_displayed)):
                    xfill True
                    yfill True
                    scrollbars "vertical"
                    mousewheel True
                    yinitial 1.0

                    vbox:
                        xfill True
                        spacing 10
                        xmaximum 400

                        for mission_sms_entry_i in mission_sms_displayed:
                            use mission_sms_bubble(mission_sms_entry_i)

                        if mission_sms_typing:
                            use mission_sms_typing_indicator

            ## Pied de page, superposé au viewport et toujours ancré en bas
            ## du panneau (choix / bandeau de fin / indicateur de clic sont
            ## mutuellement exclusifs, donc un seul de ces blocs s'affiche).
            if mission_sms_waiting_choice and mission_sms_displayed and mission_sms_displayed[-1].get("type") == "choice":
                $ mission_sms_choice_entry = mission_sms_displayed[-1]

                vbox:
                    style "mission_sms_choices"
                    xfill True
                    yalign 1.0

                    for mission_sms_choice_i in mission_sms_choice_entry.get("choices", []):
                        if mission_sms_eval_condition(mission_sms_choice_i.get("condition")):
                            textbutton mission_sms_tags(mission_sms_choice_i.get("text", "")):
                                style "mission_sms_choice_button"
                                action Function(mission_sms_choose, mission_sms_choice_i)

            elif mission_sms_finished and mission_sms_displayed:
                frame:
                    style "mission_sms_finish_banner"
                    xfill True
                    yalign 1.0

                    vbox:
                        spacing 10

                        text mission_sms_tags(mission_sms_displayed[-1].get("content", "")) style "mission_sms_finish_text"

                        textbutton _("Fermer"):
                            style "mission_sms_choice_button"
                            action Hide("mission_sms")

            elif mission_sms_wait_click:
                ## Indicateur visuel (non cliquable : le clic est capté
                ## n'importe où sur l'écran via "key mouseup_1" ci-dessus).
                frame:
                    style "mission_sms_advance_hint"
                    xfill True
                    yalign 1.0

                    hbox:
                        xalign 0.5
                        spacing 8
                        text _("Toucher pour continuer") style "mission_sms_advance_arrow"
                        text "▼" style "mission_sms_advance_arrow" at mission_sms_bounce

    ## Timer dynamique : reprogrammé à chaque interaction avec le délai exact
    ## restant jusqu'à la prochaine échéance (typing en cours ou auto-avance).
    $ mission_sms_now = _mission_sms_time.time()
    $ mission_sms_scope_ref = mission_sms_scope()

    if mission_sms_typing and mission_sms_reveal_at is not None:
        timer max(0.02, mission_sms_reveal_at - mission_sms_now) action Function(mission_sms_on_timer, mission_sms_scope_ref)
    elif mission_sms_advance_at is not None:
        timer max(0.02, mission_sms_advance_at - mission_sms_now) action Function(mission_sms_on_timer, mission_sms_scope_ref)


screen mission_sms_typing_indicator():

    hbox:
        xalign 0.0

        frame:
            style "mission_sms_bubble_interlocutor"

            text "…" style "mission_sms_bubble_text"


screen mission_sms_bubble(entry):

    $ mission_sms_b_type = entry.get("type", "text")
    $ mission_sms_b_sender = entry.get("sender", "")

    if mission_sms_b_type == "narratif":

        text ("{i}" + mission_sms_tags(entry.get("content", "")) + "{/i}"):
            style "mission_sms_narratif_text"
            xalign 0.5
            xfill True
            textalign 0.5

    elif mission_sms_b_type in ("choice", "finish"):

        ## Affichés séparément (boutons de choix / bandeau de fin), rien ici.
        null height 1

    else:

        $ mission_sms_is_player = (mission_sms_b_sender == "player")

        hbox:
            xfill True
            xalign (1.0 if mission_sms_is_player else 0.0)

            frame:
                style ("mission_sms_bubble_player" if mission_sms_is_player else "mission_sms_bubble_interlocutor")
                xmaximum 300

                vbox:
                    spacing 6

                    for mission_sms_att in (entry.get("attachments") or []):
                        if mission_sms_att.get("type") == "image":
                            button:
                                style "mission_sms_attachment_button"
                                action Show("mission_sms_attachment_zoom", path=mission_sms_att.get("path"))

                                add mission_sms_att.get("path"):
                                    xsize 150
                                    ysize 150
                                    fit "contain"

                            if mission_sms_att.get("caption"):
                                text mission_sms_att.get("caption") style "mission_sms_caption_text"

                    if entry.get("copydata"):
                        button:
                            style "mission_sms_copy_button"
                            action Function(
                                mission_sms_copy,
                                entry.get("copydataValue", entry.get("content", "")),
                                entry.get("copydataValue", entry.get("content", "")),
                            )

                            text mission_sms_tags(entry.get("content", "")) style "mission_sms_bubble_text"
                    else:
                        text mission_sms_tags(entry.get("content", "")) style "mission_sms_bubble_text"


screen mission_sms_attachment_zoom(path):

    zorder 100
    modal True

    button:
        xfill True
        yfill True
        background Solid("#000000CC")
        action Hide("mission_sms_attachment_zoom")

    add path:
        xalign 0.5
        yalign 0.5
        xsize int(config.screen_width * 0.8)
        ysize int(config.screen_height * 0.8)
        fit "contain"


################################################################################
## Styles
################################################################################

style mission_sms_panel:
    background Solid("#161616E6")
    padding (0, 0)

style mission_sms_header:
    background Solid("#0d0d0dF2")
    padding (16, 12)

style mission_sms_header_name is desk_text:
    size 40

style mission_sms_header_sub is desk_text:
    size 20
    color "#9a9a9a"

style mission_sms_close_button:
    background None
    padding (8, 0)

style mission_sms_close_button_text is desk_text:
    size 30

style mission_sms_bubble_player:
    background Solid("#2b6cb0")
    padding (12, 8)
    left_margin 40
    right_margin 8

style mission_sms_bubble_interlocutor:
    background Solid("#2a2a2a")
    padding (12, 8)
    left_margin 8
    right_margin 40

style mission_sms_bubble_text is desk_text

style mission_sms_narratif_text is desk_text:
    color "#777777"
    size 25

style mission_sms_caption_text is desk_text:
    size 25
    color "#999999"

style mission_sms_attachment_button:
    background None
    padding (0, 0)

style mission_sms_choices:
    spacing 6
    padding (10, 10)
    background Solid("#0d0d0dF2")

style mission_sms_choice_button:
    background Solid("#1f1f1f")
    padding (10, 8)
    xfill True

style mission_sms_choice_button_text is desk_text

style mission_sms_copy_button:
    background None
    padding (0, 0)

style mission_sms_finish_banner:
    background Solid("#0d0d0dF2")
    padding (16, 16)

style mission_sms_finish_text is desk_text

style mission_sms_advance_hint:
    background Solid("#1f1f1fF2")
    ysize 46
    padding (0, 4)

style mission_sms_advance_arrow is desk_text:
    xalign 0.5
    size 17
    color "#cfcfcf"

transform mission_sms_bounce:
    ypos 0
    linear 0.4 ypos 6
    linear 0.4 ypos 0
    repeat
