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

class OpenFileOnClickCommand(sublime_plugin.WindowCommand):
  cache = []

  def locate_file(self, target):
    if not self.cache:
      for folder in self.window.folders():
        print("Start on " + folder)
        self.cache = get_filepaths_with_oswalk(folder, ".*\.scala$")

    print("Found " + str(len(self.cache)) + " files")

    print("Now let's see which one ends with Main.scala")
    results = [s for s in self.cache if s.endswith(target)]

    for r in results:
      print(r)

    return results

  def locate_current_view(self, x, y):
    for view in self.window.views():
      x0, y0 = self.view_coords(view)
      xExt, yExt = view.viewport_extent()
      xMax, yMax = (x0 + xExt, y0 + yExt)

      # print('x: {0} >= {2}, {0} <= {3}; y: {1} >= {4}, {1} <= {5}'
      #   .format(x, y, x0, xMax, y0, yMax))

      if x >= x0 and x <= xMax and y >= y0 and y <= yMax:
        return view

  def debug_views(self):
    for view in self.window.views():
      print("Visible region: {0}".format(view.visible_region()))
      x0, y0 = view.text_to_window(view.visible_region().a)
      xExt, yExt = view.viewport_extent()
      xMax, yMax = (x0 + xExt, y0 + yExt)

      print('{4}: x: {0} to {1}, y: {2} to {3}'
        .format(x0, xMax, y0, yMax, view.id()))

  def view_coords(self, view):
    first_visible_point = view.visible_region().a
    x, y = 0, 0
    while x == 0 and y == 0 and first_visible_point < len(view):
      x, y = view.text_to_window(first_visible_point)
      first_visible_point = first_visible_point + 1  # Find the first fully visible character
    return x, y - view.line_height()

  def run(self, event):
    # Capture the text under the cursor
    # print("Got event: " + str(event))

    # # Get view from event (mouse coordinates)
    clickedView = self.locate_current_view(event['x'], event['y'])

    # # Get point of the view from event
    point = clickedView.window_to_text((event['x'], event['y']))

    # # Get filename from the point
    word = clickedView.expand_by_class(point,
      sublime.CLASS_WORD_START | sublime.CLASS_WORD_END, ' ')
    print('Word: {0}'.format(clickedView.substr(word)))

    # # self.locate_file("Repl.scala")

  def want_event(self):
    return True
