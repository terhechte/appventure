[frontMatter]
title = "Settings Provider"
tags = ["keypath", "generics", "protocol"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# A Settings Provider

Now that we have our `SettingsEntry` type, we need a way to provide all the settings entries that make up our UI. This is where protocols are a great solution. We want something that works for our different settings types (`Settings`, `ProfileSettings`, `PrivacySettings`), and protocols are made for just that. Our concrete protocol is defined to provide our applications with the specific settings for a type, so we will call it `SettingsProvider`.

``` Swift
protocol SettingsProvider {
  var settingsEntries: [SettingsEntry] { get }
}
```

It is also a fairly simple protocol. The only thing it does is provide a `getter` to return an array of `SettingsEntry` types for one of our settings types. Lets implement it:

``` Swift
extension Settings: SettingsProvider {
 var settingsEntries: [SettingsEntry] {
  return [
      SettingsEntry(
          keyPath: \Settings.profileSettings, 
            title: "Profile"),

      SettingsEntry(
          keyPath: \Settings.privacySettings, 
            title: "Privacy")
  ]
 }
}
```

Our first implementation is for our main parent `Settings` `class`. It has two properties that we'd like to be displayed in the settings, the `Profile Settings` and the `Privacy Settings`, which is why we're returning these two as `SettingsEntry` types.

Next up, we will implement the `SettingsProvider` for our `ProfileSettings`:

``` Swift
extension ProfileSettings: SettingsProvider {
 var settingsEntries: [SettingsEntry] {
  return [
    SettingsEntry(
       keyPath: \ProfileSettings.displayName,
         title: "Display Name"),

    SettingsEntry(
       keyPath: \ProfileSettings.shareUpdates,
         title: "Share Profile Media Updates")
  ]
 }
}
```

Again, we return two settingsEntries, because this settings screen should display the `Display Name` and `Share Updates` setting. Finally, we obviously also need to implement our `SettingsProvider` for our `PrivacySettings`.

``` Swift
extension PrivacySettings: SettingsProvider {
 var settings: [SettingsEntry] {
  return [
    SettingsEntry(
        keyPath: \PrivacySettings.addByID, 
          title: "Allow add me by ID"),

    SettingsEntry(
        keyPath: \PrivacySettings.passcode, 
          title: "Passcode Lock")
  ]
 }
}
```

No surprises here.
