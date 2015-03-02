# -*- coding: utf-8 -*-
import widgetUtils
import config
import wx_ui
import constants

class KeystrokeEditor(object):
 def __init__(self):
  super(KeystrokeEditor, self).__init__()
  self.changed = False # Change it if the keyboard shorcuts are reassigned.
  self.dialog = wx_ui.keystrokeEditorDialog()
  self.map = config.app["keymap"]
  # we need to  copy the keymap before modify it, for unregistering the old keystrokes if is needed.
  self.hold_map = self.map.copy()
  self.dialog.put_keystrokes(constants.actions, self.map)
  widgetUtils.connect_event(self.dialog.edit, widgetUtils.BUTTON_PRESSED, self.edit_keystroke)
  self.dialog.get_response()

 def edit_keystroke(self, *args, **kwargs):
  action = self.dialog.actions[self.dialog.get_action()]
  edit_dialog = wx_ui.editKeystrokeDialog()
  self.set_keystroke(self.map[action], edit_dialog)
  answer = edit_dialog.get_response()
  if answer == widgetUtils.OK:
   new_keystroke = self.get_edited_keystroke(edit_dialog)
   print new_keystroke
   if new_keystroke != self.map[action]:
    self.changed = True
    print "changed"
    self.map[action] = new_keystroke

 def set_keystroke(self, keystroke, dialog):
  for i in keystroke.split("+"):
   if hasattr(dialog, i):
    dialog.set(i, True)
  dialog.set("key", keystroke.split("+")[-1])

 def get_edited_keystroke(self, dialog):
  keys = []
  if dialog.get("win") == False:
   wx_ui.no_win_message()
   return
  if dialog.get("control") == True:
   keys.append("control")
#  if dialog.get("win") == True:
  keys.append("win")
  if dialog.get("alt") == True:
   keys.append("alt")
  if dialog.get("shift") == True:
   keys.append("shift")
  if dialog.get("key") != "":
   keys.append(dialog.get("key"))
  else:
   wx_ui.no_key()
   return
  return "+".join(keys)