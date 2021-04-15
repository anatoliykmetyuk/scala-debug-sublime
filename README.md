# DottyDebug
Tracing issues in big codebases is hard. As with any task, for effective work, it is imperative to have the right tools to trace issues.

[Dotty](https://github.com/lampepfl/dotty) is one such codebase. And this project is one such tool to trace issues in it effectively. DottyDebug is a plugin for [Sublime Text 3](https://www.sublimetext.com/) that teaches this editor to do tasks related to tracing.

# Installation
- Install Sublime Text 3.
- Install [Origami](https://github.com/SublimeText/Origami) and [Terminus](https://github.com/randy3k/Terminus) packages via `cmd+shift+P`->`Package Control: Install Package`.
- If you want to use Scala LSP, see this [guide](https://scalameta.org/metals/docs/editors/sublime.html).
- Clone this repo into `~/Library/Application Support/Sublime Text 3/Packages/`.
- Install [Dotty Issues Workspace](https://github.com/anatoliykmetyuk/dotty-issue-workspace), read its README to learn how it works.

# Usage
## Environment setup
1. Open the Dotty folder in Sublime
2. Open a terminal as follows:
  1. `cmd+k` followed by right arrow: split editor screen into two panes (see Origami docs for details).
  2. `cmd+shift+P`->`terminus view` to create a terminal, drag and drop it to the new pane.
  3. Go to the Dotty directory and run `sbt` there.

## Navigation
When dealing with stack traces, you can jump to individual stack frames by `alt+click`'ing on them.

## Debugging variables
This plugin also adds ability to quickly see the values of the variables in the Dotty codebase. This is done by the virtue of text replacement: you select a variable, press a hotkey, and it gets instrumented with debug code. E.g. a variable `foo` may be replaced by `{ val r = foo; pinpoint.log(s"""foo = ${r}""", 0); foo }`.

You can read all available replacements in [settings](DottyDebug.sublime-settings) (`scala_debug`->`snippets`) section, and the hotkeys in [keymap](Default.sublime-keymap).

For example, if you highlight variable `qual1` somewhere in the Dotty codebase and press `alt+a`, it will be replaced with:

```scala
{ val r = qual1; pinpoint.log(s"""qual1 = ${r.show}""", 1); r }
```

Note that you do not need to explicitly add the dependency on Pinpoint to the Dotty's build file: when you press a hotkey from this plugin, it will be added to `Build.scala` automatically if not already there – you just need to reload SBT after pressing a hotkey for the first time.

## Conditional debugging
There are methods in Dotty which are "hotspots": called many times on many different inptus throughout the compilation lifecycle. E.g. the Typer's `adapt1` is one of them, which may go something as follows:

```scala
private def adapt1(tree: Tree, pt: Type)(using Context): Tree = {
  ...
  doSomethingWith(tree)
  ...
  doSomethingWith(pt)
  ...
}
```

Often you want to debug one variable (say `pt`) only when another variable (say `tree`) has a certain value. E.g. if you're debugging a case when a typer errors on `val x: Int = "String"`, you are interested only in that tree, not in other stuff Typer may be working with.

A trivial solution is to use `if tree == ... then /* log pt */`. However it doesn't scale well: you need to write the condition manually, and you need to figure out what to compare that `tree` against.

A more general solution is to predicate not on the value of `tree`, but on the log's line number on which that `tree` gets printed. Pinpoint logs are prefixed by line number. Selecting that number and pressing `alt+q` on it will be equivalent to predicating all subsequently added log statements with `if (log_line == selected_line)`. This hotkey will add that line to `pinpoint-cfg.json` file which will be created in the root of the Dotty repo.

# Troubleshooting the plugin
This plugin works only on the Dotty repo. It is still work in progress. If something doesn't work as expected, you are encouraged to first check Sublime console (`` ctrl+` ``). If that doesn't work, you can check the plugin sources (`cmd+shift+p -> view package file -> DottyDebug/`).

It is good to be familiar with Sublime plugin system to troubleshoot this plugin – a great intro course is [here](https://www.youtube.com/playlist?list=PLGfKZJVuHW91zln4ADyZA3sxGEmq32Wse).
