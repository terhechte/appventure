[frontMatter]
title = "sign the app?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# How do I sign the app

Catalyst apps, just like simulator apps, do not require signing. However, since Catalyst apps run on the real hardware, right away, they are set up for signing by default.

If you have a paid Apple Developer account, that is not a problem. However if you're a student or just looking into Catalyst, you might not have a paid Apple Developer account.

Thankfully, you can test Catalyst apps just fine without a paid account. You only have to go into the signing settings of Xcode (*"Target"* -> *"Signing & Capabilities"* -> *"Signing Certificate"*) and then select *Sign to Run Locally*.

Now, Xcode will still complain with a small red alert that says *"Signing for ... requires a development team"*, however it will build the app just fine and also run it just fine.

![](/img-content/catalyst/signing_settings.png)

## Signing Frameworks

If you're signing locally and your code is split up into frameworks, it may be the case that you're getting code signing errors *when your binary starts*. So, your code is building fine, it is sining fine, but when the Catalyst App actually starts, it will crash with a code signing error. The current known way to prevent this is to have the following settings for your *main target* and for your *frameworks* (screenshots below):

### Main Target
- Automatically Manage Signing
- Team: A working account
- Signing Certificate: Apple Development

![](/img-content/catalyst/signing_frameworks1.png)

### Any Framework Target
- Automatically Manage Signing
- Team: The same working account
- Signing Certificate: Sign to run locally

![](/img-content/catalyst/signing_frameworks2.png)

Keep in mind that the frameworks and the main target need to have distinct bundle identifiers.

This issue does appear to only happen to some people.
