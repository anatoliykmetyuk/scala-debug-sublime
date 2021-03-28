import sublime
import sublime_plugin

from .Pinpoint import init, pinpoint_settings
from .ABDebug import load_ab_debug_params

class ScalaDebugCommand(sublime_plugin.TextCommand):

  def determine_pinpoint_level(self):
    init(self.view.window().folders())
    ab_debug_params = load_ab_debug_params(self.view.window().folders())
    if ab_debug_params:
      return max([len(v['markers']) for v in ab_debug_params.values()])
    else:
      return len(pinpoint_settings()['markers'])

  def run(self, edit, snippet):
    target_snippet = sublime.load_settings("DottyDebug.sublime-settings").get("scala_debug")['snippets'][snippet]
    pinpoint_level = None

    if isinstance(target_snippet, str):
      if 'pinpoint.log' in target_snippet:
        pinpoint_level = self.determine_pinpoint_level()
      for r in self.view.sel():
        text = self.view.substr(r)
        self.view.replace(edit, r, target_snippet.format(
          sel = text, ppt_level = pinpoint_level))
    else:
      defined_vars = {}
      for i, r in enumerate(self.view.sel()):  # Collect all the selected regions into the dictionary
        text = self.view.substr(r)
        defined_vars[target_snippet['region_names'][i]] = text

      for vname, vvalue in target_snippet['variables'].items():  # Collect all the user-defined variables
        defined_vars[vname] = vvalue.format(**defined_vars)

      substitution_first, *substitution_tail = target_snippet['substitution']

      # Replace first selection with the first line on the substitution
      first_selection = self.view.sel()[0]
      indent = self.view.indentation_level(first_selection.begin())
      self.view.replace(edit, first_selection, substitution_first.format(**defined_vars))

      # Add the rest of the substitution below on separate lines
      current_line = self.view.line(first_selection.begin()).end()
      for l in substitution_tail:
        inserted = self.view.insert(edit, current_line, "\n" + (" " * indent * 2) + l.format(**defined_vars))
        current_line += inserted




