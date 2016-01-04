import urwid
from programs import Program

program = None
def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    body.append(urwid.Divider())
    button = urwid.Button("EXIT")
    urwid.connect_signal(button, 'click', exit_application)
    body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'Program chosen: ', choice, u'\n'])
    done = urwid.Button(u'Ok')
    back = urwid.Button(u'Back')
    urwid.connect_signal(done, 'click', start_program, choice)
    urwid.connect_signal(back, 'click', show_menu)
    mainMenu.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed'), 
        urwid.AttrMap(back, None, focus_map='reversed')]))

def start_program(button, choice):
    global program
    program = choice
    raise urwid.ExitMainLoop()

def exit_application(button):
    global program
    program = None
    raise urwid.ExitMainLoop()

def show_menu(button):
    mainMenu.original_widget = menu(u'Programs', Program.promotedPrograms.keys())
 
def choose():
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
    if program is None:
        exit()
    return program


mainMenu = urwid.Padding(menu(u'Programs', Program.promotedPrograms.keys()), left=2, right=2)
top = urwid.Overlay(mainMenu, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)