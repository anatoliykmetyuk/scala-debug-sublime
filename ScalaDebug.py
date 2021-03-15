import sublime
import sublime_plugin

class ScalaDebugCommand(sublime_plugin.TextCommand):
  def run(self, edit, snippet):
    target_snippet = sublime.load_settings("ScalaDebug.sublime-settings").get("snippets")[snippet]
    for r in self.view.sel():
      text = self.view.substr(r)
      self.view.replace(edit, r, target_snippet.format(text))
