# -*- coding: utf-8 -*-
import urwid
import logging
from manager.base import Manager


class UrwidManager(Manager):

    def __init__(self):
        self.status = urwid.Text(self.get_status())
        self.mainWidget = urwid.Padding(None, left=1, right=1)

    def get_status(self):
        info = Manager.get_status(self)
        status = "Status: " + info['program']['status']
        if info['program']['status'] != 'stopped':
            status += ' (' + info['program']['name'] + ") "
        if info['program']['status'] == 'error':
            status += '\n' + info['program']['error']['text'] + " (" + info['program']['error']['class'] + ") "

        status += "\nSwitch detected: " + ('YES' if info['switch'] else 'NO')

        return status

    def menu(self, choices):
        body = [urwid.Divider("-"), urwid.Text("ANGEZEIGE", align='center'), urwid.Divider("-"),
                self.status, urwid.Divider("-"), urwid.Text("Choose Program:")]
        for choice in choices:
            button = urwid.Button(choice)
            urwid.connect_signal(button, 'click', self.item_chosen, user_args=[choice])
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        env = self.get_environment()
        for proxy_name, proxy_items in env.iteritems():
            if len(proxy_items) > 0:
                body.extend([urwid.Divider("-"), urwid.Text(proxy_name + ":")])
                for item in proxy_items:
                    body.append(urwid.CheckBox(item['name'], state=item['enabled'],
                                               on_state_change=self.checkbox, user_data={"proxy": proxy_name, "name": item['name']}))

        body.append(urwid.Divider("-"))
        button = urwid.Button("EXIT")
        urwid.connect_signal(button, 'click', self.disable)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def checkbox(self, checkbox, state, user_data):
        self.set_environment(state=state, **user_data)

    def item_chosen(self, choice, button):
        body = [urwid.Divider("-"), urwid.Text(choice, align='center')]

        program_params = self.get_programs()[choice]

        if len(program_params) > 0:
            body.extend([urwid.Divider("-"), urwid.Text("Parameters:")])

        params = {}
        for p, v in program_params.items():
            # body.append(urwid.Text())
            edit = urwid.Edit(caption=u"▸ " + p.replace('_', ' ').title() + ": ", edit_text=v)
            body.append(urwid.AttrMap(edit, None, focus_map='reversed'))
            # body.append(urwid.Divider())
            params[p] = edit

        body.append(urwid.Divider("-"))

        ok = urwid.Button(u'Ok')
        back = urwid.Button(u'Back')

        urwid.connect_signal(ok, 'click', self.start_program, user_args=[choice, params])
        urwid.connect_signal(back, 'click', self.show_menu)

        tOk = urwid.AttrMap(ok, None, focus_map='reversed')

        body.append(tOk)
        body.append(urwid.AttrMap(back, None, focus_map='reversed'))

        self.mainWidget.original_widget = urwid.Filler(urwid.Pile(body, focus_item=tOk))

    def start_program(self, name, params, button=None, params_from_edit=True):
        cParams = {}
        for p in params:
            cParams[p] = params[p].get_edit_text()

        Manager.start_program(self, name=name, params=cParams)
        self.show_menu()

    def exit_application(self, button=None):
        raise urwid.ExitMainLoop()

    def show_menu(self, button=None):
        listMenu = self.menu(self.get_programs().keys())
        self.mainWidget.original_widget = listMenu

    def get_info(self, mainLoop, data):
        self.status.set_text(self.get_status())
        mainLoop.set_alarm_in(0.2, self.get_info)

    def enable(self):
        #self.thread = Thread(name="Urwid", target=self.start)
        # self.thread.start()
        self.start()

    def disable(self, *argv):
        raise urwid.ExitMainLoop()

    def start(self):
        top = urwid.Overlay(self.mainWidget, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                            align='center', width=('relative', 60),
                            valign='middle', height=('relative', 60),
                            min_width=20, min_height=9)

        self.show_menu()
        mainLoop = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
        mainLoop.set_alarm_in(0, self.get_info)
        mainLoop.run()
