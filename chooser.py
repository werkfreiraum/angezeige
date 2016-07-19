# -*- coding: utf-8 -*-
import urwid
import sys
from programs import Program

switch = None
switch_programs = None


def get_status():
    status = "Status: "
    if Program.running:
        e = Program.running.error()
        if e:
            status += "ERROR"
        else:
            status += "RUNNING"
        status += " (" + Program.running.__class__.__name__ + ") "
        if e:
            status += "\n" + str(e) + " (" + e.__class__.__name__ + ") "
    else:
        status += "OFF"

    if switch:
        status += "\nClap: "

        if switch.detected:
            status += "YES"
        else:
            status += "NO"

    return status

status = urwid.Text(get_status())


def menu(choices):
    body = [urwid.Divider("-"), urwid.Text("ANGEZEIGE", align='center'), urwid.Divider("-"),
            status, urwid.Divider("-"), urwid.Text("Choose Program:")]
    for choice in choices:
        button = urwid.Button(choice)
        urwid.connect_signal(button, 'click', item_chosen, user_args=[choice])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    body.append(urwid.Divider("-"))
    button = urwid.Button("EXIT")
    urwid.connect_signal(button, 'click', exit_application)
    body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def item_chosen(choice, button):
    body = [urwid.Divider("-"), urwid.Text(choice, align='center')]

    if len(Program.getPromotedPrograms()[choice].getParams()) > 0:
        body.extend([urwid.Divider("-"), urwid.Text("Parameters:")])

    params = {}
    for p, v in Program.getPromotedPrograms()[choice].getParams().items():
        # body.append(urwid.Text())
        edit = urwid.Edit(caption=u"▸ " + p.replace('_', ' ').title() + ": ", edit_text=v)
        body.append(urwid.AttrMap(edit, None, focus_map='reversed'))
        # body.append(urwid.Divider())
        params[p] = edit

    body.append(urwid.Divider("-"))

    ok = urwid.Button(u'Ok')
    back = urwid.Button(u'Back')

    urwid.connect_signal(ok, 'click', start_program, user_args=[choice, params])
    urwid.connect_signal(back, 'click', show_menu)

    tOk = urwid.AttrMap(ok, None, focus_map='reversed')

    body.append(tOk)
    body.append(urwid.AttrMap(back, None, focus_map='reversed'))

    mainWidget.original_widget = urwid.Filler(urwid.Pile(body, focus_item=tOk))


def start_program(choice, params, button=None, params_from_edit=True):
    cParams = {}
    if params_from_edit:
        for p in params:
            cParams[p] = params[p].get_edit_text()
    else:
        cParams = params

    if Program.running:
        Program.running.stop()
        Program.running.join()

    p = Program.getPromotedPrograms()[choice](**cParams)
    p.start()
    show_menu()


def exit_application(button=None):
    raise urwid.ExitMainLoop()


def show_menu(button=None):
    mainWidget.original_widget = listMenu


next_switch_program_idx = 0


def get_info(mainLoop, data):
    global next_switch_program_idx

    status.set_text(get_status())
    if switch and switch.detected:
        prog = switch_programs[next_switch_program_idx]
        name = prog["name"]
        params = prog["params"] if "params" in prog else {}
        start_program(name, params, None, False)
        next_switch_program_idx = (next_switch_program_idx + 1) % len(switch_programs)
        switch.detected = False
        # exit_application()
    mainLoop.set_alarm_in(0.2, get_info)


def choose(use_switch=None, use_switch_programs=None):

    top = urwid.Overlay(mainWidget, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                        align='center', width=('relative', 60),
                        valign='middle', height=('relative', 60),
                        min_width=20, min_height=9)
    show_menu()
    # start with first program
    if use_switch is not None:
        global switch, switch_programs
        switch = use_switch
        switch_programs = use_switch_programs
        switch.detected = True

    mainLoop = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
    mainLoop.set_alarm_in(0, get_info)
    mainLoop.run()


listMenu = menu(Program.getPromotedPrograms().keys())
mainWidget = urwid.Padding(None, left=1, right=1)
