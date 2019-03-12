[frontMatter]
title = "Custom Mirrors"
tags = ["reflection", "mirror", "CustomReflectable"]
created = "2019-03-01 11:47:01"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Custom Mirrors

As we already discussed earlier, there\'re other options creating a
Mirror. This is useful, for example, if you need to customize just how
much of your **subject** can be seen with a mirror. The `Mirror Struct`
has additional initializers for this.

This is especially useful in two cases:

1. If reflection is a core part of your code, so that you have more control
2. If you write a library and you expect that consumers will use reflection on it and you'd rather surpress that.

The way you use it is via the `CustomReflectable` protocol. This protocol only has one requirement: `var customMirror: Mirror`. If you implement it, you can create your own `Mirror` and return that instead of the custom `Mirror(reflecting:)` one.
