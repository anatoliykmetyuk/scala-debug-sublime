import sublime, sublime_plugin
import os, json
from .Pinpoint import init

ab_debug_cfg_file = None

def load_ab_debug_params(roots):
  init(roots)
  from .Pinpoint import dotty_dir
  global ab_debug_cfg_file
  if not ab_debug_cfg_file: # Init filename
    ab_debug_cfg_file = os.path.join(dotty_dir, 'abdebug_cfg.json')

  if not os.path.exists(ab_debug_cfg_file): # Create config if not exists
    default_params = sublime.load_resource('Packages/DottyDebug/resources/DefaultAbDebugParams.json')
    with open(ab_debug_cfg_file, 'w') as outfile:
      outfile.write(default_params)

  with open(ab_debug_cfg_file) as cfgFile: # Read the config into json
    return json.loads(cfgFile.read())

class AbDebugOpenConfigCommand(sublime_plugin.WindowCommand):
  def run(self):
    load_ab_debug_params(self.window.folders())  # Create the file if not exists
    self.window.open_file(ab_debug_cfg_file)

class AbDebugCommand(sublime_plugin.WindowCommand):

  def find_terminus_view(self):
    for view in self.window.views():
      if view.name() == 'Login Shell' or 'Terminus' in view.name():
        return view

  def run(self, test = None):
    init(self.window.folders())
    params = load_ab_debug_params(self.window.folders())

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
