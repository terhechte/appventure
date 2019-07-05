[frontMatter]
title = "support multiple windows?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I support multiple windows firststeps/multiple_windows.md

Initially, this is rather simple. You just need to enable the *Supports multiple windows* setting for your target:

![](/img-content/catalyst/multiwindow.png)

After this, if you didn't [create your own MenuBar](firststeps/modify_menubar.md), you will have a new *New Window* `Control + N` shortcut that you can use to instantiate a new window.

If you did modify your menubar (as explained above) [you can re-create the *New Window* shortcut by following these explanations.](how/custom_new_window_entry.md)

Finally, if you want to support multiple *different* windows, that is [explained here](how/multiple_different_windows.md)
