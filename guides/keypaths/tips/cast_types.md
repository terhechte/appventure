[frontMatter]
title = "Cast Types"
tags = ["keypath", "casting", "type-cast", "anykeypath", "erase"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# 2. Cast Types Back

This is the opposite of what we just did. Instead of removing types, we're adding types back:

``` Swift
AnyKeyPath as? WritableKeyPath<User, String>
PartialKeyPath<User> as? KeyPath<User, Bool>
```

Sometimes you might need to add generics in order to keep the necessary types around to perform the correct casting. An example of this was how we wrote

``` Swift
editSettings<Provider: SettingsProvider>(provider: Provider)
```

instead of the simpler:

``` Swift
editSettings(provider: SettingsProvider)
```

The second version would work just as fine, but it would not allow us to use `Provider` as the `Root` type in our `WritableKeyPath<Provider, Bool>` cast.
