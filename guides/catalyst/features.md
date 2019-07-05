[frontMatter]
title = "Features"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---

Here's a bullet point guide on Catalyst:


- Run iPad apps on macOS
- macOS 13.0 only
- Supports most of iOS (i.e. no ARKit)
- Adds [macOS sandbox](rel::how/sandbox.md) support (and a `AppName.entitlements` file
- Uses [Settings.bundle](rel::firststeps/preferences.md) for automatic macOS Preferences
- You can build full-fledged macOS apps
- You can sell your apps outside of the Mac App Store
- Dynamic Type is disabled as it doesn't exist on macOS. Everything is *Large*
- Your whole app, when run on macOS, is resized to 77% of the original size. That's all automatic and in the background 
- A default menu bar for your app.
- Support for trackpad, mouse, and keyboard input.
- Support for window resizing and full-screen display.
- Mac-style scroll bars.
- Copy-and-paste support.
- Drag-and-drop support.
- Support for system Touch Bar controls.

Apart from that, another major difference is that the Application Lifecycle behaves slightly different. We will look at that next.
