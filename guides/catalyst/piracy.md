[frontMatter]
title = "How do I prevent piracy?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# This more or less only affects paid apps

On iOS, Apple automatically deploys code that does receipt validation and makes sure that your app can't just be pirated by copying it from device to device (albeit this still being a possibilty on rooted iOS devices).

On macOS, users can just copy the `MyApp.app` folder to a different Mac and run it. By default, macOS does not perform any receipt validation whatsoever. [Apple has some guides on how to implement the necessary code to perform receipt validation yourself.](https://developer.apple.com/library/archive/releasenotes/General/ValidateAppStoreReceipt/Introduction.html).

# Please Don't do that!

This is rather difficult to do properly, and even then you have to do it in a way that can't be easily circumvented by hackers. This is certainly doable but requires an astonishing amount of work. There's a much better solution.

# Receigen

[Receigen](http://receigen.etiemble.com) is a fantastic macOS app that will automatically generate the required receipt validation code for you. I strongly suggest using *Receigen* or an alternative solution.

