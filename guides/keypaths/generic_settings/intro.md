[frontMatter]
title = "Example: Generic Settings"
tags = ["keypath", "abstraction"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Generic Settings

Our first practical example showcases how keypaths, protocols, and keypath composition work together to allow you to handle app settings in a generic manner. Here is the problem we're trying to solve, have a look at these different settings screens for our `Chat` app:

![Image](/img-content/keypaths_settings.gif)

Lets map those settings as a type:

``` Swift

final class ProfileSettings {
  var displayName: String
  var shareUpdates: Bool
}

final class PrivacySettings {
  var passcode: Bool
  var addByID: Bool
}

final class Settings {
  var profileSettings: ProfileSettings
  var privacySettings: PrivacySettings
}
```

If we want to find a generic abstraction for these settings, it would be very difficult. That's because they're all so very different. Their types are `String, Bool`, `Bool, Bool`, and `ProfileSettings, PrivacySettings`. 
Even more, as we expand our settings they will become more and more different. 
Lets try to find a nice solution for this by utilizing keypaths.
