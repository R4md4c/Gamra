'''
Created on Jun 10, 2010

@author: blaze
'''
import os
import wx
import Edit
from Edit import *

class ToolBar(wx.ToolBar):
    '''
    Window main toolbar, instansiate
    and add it, it'll load all tools
    and add them to himself then 
    handle all events to activate tools,deactivate
    and everything that is related to them.
    '''
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TB_HORIZONTAL | wx.NO_BORDER, name=wx.PanelNameStr):
        wx.ToolBar.__init__(self, parent, id, pos, size, style, name)
        
        self.height = 10
        
        #================================================
        #=========== loading all tools ==================
        #================================================
        #========== Making objects of Editing tools ===== 
        tempEditTools = []
        for tool in Edit.__all__:
            tempToolObject = eval(tool+'.'+tool+'()')
            eval( 'tempEditTools.append((tempToolObject.Priority, tempToolObject))' )
        
        #Sort the tempEditTools by descending order
        tempEditTools.sort(reverse = True)    
        
        editTools = []
        #Adding the object from the tuple extracted from tempEditTools
        for tool in tempEditTools:
            editTools.append(tool[1])
        
        #========== Making buttons of Editing tools =====
        for v in editTools:
            tool = self.AddRadioTool(-1,
                     bitmap = wx.Bitmap( os.path.normpath("data/icons/"+v.Icon)), 
                     shortHelp = v.Name,
                     longHelp = v.__doc__
                     )
            tool.ClientData = v
            self.Bind(wx.EVT_MENU, self.OnToolChange, tool)
            
        self.AddSeparator()

        self.Realize()
        #================================================
        # Note: we have to merge all tools lists to (self.Tools)
        #================================================
        self.Tools = []
        self.Tools.extend(editTools)
        self.Tools[0].Activate(self.Parent.Canvas)
        self.ActiveTool = self.Tools[0]
            
    def OnToolChange(self,event):
        
        #========= getting new tool
        toolbutton = self.FindById(event.Id)
        tool = toolbutton.ClientData
        
        #======== Activating and Deactivating
        self.ActiveTool.Deactivate()
        tool.Activate(self.Parent.Canvas)
        
        #======== Setting new Tool
        self.ActiveTool = tool
