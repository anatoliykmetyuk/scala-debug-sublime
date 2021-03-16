import sublime
import sublime_plugin

from .Pinpoint import init, pinpoint_settings

class ScalaDebugCommand(sublime_plugin.TextCommand):
  def run(self, edit, snippet):
    target_snippet = sublime.load_settings("Default.sublime-settings").get("scala_debug")['snippets'][snippet]
    pinpoint_level = None

    if 'pinpoint.log' in target_snippet:
      init(self.view.window().folders())
      pinpoint_level = len(pinpoint_settings()['markers'])

    for r in self.view.sel():
      text = self.view.substr(r)
      self.view.replace(edit, r, target_snippet.format(
        sel = text, ppt_level = pinpoint_level))
