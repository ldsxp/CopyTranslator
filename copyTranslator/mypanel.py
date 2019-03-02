# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 0025 18:01
# @Author  : Elliott Zheng
# @FileName: mypanel.py
# @Software: PyCharm

import wx


class MyPanel(wx.Panel):
    NOT_LISTEN = (255, 255, 255)
    LISTEN = (84, 255, 159)
    LISTEN_COPY = (152, 245, 255)
    TRANSLATEING = (238, 238, 0)
    INCERMENT_LISTEN = (147, 112, 219)
    INCERMENT_COPY = (199, 21, 133)

    def __init__(self, parent, setting=None):
        wx.Panel.__init__(self, parent, -1)
        self.leftDown = False
        self.parentFrame = parent
        self.setting = setting
        while self.parentFrame.GetParent() is not None:
            self.parentFrame = self.parentFrame.GetParent()
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        # self.Bind(wx.EVT_RIGHT_UP, self.parentFrame.setting.Copy)
        self.Bind(wx.EVT_RIGHT_DOWN, self.parentFrame.setting.ReverseListen)

    def OnLeftDClick(self, evt):
        # self.parentFrame.setting.ChangeMode(evt)
        # if self.setting.config.autohide:
        self.setting.AutoHide(False)
        # else:
        #     self.setting.get_current_frame().OnIconfiy(evt)

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        self.leftDown = True
        pos = self.ClientToScreen(evt.GetPosition())
        origin = self.parentFrame.GetPosition()
        dx = pos.x - origin.x
        dy = pos.y - origin.y
        self.delta = wx.Point(dx, dy)

    def OnLeftUp(self, evt):
        if not self.leftDown:
            return
        self.ReleaseMouse()
        self.leftDown = False

    def OnMouseMove(self, evt):
        if evt.Dragging() and self.leftDown:
            pos = self.ClientToScreen(evt.GetPosition())
            fp = (pos.x - self.delta.x, pos.y - self.delta.y)
            self.parentFrame.Move(fp)

    def SetState(self, state):
        self.SetBackgroundColour(state)
        self.Refresh()
