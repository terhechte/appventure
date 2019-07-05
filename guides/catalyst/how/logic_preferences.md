[frontMatter]
title = "How do I implement preferences with additional logic?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



Now, if you have more involved logic in your settings, special view controllers, web views, and other things, then this doesn't work well for you. In that case, you basically have three options.

1. Don't display the preferences in a window, but present the view controller as a modal form or sheet instead
2. Use the [new iOS multi window support to](firststeps/multiple_windows.md), only on macOS, open the settings controller in a new window. This is a bit more involved but certainly the most feasible solution.
3. Use AppKit to macOS specific preferences in a separate AppKit bundle and load it at runtime. We won't dive into this here, but you can find [more information on this in Steve Troughton-Smith' excellent article on the topic.](https://www.highcaffeinecontent.com/blog/20190607-Beyond-the-Checkbox-with-Catalyst-and-AppKit)
