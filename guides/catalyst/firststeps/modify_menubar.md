[frontMatter]
title = "How do I modify the menubar?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



In the WWDC slides and the sample code, Apple touts a `buildCommands` method on `UIResponder` for menus. [However, this was deprecated with beta 1](https://developer.apple.com/documentation/uikit/uiresponder/3175394-buildcommands). Instead, we should use [buildMenu(with:)](https://developer.apple.com/documentation/uikit/uiresponder/3327317-buildmenu). This currently lacks documentation though.

It seems, currently, the best way to modify the Menubar (or, `MainMenu`) is by using storyboards and dropping a `Main Menu` into your storyboard. This new scene will be just like the default menu, but you can edit it.
