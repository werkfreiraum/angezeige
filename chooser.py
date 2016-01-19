# -*- coding: utf-8 -*-
import urwid, sys
from programs import Program, program_registry


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

    return status

status = urwid.Text(get_status())

def menu(choices):
    body = [urwid.Divider("-"), urwid.Text("ANGEZEIGE", align='center'), urwid.Divider("-"), status, urwid.Divider("-"), urwid.Text("Choose Program:")]
    for choice in choices:
        button = urwid.Button(choice)
        urwid.connect_signal(button, 'click', item_chosen, user_args = [choice])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    body.append(urwid.Divider("-"))
    button = urwid.Button("EXIT")
    urwid.connect_signal(button, 'click', exit_application)
    body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(choice, button):
    body = [urwid.Divider("-"), urwid.Text(choice, align='center')]

    if len(program_registry[choice].getParams()) > 0:
        body.extend([urwid.Divider("-"), urwid.Text("Parameters:")])

    params = {}
    for p, v in program_registry[choice].getParams().items():
        #body.append(urwid.Text())
        edit = urwid.Edit(caption = u"▸ " + p.replace('_', ' ').title() + ": ", edit_text = v)
        body.append(urwid.AttrMap(edit, None, focus_map='reversed'))
        #body.append(urwid.Divider())
        params[p] = edit

    body.append(urwid.Divider("-"))

    ok = urwid.Button(u'Ok')
    back = urwid.Button(u'Back')

    urwid.connect_signal(ok, 'click', start_program, user_args = [choice, params])
    urwid.connect_signal(back, 'click', show_menu)

    tOk = urwid.AttrMap(ok, None, focus_map='reversed')

    body.append(tOk)
    body.append(urwid.AttrMap(back, None, focus_map='reversed'))

    mainWidget.original_widget = urwid.Filler(urwid.Pile(body, focus_item=tOk))

def start_program(choice, params, button):
    cParams = {}
    for p in params:
        cParams[p] = params[p].get_edit_text()

    if Program.running:
        Program.running.stop()
        Program.running.join()

    p = program_registry[choice](**cParams)
    p.start()
    show_menu()

def exit_application(button):
    raise urwid.ExitMainLoop()

def show_menu(button = None):
    mainWidget.original_widget = listMenu

def get_info(mainLoop, data):
    status.set_text(get_status())
    mainLoop.set_alarm_in(1, get_info)

def choose():
    top = urwid.Overlay(mainWidget, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 60),
        valign='middle', height=('relative', 60),
        min_width=20, min_height=9)
    show_menu()
    mainLoop = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
    mainLoop.set_alarm_in(0, get_info)
    mainLoop.run()


listMenu = menu(program_registry.keys())
mainWidget = urwid.Padding(None, left=1, right=1)
