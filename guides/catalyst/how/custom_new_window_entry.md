[frontMatter]
title = "add a `New Window` entry to a custom MainMenu?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I add a `New Window` entry to a custom MainMenu? how/custom_new_window_entry.md

Once you modify your Main Menu, you will find that the entry to create a new window has suddenly disappeared. That happens because the `New Window` entry is dynamicaly inserted by UIKit depending on whether your app supports multiple windows (or not).

In order to support this again, you have to do the following:

1. Create a new `UICommand` in your Storyboard for the `New Window` entry.
2. Assign the title and your desired shortcut (probably Command + N).
3. Select the `First Responder` in your `MainMenu Scene`

![](/img-content/catalyst/storyfirstresponder.png)

4. Switch to the *Attributes Inspector* (from the inspectors on the right)
5. There, you will find an empty list named "User Defined"
6. Add a new entry to this list with the following attributes:
7. Action: `requestNewScene:`, Type: `id` (the default)
8. Finally, drag from your `UICommand` menu entry to the First Responder and select the newly created action.
