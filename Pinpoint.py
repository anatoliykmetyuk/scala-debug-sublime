import sublime, sublime_plugin
import json, os, re

def locate_build_file(root):
  pattern = re.compile(r'.*/dotty/project/Build\.scala$')
  for root, dirs, files in os.walk(root):
    for file in files:
      full_path = os.path.join(root, file)
      if pattern.match(full_path):
        return full_path

def init(roots):
  global build_file
  global dotty_dir
  global pinpoint_cfg_file
  if not build_file or not dotty_dir or not pinpoint_cfg_file:
    root = os.path.commonprefix(roots)
    build_file = locate_build_file(root)
    dotty_dir = os.path.dirname(os.path.dirname(build_file))
    pinpoint_cfg_file = os.path.join(dotty_dir, 'pinpoint-cfg.json')

    if not os.path.exists(pinpoint_cfg_file):
      default_settings = {
        "markers": [],
        "hash_size": 8
      }
      write_pinpoint_settings(default_settings)

def pinpoint_settings():
  pinpoint_settings_str = open(pinpoint_cfg_file).read()
  return json.loads(pinpoint_settings_str)

def write_pinpoint_settings(settings):
  with open(pinpoint_cfg_file, 'w') as outfile:
    json.dump(settings, outfile)

class PinpointInitCommand(sublime_plugin.WindowCommand):
  def run(self):
    init(self.window.folders())
    # open.pinpoint_cfg_file
