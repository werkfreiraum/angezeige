import urwid, sys
from programs import Program


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
    body = [urwid.Text("CHOOSE PROGRAM\n=============="), status, urwid.Divider()]
    for choice in choices:
        button = urwid.Button(choice)
        urwid.connect_signal(button, 'click', item_chosen, user_args = [choice])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    body.append(urwid.Divider())
    button = urwid.Button("EXIT")
    urwid.connect_signal(button, 'click', exit_application)
    body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def item_chosen(choice, button):
    body = [urwid.Text([u'Program chosen: ', choice, u'\n'])]

    params = {}
    for p, v in Program.getPromotedPrograms()[choice].getParams().items():
        body.append(urwid.Text("- " + p.title() + ":"))
        edit = urwid.Edit(caption = "  ", edit_text = v)
        body.append(urwid.AttrMap(edit, None, focus_map='reversed'))
        body.append(urwid.Divider())
        params[p] = edit

    ok = urwid.Button(u'Ok')
    back = urwid.Button(u'Back')
    
    urwid.connect_signal(ok, 'click', start_program, user_args = [choice, params])
    urwid.connect_signal(back, 'click', show_menu)
    
    tOk = urwid.AttrMap(ok, None, focus_map='reversed')
    
    body.append(tOk)
    body.append(urwid.AttrMap(back, None, focus_map='reversed'))

    mainMenu.original_widget = urwid.Filler(urwid.Pile(body, focus_item=tOk))

def start_program(choice, params, button):
    cParams = {}
    for p in params:
        cParams[p] = params[p].get_edit_text()

    if Program.running:
        Program.running.stop()
        Program.running.join()

    p = Program.getPromotedPrograms()[choice](**cParams)
    p.start()
    show_menu()

def exit_application(button):
    raise urwid.ExitMainLoop()

def show_menu(button = None):
    mainMenu.original_widget = menuWidget
 
def get_info(mainLoop, data):
    status.set_text(get_status())
    mainLoop.set_alarm_in(1, get_info)

def choose():
    mainLoop = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
    mainLoop.set_alarm_in(1, get_info)
    mainLoop.run()

menuWidget = menu(Program.promotedPrograms.keys())

mainMenu = urwid.Padding(menuWidget, left=2, right=2)
top = urwid.Overlay(mainMenu, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)