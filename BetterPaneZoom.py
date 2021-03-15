import sublime
import sublime_plugin


class BetterToggleZoomCommand(sublime_plugin.WindowCommand):
  full_layout = None

  def run(self):
    print(self.full_layout)
    if not self.is_zoomed():
      self.zoom()
    elif self.full_layout:
      self.unzoom()

  def is_zoomed(self):
    return self.window.layout()['cols'][1] > 0.9

  def zoom(self):
    self.full_layout = self.window.layout()
    new_layout = self.window.layout().copy()
    new_layout['cols'][1] = 0.97
    self.window.set_layout(new_layout)

  def unzoom(self):
    self.window.set_layout(self.full_layout)
