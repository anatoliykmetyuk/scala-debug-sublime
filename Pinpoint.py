import sublime, sublime_plugin
import json, os, re

build_file = None
dotty_dir = None
pinpoint_cfg_file = None

def locate_build_file(root):
  pattern = re.compile(r'.*/dotty/project/Build\.scala$')
  for root, dirs, files in os.walk(root):
    for file in files:
      full_path = os.path.join(root, file)
      if pattern.match(full_path):
        return full_path

def init(roots, settings):
  # Locate the build file and the pinpoint config
  global build_file
  global dotty_dir
  global pinpoint_cfg_file
  if not build_file or not dotty_dir or not pinpoint_cfg_file:
    root = os.path.commonprefix(roots)
    build_file = locate_build_file(root)
    dotty_dir = os.path.dirname(os.path.dirname(build_file))
    pinpoint_cfg_file = os.path.join(dotty_dir, settings['pinpoint_cfg'])

  # Write default pinpoint config if it doesn't exist already
  if not os.path.exists(pinpoint_cfg_file):
    default_settings = {
      "markers": [],
      "hash_size": 8
    }
    write_pinpoint_settings(default_settings)

  # Check if the build dependency is there, if not – write it after a given marker
  build_contents = ''
  with open(build_file, 'r', encoding='utf8') as f:
    build_contents = f.read()
  if settings['build_dep'] not in build_contents:
    build_contents = build_contents.replace(settings['build_dep_marker'],
      settings['build_dep_marker'] + '\n' + settings['build_dep'])
    with open(build_file, 'w', encoding='utf8') as outfile:
      outfile.write(build_contents)

def pinpoint_settings():
  with open(pinpoint_cfg_file) as cfgFile:
    return json.loads(cfgFile.read())

def write_pinpoint_settings(settings):
  with open(pinpoint_cfg_file, 'w') as outfile:
    json.dump(settings, outfile)

class PinpointInitCommand(sublime_plugin.WindowCommand):
  def run(self):
    settings = sublime.load_settings("Pinpoint.sublime-settings").get("settings")  # To have the nice ['foo'] syntax
    init(self.window.folders(), settings)
    # open.pinpoint_cfg_file
