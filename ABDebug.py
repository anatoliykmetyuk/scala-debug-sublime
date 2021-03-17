import sublime
import sublime_plugin


class AbDebugTestFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    test_file = self.view.window().new_file(syntax = 'Packages/JavaScript/JSON.sublime-syntax')
    test_file.set_name('TestParams.abdebug')
    default_params = sublime.load_resource('Packages/DottyDebug/resources/DefaultDebugParams.abdebug')
    test_file.insert(edit, 0, default_params)
