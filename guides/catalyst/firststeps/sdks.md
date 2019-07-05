[frontMatter]
title = "Third Party SDKs"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---

Catalyst requires new builds of your third party frameworks and SDKs. The iOS or Simulator builds are not appropriate. This means that until your third party, closed source advertising or tracking library offers a new release with an added `UIKitForMac` target, you won't be able to build your app.

As a temporary solution, if you wrapped all these dependencies in a wrapper, [you can just use conditional compilation to just not ship them on macOS.](rel::firststeps/conditional_compilation.md)
