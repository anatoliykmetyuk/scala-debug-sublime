import sublime, sublime_plugin
import os, json


class AbDebugCreateParamsFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    test_file = self.view.window().new_file(syntax = 'Packages/JavaScript/JSON.sublime-syntax')
    test_file.set_name('TestParams.abdebug')
    default_params = sublime.load_resource('Packages/DottyDebug/resources/DefaultDebugParams.abdebug')
    test_file.insert(edit, 0, default_params)

class AbDebugCommand(sublime_plugin.WindowCommand):
  def find_test_params_view(self):
    for view in self.window.views():
      if view.file_name():
        if os.path.splitext(view.file_name())[1] == '.abdebug':
          return view

  def run(self, test = None):
    params_view = self.find_test_params_view()
    params_raw = params_view.substr(sublime.Region(0, params_view.size()))
    params = json.loads(params_raw)

    def execute(target_test):
      target_test_params = params[target_test]
      self.window.run_command('pinpoint_set',
        { 'markers': target_test_params['markers'] })
      self.window.run_command('terminus_send_string',
        { 'string': target_test_params['command'] + '\n' })

    if test:
      execute(test)
    else:
      keys = list(params.keys())
      def handler(kid):
        if kid >= 0:
          execute(keys[kid])
      self.window.show_quick_panel(keys, handler)
