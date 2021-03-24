import sublime, sublime_plugin
import os, json


def load_ab_debug_params(window):
  for view in window.views():
    if view.file_name():
      if os.path.splitext(view.file_name())[1] == '.abdebug':
        params_raw = view.substr(sublime.Region(0, view.size()))
        return sublime.decode_value(params_raw)

class AbDebugCreateParamsFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    test_file = self.view.window().new_file(syntax = 'Packages/JavaScript/JSON.sublime-syntax')
    test_file.set_name('TestParams.abdebug')
    default_params = sublime.load_resource('Packages/DottyDebug/resources/DefaultDebugParams.abdebug')
    test_file.insert(edit, 0, default_params)

class AbDebugCommand(sublime_plugin.WindowCommand):

  def find_terminus_view(self):
    for view in self.window.views():
      if view.name() == 'Login Shell' or 'Terminus' in view.name():
        return view

  def run(self, test = None):
    params = load_ab_debug_params(self.window)

    def execute(target_test):
      target_test_params = params[target_test]
      terminus_view = self.find_terminus_view()

      self.window.status_message('Debugging case: {0}'.format(target_test))

      self.window.run_command('pinpoint_set',
        { 'markers': target_test_params['markers'] })
      terminus_view.run_command('terminus_reset')

      def callback():
        self.window.run_command('terminus_send_string',
          { 'string': target_test_params['command'] + '\n' })
      sublime.set_timeout(callback, 200),

    if test:
      execute(test)
    else:
      keys = list(params.keys())
      def handler(kid):
        if kid >= 0:
          execute(keys[kid])
      self.window.show_quick_panel(keys, handler)
