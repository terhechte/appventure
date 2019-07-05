[frontMatter]
title = "enable / disable toolbar items based on whats visible on screen?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I enable / disable toolbar items based on whats visible on screen?

Currently, there doesn't seem to be a way to do this. I've tracked this as issue *FB6360289* in Apple's Feedback tool.

I could not figure out how to dynamically update the enabled / disabled status of toolbar items based on app actions such as a new controller entering the responder chain. This makes it very difficult to implement toolbars that adapt to the users actions. Event Apple’s own Catalyst apps seem to be affected by this: The Stocks app has a “Share” toolbar item that just does nothing when pressed and nothing is selected (it is enabled, not disabled).

The best solution is to have a singleton with access to the toolbar (or as a dependency injection) and then call a method on it that updates the contents of the toolbar. An easy way to do that is by iterating over the `toolbar.items` property and updating each entry accordingly (disabling / enabling).
