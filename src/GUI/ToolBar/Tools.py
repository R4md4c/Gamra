'''
Created on Jun 5, 2010

@author: blaze
'''
import wx
import Document
import cairo

class Tool():
    '''
    the parent of all tools here
    '''
    def __init__(self, name='tool', icon='tool.png'):
        self.Name = name
        self.Icon = icon
            
    def Activate(self,canvas):
        self.Canvas = canvas
        self.Canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Canvas.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseMiddleDown)
        self.Canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        
        self.Canvas.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Canvas.Bind(wx.EVT_MIDDLE_UP, self.OnMouseMiddleUp)
        self.Canvas.Bind(wx.EVT_RIGHT_UP, self.OnMouseRightUp)
        
        self.Canvas.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Canvas.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Canvas.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        
        self.Canvas.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)
        self.Canvas.Bind(wx.EVT_PAINT, self.OnPaint)
        
    
    def Deactivate(self):
        self.Canvas.Unbind(wx.EVT_LEFT_DOWN)
        self.Canvas.Unbind(wx.EVT_MIDDLE_DOWN)
        self.Canvas.Unbind(wx.EVT_RIGHT_DOWN)
        
        self.Canvas.Unbind(wx.EVT_LEFT_UP)
        self.Canvas.Unbind(wx.EVT_MIDDLE_UP)
        self.Canvas.Unbind(wx.EVT_RIGHT_UP)
        
        self.Canvas.Unbind(wx.EVT_MOTION)
        self.Canvas.Unbind(wx.EVT_KEY_DOWN)
        self.Canvas.Unbind(wx.EVT_KEY_UP)
        
        self.Canvas.Unbind(wx.EVT_MOUSEWHEEL)
        self.Canvas.Unbind(wx.EVT_PAINT)
    
    def OnMouseLeftDown(self,event): 
        
        selected = self.Canvas.Document.GetUnderPixel(self.Canvas.Document.Mouse)
        # check if there is something selected
        if( selected!=None ):
            
            # check if shift is down, that will add,remove element from selection
            if event.ShiftDown() :
                if( selected in self.Canvas.Document.SelectedObjects ):
                    self.Canvas.Document.SelectedObjects.remove(selected)
                else:
                    self.Canvas.Document.SelectedObjects.append(selected)
                    
            #if shift is not down, the selection will be only the object
            else:
                self.Canvas.Document.SelectedObjects = [selected]
                
            # create the highlight rectangle around selected objects 
            highlight = self.Canvas.Document.GetRect(self.Canvas.Document.SelectedObjects)
            highlight.Stroke.Dash = [5,5]
            highlight.Fill.Color = (0,0,0,0)
            highlight.Antialiase = cairo.ANTIALIAS_NONE
            self.Canvas.Document.ToolObjects = [highlight]
            
        # if nothing clicked then clear the toolobjects and the selected objects
        else:
            self.Canvas.Document.ToolObjects = []
            self.SelectedObjects = []
            
        # after all reftesh the canvas
        self.Canvas.Refresh()
        event.Skip()
    
    def OnMouseMiddleDown(self,event): 
        self.StartPoint = self.Canvas.Document.Mouse
        event.Skip()
        
    def OnMouseRightDown(self,event): event.Skip()
    
    def OnMouseLeftUp(self,event): event.Skip()
    
    def OnMouseMiddleUp(self,event): event.Skip()
        
    def OnMouseRightUp(self,event): event.Skip()
    
    def OnMouseMove(self,event): 
        
        self.Canvas.Document.SetMouse(event.Position)
        
        if(event.Dragging() and event.MiddleIsDown() ):
            newpoint = self.Canvas.Document.Mouse
            zoom = self.Canvas.Document.Zoom
            self.Canvas.Document.Clip[0] -= int((newpoint[0]-self.StartPoint[0])*zoom)
            self.Canvas.Document.Clip[1] -= int((newpoint[1]-self.StartPoint[1])*zoom)
            self.Canvas.Refresh()
                
        wx.GetApp().Frame.SetStatusText(
                        'Current Position:'+str(self.Canvas.Document.Mouse)+
                        ', Zoom : '+str(self.Canvas.Document.Zoom*100)+'%'+
                        ', Clipping :'+str(self.Canvas.Document.Clip)
                        )
        event.Skip()
    
    def OnKeyDown(self,event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_TAB:
            
            #check the visibility of the panel..
            if wx.GetApp().Frame.Properties.IsShown(): 
                wx.GetApp().Frame.Properties.Hide()
            else:
                wx.GetApp().Frame.Properties.Show()
                wx.GetApp().Frame.FitInside()
                
                
    def OnKeyUp(self,event): event.Skip()
    
    def OnWheel(self,event):
        if(event.GetWheelRotation()>0):
            self.Canvas.Document.Zoom = round(self.Canvas.Document.Zoom*1.1,2)
        else:
            self.Canvas.Document.Zoom = round(self.Canvas.Document.Zoom/1.1,2)          
        
        self.Canvas.Refresh()
        
        event.Skip()
        
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self.Canvas)
        dc.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)))
        dc.Clear()
        self.Canvas.Document.Render(dc)
    
class EditingTool(Tool):
    '''
    Object editing tool parent like
    moving, rotating, scale, skew, shear...etc
    '''
    pass
    
class VectorTool(Tool):
    '''
    vector adding, editing, drawing like
    pen tool, biezer curves, lines, 
    circle, rectangle, stars...etc
    '''
    pass
        
class BitmapTool(Tool):
    '''
    bitmap editing tools like:
    rectangle, circle selections, burn, dodge
    '''
    pass
    
        