import sublime
import sublime_plugin
import os, re

def get_filepaths_with_oswalk(root_path: str, file_regex: str):
  files_paths = []
  pattern = re.compile(file_regex)
  for root, directories, files in os.walk(root_path):
    for file in files:
      if pattern.match(file):
        files_paths.append(os.path.join(root, file))
  return files_paths

def view_coords(view):
  first_visible_point = view.visible_region().a
  x, y = 0, 0
  while x == 0 and y == 0 and first_visible_point < len(view):
    x, y = view.text_to_window(first_visible_point)
    first_visible_point = first_visible_point + 1  # Find the first fully visible character
  return x, y - view.line_height()

class OpenFileOnClickCommand(sublime_plugin.WindowCommand):
  cache = []

  def locate_file(self, target):
    if not self.cache:
      for folder in self.window.folders():
        self.cache = get_filepaths_with_oswalk(folder, ".*\.(scala|java)$")
    return [s for s in self.cache if s.endswith('/{0}'.format(target))]

  def locate_current_view(self, x, y):
    for view in self.window.views():
      x0, y0 = view_coords(view)
      xExt, yExt = view.viewport_extent()
      xMax, yMax = (x0 + xExt, y0 + yExt)

      if x >= x0 and x <= xMax and y >= y0 and y <= yMax:
        return view

  def run(self, event):
    clickedView = self.locate_current_view(event['x'], event['y'])
    point = clickedView.window_to_text((event['x'], event['y']))
    highlightRegion = clickedView.expand_by_class(point,
      sublime.CLASS_WORD_START | sublime.CLASS_WORD_END, ' ')
    highlight = clickedView.substr(highlightRegion)

    if re.compile(r'^[\w\.\$\(\)\:]+$').match(highlight):
      self.jump_to_stack_frame(highlight)
    else:
      self.jump_to_ref(highlight)

  def jump_to_stack_frame(self, frame):
    print('Stack jump: ' + frame)
    m = re.search(r'\(([\w\.]+):(\d+)\)$', frame)
    if m:
      self.jump_to_file(m.group(1), m.group(2))

  def jump_to_ref(self, ref):
    print('Ref jump: ' + ref)
    m = re.search(r'/([\w\.]+):(\d+)$', ref)
    if m:
      self.jump_to_file(m.group(1), m.group(2))

  def jump_to_file(self, filename, line):
    files = self.locate_file(filename)

    if len(files) == 0:
      print('File not found: {0}'.format(filename))

    elif len(files) == 1:
      self.window.open_file(
        '{0}:{1}'.format(files[0], line), sublime.ENCODED_POSITION)

    else:
      print('More than one alternative found for {0} – unsupported for the moment'.format(filename))


  def want_event(self):
    return True
