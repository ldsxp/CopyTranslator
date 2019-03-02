# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 0017 17:19
# @Author  : Elliott Zheng
# @Email   : admin@hypercube.top
# @FileName: config.py
# @Software: PyCharm

import json
import os
import threading
import webbrowser

import wx
from pynput import mouse

from constant import *
from copyTranslator.youdao import YoudaoSpider
from focusframe import FocusFrame
from googletranslator import GoogleTranslator
from mainframe import MainFrame
from myenum import *
from mypanel import MyPanel
from writingframe import WritingFrame


class Config:
    def __init__(self, setting):
        self.setting = setting
        self.mouseListener = mouse.Listener(on_click=self.setting.onLongClick)
        self._default_value = {'author': 'Elliott Zheng',
                               'version': version,
                               'is_listen': True,
                               'is_copy': False,
                               'is_dete': False,
                               'stay_top': False,
                               'continus': False,
                               'smart_dict': True,
                               'frame_mode': FrameMode.main,
                               'translator_type': TranslatorType.GOOGLE,
                               'font_size': 15,
                               'focus_x': 100,
                               'focus_y': 100,
                               'focus_height': 300,
                               'focus_width': 500,
                               'source': 'English',
                               'target': 'Chinese (Simplified)',
                               'last_ask': 0,
                               'language': 'Chinese (Simplified)',
                               'autohide': False,
                               'autoshow': False
                               }
        self.value = self._default_value
        self.state = MyPanel.NOT_LISTEN
        self.filepath = os.path.expanduser('~/copytranslator.json')
        self.translator = None
        self.youdao_dict = YoudaoSpider()
        self.Mode1 = FrameMode.focus
        self.Mode2 = FrameMode.writing

    def initialize(self):
        self.mainFrame = self.setting.mainFrame
        self.subFrame = self.setting.subFrame
        self.writingFrame = self.setting.writingFrame
        self.lang = self.setting.lang
        self.activate()
        self.subFrame.SetSize(self['focus_x'], self['focus_y'], self['focus_width'], self['focus_height'])

    def activate(self):
        self.continus = self.continus
        self.stay_top = self.stay_top
        self.is_listen = self.is_listen
        self.is_dete = self.is_dete
        self.is_copy = self.is_copy
        self.frame_mode = self.frame_mode
        self.is_dict = self.is_dict
        self.autoshow = self.autoshow
        self.autohide = self.autohide
        self.switch_translator()

    def detect(self, string):
        return self.translator.detect(string)

    def translate(self, string, src, dest):
        return self.translator.translate(string, src=src, dest=dest)

    @property
    def source(self):
        return self.value['source']

    @source.setter
    def source(self, value):
        self['source'] = value

    @property
    def target(self):
        return self.value['target']

    @target.setter
    def target(self, value):
        self['target'] = value

    def load(self):  # 只有版本相同才会被保留，因为配置文件在不同版本间变化很大。
        if not os.path.exists(self.filepath):
            FirstThread().start()
            self.save(self.filepath)
            return self
        myfile = open(self.filepath, 'r')
        value = json.load(myfile)
        myfile.close()
        if value['version'] == version:
            self.value = value
        else:
            FirstThread().start()
        self.save(self.filepath)
        return self

    def save(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        myfile = open(filepath, 'w')
        json.dump(self.value, myfile, indent=4)
        myfile.close()

    def switch_translator(self, type=TranslatorType.GOOGLE):
        if type == TranslatorType.GOOGLE:
            self.translator = GoogleTranslator()

    def RefreshState(self):
        if self.continus and self.is_listen and self.is_copy:
            self.state = MyPanel.INCERMENT_COPY
        elif self.continus and self.is_listen:
            self.state = MyPanel.INCERMENT_LISTEN
        elif self.is_listen and self.is_copy:
            self.state = MyPanel.LISTEN_COPY
        elif self.is_listen:
            self.state = MyPanel.LISTEN
        else:
            self.state = MyPanel.NOT_LISTEN
        self.subFrame.panel.SetState(self.state)

        return self.state

    def __getitem__(self, item):
        return self.value[item]

    def __setitem__(self, key, value):
        self.value[key] = value

    @property
    def is_listen(self):
        return self['is_listen']

    @is_listen.setter
    def is_listen(self, value):
        self['is_listen'] = value
        self.mainFrame.listenCheck.SetValue(value)
        self.subFrame.listenCheck.SetValue(value)
        if value:
            self.mainFrame.timer.Start(2000)  # 设定时间间隔为1000毫秒,并启动定时器
            self.mouseListener = mouse.Listener(on_click=self.setting.onLongClick)
            self.mouseListener.start()
        else:
            self.mainFrame.timer.Stop()
            self.mouseListener.stop()
        self.RefreshState()

    @property
    def is_copy(self):
        return self['is_copy']

    @is_copy.setter
    def is_copy(self, value):
        self['is_copy'] = value
        self.mainFrame.copyCheck.SetValue(value)
        self.subFrame.copyCheck.SetValue(value)
        self.RefreshState()

    @property
    def is_dete(self):
        return self['is_dete']

    @is_dete.setter
    def is_dete(self, value):
        self['is_dete'] = value
        self.mainFrame.detectCheck.SetValue(value)
        self.subFrame.detectCheck.SetValue(value)
        if value:
            self.stored_source = self.mainFrame.tochoice.GetString(self.mainFrame.fromchoice.GetSelection())
            self.mainFrame.fromchoice.Disable()
            self.mainFrame.fromlabel.SetLabel(self.lang("Detected Language"))
            self.subFrame.fromchoice.Disable()
            self.subFrame.fromlabel.SetLabel(self.lang("Detected Language"))
        else:
            self.mainFrame.fromchoice.SetSelection(self.mainFrame.fromchoice.FindString(self.setting.stored_source))
            self.mainFrame.fromchoice.Enable()
            self.mainFrame.fromlabel.SetLabel(self.lang("Source Language"))

            self.subFrame.fromchoice.SetSelection(self.subFrame.fromchoice.FindString(self.setting.stored_source))
            self.subFrame.fromchoice.Enable()
            self.subFrame.fromlabel.SetLabel(self.lang("Source Language"))

    @property
    def stay_top(self):
        return self['stay_top']

    @stay_top.setter
    def stay_top(self, value):
        self['stay_top'] = value
        self.mainFrame.topCheck.SetValue(value)
        self.subFrame.topCheck.SetValue(value)
        if value:
            self.subFrame.SetWindowStyle(wx.STAY_ON_TOP | FocusFrame.subStyle)
            self.mainFrame.SetWindowStyle(wx.STAY_ON_TOP | MainFrame.mainStyle)
            self.writingFrame.SetWindowStyle(wx.STAY_ON_TOP | WritingFrame.subStyle)
        else:
            self.subFrame.SetWindowStyle(FocusFrame.subStyle)
            self.mainFrame.SetWindowStyle(MainFrame.mainStyle)
            self.writingFrame.SetWindowStyle(WritingFrame.subStyle)

    @property
    def continus(self):
        return self['continus']

    @continus.setter
    def continus(self, value):
        self['continus'] = value
        self.mainFrame.continusCheck.SetValue(value)
        self.subFrame.continusCheck.SetValue(value)
        self.RefreshState()

    @property
    def font_size(self):
        return self['font_size']

    @font_size.setter
    def font_size(self, value):
        self['font_size'] = value

    @property
    def is_dict(self):
        return self['smart_dict']

    @is_dict.setter
    def is_dict(self, value):
        self['smart_dict'] = value
        self.mainFrame.dictCheck.SetValue(value)
        self.subFrame.dictCheck.SetValue(value)

    @property
    def translator_type(self):
        return self['translator_type']

    @translator_type.setter
    def translator_type(self, value):
        self['translator_type'] = value
        self.switch_translator(value)

    @property
    def frame_mode(self):
        return self['frame_mode']

    @frame_mode.setter
    def frame_mode(self, value):
        self['frame_mode'] = value
        if value == FrameMode.main:
            self.subFrame.Show(False)
            self.mainFrame.Show(True)
            self.writingFrame.Show(False)
            self.Mode1 = FrameMode.focus
            self.Mode2 = FrameMode.writing
        elif value == FrameMode.focus:
            self.subFrame.Show(True)
            self.mainFrame.Show(False)
            self.writingFrame.Show(False)
            self.Mode1 = FrameMode.main
            self.Mode2 = FrameMode.writing
        elif value == FrameMode.writing:
            self.subFrame.Show(False)
            self.mainFrame.Show(False)
            self.writingFrame.Show(True)
            self.Mode1 = FrameMode.main
            self.Mode2 = FrameMode.focus

    @property
    def autohide(self):
        return self.value['autohide']

    @autohide.setter
    def autohide(self, value):
        self.value['autohide'] = value
        self.setting.mainFrame.hideCheck.SetValue(value)

    @property
    def autoshow(self):
        return self.value['autoshow']

    @autoshow.setter
    def autoshow(self, value):
        self.value['autoshow'] = value
        self.setting.mainFrame.showCheck.SetValue(value)


class FirstThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        box = wx.MessageDialog(None,
                               'If you found it useful, please give me a star on GitHub or introduce to your friend.\n\n如果您感觉本软件对您有所帮助，请在项目Github上给个star或是介绍给您的朋友，谢谢。\n\n本软件免费开源，如果您是以付费的方式获得本软件，那么你应该是被骗了。[○･｀Д´･ ○]\n\n这是您首次使用，本软件功能非常丰富，需要查看使用指南才能完全发挥功能，前往软件官网查看？',
                               project_name + ' ' + version + ' by Elliott Zheng',
                               wx.YES_NO | wx.STAY_ON_TOP | wx.ICON_QUESTION)
        answer = box.ShowModal()
        if answer == wx.ID_YES:
            webbrowser.open(usage_url)
        box.Destroy()
