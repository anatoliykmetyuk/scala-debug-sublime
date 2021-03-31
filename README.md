# Installation
- Install Sublime Text 3.
- Install [Origami](https://github.com/SublimeText/Origami) and [Terminus](https://github.com/randy3k/Terminus) packages via `cmd+shift+P`->`Package Control: Install Package`.
- If you want to use LSP, see this [guide](https://scalameta.org/metals/docs/editors/sublime.html).
- Clone this repo into `~/Library/Application Support/Sublime Text 3/Packages/`.
- Install [Dotty Issues Workspace](https://github.com/anatoliykmetyuk/dotty-issue-workspace), read its README to learn how it works.

# Usage
## Setup
1. Open the Dotty folder in Sublime
2. Open a terminal as follows:
  1. `cmd+k` followed by right arrow: split editor screen into two panes (see Origami docs for details).
  2. `cmd+shift+P`->`terminus view` to create a terminal, drag and drop it to the new pane.
  3. Go to the Dotty directory and run `sbt` there.

## Jump stack frames
`alt+click` on a stack trace frame will take you to that frame.

## Pinpoint: Variables Debug
### Debug hotkeys
You can highlight any variable in Dotty and press certain hotkeys to instrument it with debug code. See `Default.sublime-keymap` for the key bindings and `DottyDebug.sublime-settings`->`scala_debug`->`snippets` for what they do to a variable.

For example, if you highlight variable `qual1` somewhere in the Dotty codebase and press `alt+a`, it will be replaced with:

```scala
{ val r = qual1; pinpoint.log(s"""qual1 = ${r.show}""", 1); r }
```

### Pinpoint: multilevel logging
There are methods in Dotty which are "hotspots": called many times on many different inptus throughout the compilation lifecycle. E.g. the Typer's `adapt` is one of them. Often you are interested in only how such a method behaves given one particular input though.

This is where Pinpoint plugin, which is part of this repo, comes in.
