[frontMatter]
title = "Settings Entries"
tags = ["keypath", "anykeypath"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Settings Entries

Fundamentally, the first thing we need is a way to describe a particular settings entry. It is not sufficient to just know the value of the settings; we also need a title, a subtitle, maybe some help, or an icon. We will summarize this information into a `SettingsEntry` struct. This struct will also contain a keypath that points at the individual value this setting refers to.

``` Swift
struct SettingsEntry {
  let keyPath: AnyKeyPath
  let title: String
  let subtitle: String
  let icon: UIImage
}
```

For the sake of simplicity, we will use the following, shorter struct in the upcoming code examples:

``` Swift
struct SettingsEntry {
  let keyPath: AnyKeyPath
  let title: String
}
```

Note that the type of the keypath is `AnyKeyPath`. We have to do that because our types can be anything: `\Settings.privacySettings`, `\PrivacySettings.passcode`, or `\ProfileSettings.displayName`.
