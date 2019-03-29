[frontMatter]
title = "Handling Settings"
tags = ["keypath", "generics", "recursion", "anykeypath", "type-cast"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Handling the Settings

The next part is crucial. What do we intend to do with these settings? The natural way would be to build a UI that displays them and allows the user to edit them. Another option would be to set settings to specific values. All of these things are possible. We will do something slightly simpler which still explains the basics of the code without requiring us to write a lot of UI code. In this example, we will iterate over the settings, print out their title and value, and will then change the value to `true` if it is `Bool`. However, as mentioned above, you can use the very same pattern to display these settings in a very nice UI.

The first thing we need is a function we can call with our settings. This function needs to be generic. We should be able to call it with any type. To do this, it will only have one argument of the `SettingsProvider` type. However, later on, we will also need the specific type that implements the protocol, which is why we code this in a generic manner:

``` Swift
func editSettings<Provider: SettingsProvider>(provider: Provider) {
  ...
}

/// And lets call it
let appSettings = Settings()
editSettings(appSettings)
```

Since our `SettingsProvider` only really offers one property, the `settingsEntries` we will iterate over them:

``` Swift
func editSettings<Provider: SettingsProvider>(provider: Provider) {
  for setting in provider.settingsEntries {
    
  }
}
```

Remember how we created settings entries for nested settings, such as `ProfileSettings` as well as the actual settings values, such as `PrivacySettings.passcode`? In this case, we have to disambigiuate, do we have an actual value that we want to print and edit, or do we have another, nested, settings provider? To do this, we will get the value of the current `KeyPath` from the `Provider`:

``` Swift
func editSettings<Provider: SettingsProvider>(provider: Provider) {
  for setting in provider.settingsEntries {
    let value = provider[keyPath: setting.keyPath]
  }
}
```

Here, we tell Swift to give us the value in the current `SettingsProvider` at the `KeyPath` `setting.keypath`. This doesn't really solve our problem, though. This value could still be a `Bool` type or a `PrivacySettings` type. We can't check whether the type is `PrivacySettings` because we want to be generic, work with any type. However, since all nested settings also **have** to implement the `SettingsProvider` protocol, we can simply test for this:

``` Swift
func editSettings<Provider: SettingsProvider>(provider: Provider) {
  for setting in provider.settingsEntries {
    let value = provider[keyPath: setting.keyPath]
    if let nestedProvider = value as? SettingsProvider {
    }
  }
}
```

Via the `value as? SettingsProvider` we're just asking Swift at runtime whether the `value` is actually a type we want to handle (such as `Bool`, or `String`) or another nested `SettingsProvider` that we'd like to iterate over. Which is precisely what we will do next, iterate over the provider again. However, since we may have another settings provider, and then another one, we would need to write more and more for loops:

``` Swift
  for setting in provider.settingsEntries {
    let value = provider[keyPath: setting.keyPath]
    if let nestedProvider = value as? SettingsProvider {
      for nestedSetting in nestedProvider.settingsEntries {
        let value = provider[keyPath: nestedSetting.keyPath]
        if let nestedNestedProvider = value as? SettingsProvider {
          for nestedNestedSetting in nestedNestedProvider.settingsEntries {
          ...
          }
        }
      }
    }
  }
```

This is truly terrible. Instead, we will move this iteration code into a inlined function `updateSetting` that can be called recursively. So, whenever we identify another nested provider, we will simply call the function again:

``` Swift
func editSettings<Provider: SettingsProvider>(provider: Provider) {
  // All subsequent iterations happen here
  func updateSetting(keyPath: AnyKeyPath, title: String) {
    let value = provider[keyPath: keyPath]
    if let nestedProvider = value as? SettingsProvider {
      for item in nestedProvider.settings {
        // ??
      }
    }
  }

  // The initial iteration
  for setting in provider.settingsEntries {
    updateSetting(keyPath: setting.keyPath, title: setting.title)
  }
}
```

Here, we moved the iteration code into its own function. It has two parameters, the `keyPath` of the value we want to test, and the title of the current setting. The keypath helps us to extract the value:

``` Swift
let value = provider[keyPath: keyPath]
```

The value is then tested for being another `SettingsProvider`:

``` Swift
if let nestedProvider = value as? SettingsProvider {
 ...
}
```

But what do we do now? In the first step, here, the `keyPath` would be `\Settings.profileSettings` and the `value` will be `ProfileSettings`. 
But what do we do now? If we iterate over the `ProfileSettings` as a `SettingsProvider` we get two new SettingsEntries, one for `displayName`, and one for `shareUpdates`. However, our `updateSetting` function always calls `let value = provider[keyPath: keyPath]` on the original `provider`, the `Settings` class that was given as a parameter to the `editSettings` function. This makes sense, because we want to edit the contents of this `Settings` type. 

So we have a keypath to `\Setting.profileSettings` and a keypath to `\ProfileSettings.displayName` and we want to retrieve the value at `\Setting.profileSettings.displayName`. We can use Swift's `KeyPath` composition!

``` Swift
func editSettings<Provider: SettingsProvider>(provider: Provider) {
  // All subsequent iterations happen here
  func updateSetting(keyPath: AnyKeyPath, title: String) {
    let value = provider[keyPath: keyPath]
    if let nestedProvider = value as? SettingsProvider {
      for item in nestedProvider.settings {
        // Join the keypaths
        if let joined = keyPath.appending(path: item.keyPath) {
          updateSetting(keyPath: joined, title: item.title)
        }
      }
    }
  }

  // The initial iteration
  for setting in provider.settingsEntries {
    updateSetting(keyPath: setting.keyPath, title: setting.title)
  }
}
```

In the code above, the magic happens in the following three lines:

``` Swift
if let joined = keyPath.appending(path: item.keyPath) {
  updateSetting(keyPath: joined, title: item.title)
}
```

We take the original `keyPath` that was given to the `updateSettings` function first (i.e. `\Setting.profileSettings`) and we take the `item.keyPath`, which is the keypath of the current item (i.e. `\ProfileSettings.displayName`) and join them to `\Setting.profileSettings.displayName`. Now we can use this `joined` keypath to retrieve the value of the `displayName` property of the `provider` instance and perform another iteration. By implementing it this way, we can easily support more nesting hierachies.

So what happens when our `value` isn't another nested `SettingsProvider` but an actual value such as `String` or `Bool` (`displayName` or `shareUpdates`). Since we want to be able to change the value that is stored here (from `false` to `true`) we do a run-time cast from this `keyPath` to a `WritableKeyPath` to figure out if we have an editable value.

``` Swift
if let writableKeypath = keyPath as? WritableKeyPath<???, ???> {
}
```

However, `WritableKeyPath` needs two types, the `Root` and the `Value`, what do we insert here? We don't know the type of the `Root` as we're iterating over `Settings`, `ProfileSettings`, `PrivacySettings`, etc, right? It could be anything. Actually, we do know the type of `Root`. Since our keypaths are joined (`\Settings.profileSettings.displayName`) our root is **always** `Settings`. So we could write `WritableKeyPath<Settings, ???>` but now our function would not be generic anymore. If we look at the header of our original function, though, we see something interesting:

``` Swift
func editSettings<Provider: SettingsProvider>(provider: Provider) {
...
```

We actually do have our root type, as the `Provider` generic type to the `editSettings` function. So we can just write `WritableKeyPath<Provider, ???>`. The second type of our `WritableKeyPath` is also easy. If we want to edit boolean flags, it is `Bool`, and if we want to edit `Strings` it is .. well, `String`. Lets type this out:

``` Swift
func editSettings<Provider: SettingsProvider>(provider: Provider) {
  // All subsequent iterations happen here
  func updateSetting(keyPath: AnyKeyPath, title: String) {
    let value = provider[keyPath: keyPath]
    if let nestedProvider = value as? SettingsProvider {
      for item in nestedProvider.settings {
        if let joined = keyPath.appending(path: item.keyPath) {
          updateSetting(keyPath: joined, title: item.title)
        }
      }
    } else if let writable = keyPath as? WritableKeyPath<Provider, Bool> {
      print(title)
      provider[keyPath: writable] = true
    }
  }

  // The initial iteration
  for setting in provider.settingsEntries {
    updateSetting(keyPath: setting.keyPath, title: setting.title)
  }
}
```

That's it! We cast the keypath to a writable variant, and then we can modify the contents of our `Settings` type (or nested types). Everything happens in these additional lines of code:

``` Swift
if let writable = keyPath as? WritableKeyPath<Provider, Bool> {
      print(title)
      provider[keyPath: writable] = true
    }
}
```

Subsequently, we could easily extend these lines to also query for `WritableKeyPath<Provider, String>` or `WritableKeyPath<Provider, Double>`, etc.

This is our final function. It allows us to handle app settings in a completely generic manner. It iterates over them, it can display them (we did not see that because the code size would have exploded), and it can edit them. Without ever knowing the actual shape of the settings type. It can also be used for structures other than settings. Any complex type can be iterated in this manner.

However, this was only a small example of what you can do with keypaths. There is even more! Lets have a look.
