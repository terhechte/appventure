[frontMatter]
title = "What are some coding best practices for macOS support?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# What are some coding best practices for macOS support

Catalyst is still a fresh technology. So far, based on our current knowledge, the following best practices have emerged:

- Try to use conditional compilation (via `#if targetEnvironment(UIKitForMac`) sparringly
- Your view redraw code should be fast as macOS users frequently resize windows (in a dynamic manner)
- Have proper autolayout support for bigger and smaller sizes as windows can be resized in a variety of ways
- Be aware of the [responder chain](how/responder_chain.md) as multiple view controllers can be on the screen at the same time
- Your app can run forever, memory leaks can pile up
