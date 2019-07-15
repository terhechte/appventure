[frontMatter]
title = "How do I implement preferences on macOS?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



In order to implement the preferences or your app, [Apple supports the *Settings.bundle* technology that has been there since iOS 2.0 (or rather, iPhoneOS 2.0)](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/UserDefaults/Preferences/Preferences.html). The documentation is actually so old, that it is archived and the documentation screenshots look like this:

![](/img-content/catalyst/settings2.jpg)
![](/img-content/catalyst/settings3.jpg)

On iOS, this means that you just need to add a new bundle target to your project and fill it with a collection of specially crafted `Plist` files. These settings then appear in the general iOS settings and any changes done there are stored in the `NSUserDefaults`.

If your app supports settings bundles, then your Catalyst app will automatically add a Preferences window to your app that looks something like this:

![](/img-content/catalyst/settings1.png)

For details on how to achieve this, [refer to Apples documentation.](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/UserDefaults/Preferences/Preferences.html)

Now, if you have more involved logic in your settings, special view controllers, web views, and other things, then this doesn't work well for you. [In that case, you can read here how to implement more complex preferences on macOS.](how/logic_preferences.md)

# Preferences with a Toolbar

Now, one thing you might wonder is how to get this wonderful Preferences Toolbar, that Apple has in their Podcast app (see the last screenshot). [As it turns out, this is currently completely undocumented, and we're explaining the details of how to achieve this here.](rel::how/preferences_toolbar.md)
