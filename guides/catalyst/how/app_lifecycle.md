[frontMatter]
title = "How does the iOS app lifecycle work on macOS?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How does the iOS app lifecycle work on macOS?

The ["Taking iPad apps for Mac to the Next Level" talk at WWDC 2019](https://developer.apple.com/videos/play/wwdc2019/235/) has a fantastic overview of all the changes. Here is a brief overview:

- The `UIApplication` lifecycle is fully supported on macOS
- The sequence is the same as on macOS
- State changes, however, do affect the Mac less, as are almost always *Foreground* + *Active* on macOS.
- Apps only enter background during termination and inactive when launching in the background.
- Your app should still take [App Napp](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/power_efficiency_guidelines_osx/AppNap.html) into account
- Background modes are allowed to finish when an app closes. The background tasks continue even though the app is already not visible anymore to the user
- Apps are not killed when they consume too much memory
- Background audio is not supported because users expect audio to stop when they quit an app
