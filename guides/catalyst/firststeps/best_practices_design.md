[frontMatter]
title = "What are some design best practices for macOS support?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# What are some design best practices for macOS support

These guidelines are based on information that Apple shared in different WWDC keynotes

- Most Important: [Apple has Human Interface Guidelines for *iPad Apps for Mac*](https://developer.apple.com/design/human-interface-guidelines/ios/overview/ipad-apps-for-mac/)
- Macs don't have dynamic type. Everything is "Large"
- Mac users have many windows open. Therefore you should set focus on the contents of the window. This means using less color so that the contents can shine
- Use side bars and toolbars instead of a UITabBar
- Try to take advantage of the bigger macOS windows. You can utilize different layouts and use the space wisely
- Default font size on macOS is 13pt compared to 17pt on iOS. This is handled automatically for you though, as each app is scaled to 77% of its actual size
