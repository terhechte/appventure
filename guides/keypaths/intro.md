[frontMatter]
title = "Introduction"
tags = ["keypath", "valueForKeyPath"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
feature_image = "https://appventure.me/img-content/keypath_feature_image.gif"
---

# KeyPaths in Swift

Lets talk KeyPaths. Modern KeyPaths. **Swift KeyPaths**. Not `Objective-C`'s  `valueForKeyPath: @"controller.property"`.

These particular, modern, swifty, keypaths were added with Swift 4.2. They differ from the old `Objective-C` ones by being type-safe and composable. 

Not everyone is aware of the useful functionality that Swift's new keypaths offer. They're a great addition to your toolbelt because they allow you to find abstractions for problems where protocols alone are not sufficient.

This guide will first introduce Swift's KeyPaths, then discuss the underlying theory, showcase their usefulness with practical examples, and finally list tips and tricks for applying them in daily work.

Lets start with a very basic introduction.
