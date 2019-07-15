[frontMatter]
title = "How do I implement a Preferences Toolbar like in the Podcast App?"
tags = ["catalyst", "macos", "uikitformac", "toolbar", "preferences"]
created = "2019-07-09"
description = ""
published = true

[meta]
swift_version = "5.1"
---

If you start one of Apple's prime Catalyst examples, the *Podcast App*, you will see this beautiful Preferences screen:

![](/img-content/catalyst/settings1.png)

As you already know, Preferences in Catalyst apps are handled via the [Settings.bundle](rel::firststeps/preferences.md) technology. However, one feature that is very much missing from Apples documentation is how to implement the toolbars and toolbar icons at the top of the window (General, Playback, Advanced) via the `Settings.bundle`. In this guide, we will explain how it works.

# How to implement the Preferences toolbar

In addition to the regular settings bundle (with `Root.plist`), you need to add a couple of additional files first.

- A new `.plist` file for each section
- Two new icons for each section, the `@1x` and the `@2x` variant

In our example, we will have two sections: `General`, and `Advanced`. So we need to `.plist` files, `Root` (for general) and `Advanced` for ... advanced. As well as corresponding images. It looks as follows:

![](/img-content/catalyst/settings_toolbar.png)

Next, we need to explain to the system that it should display two `Panes` in the toolbar. We do that by adding an additional section to the `Root.plist` that lists all the `Pane` sections:

``` plist
<key>PreferenceSpecifiers</key>
<array>
	...
	<dict>
		<key>Type</key>
		<string>PSChildPaneSpecifier</string>
		<key>Title</key>
		<string>Advanced</string>
		<key>File</key>
		<string>Advanced</string>
	</dict> 
</array>
```

So here we're adding a new Settings Entry, if you will, to the `Root` plist that tells the system to add a new `Child Pane` into the toolbar with the title `Advanced` and from the file `Advanced.plist`.

If we wanted to add more panes, we would add more of those `<dict>` entries.

This is how we add multiple panes, but it still doesn't explain how to add our beloved icons to the pane. For that, we add a final additional entry at the bottom of each `.plist`. file (i.e. Root and Advanced) with a `key` and a `string` value:


## In Root.plist
``` plist
<key>Icon</key>                                                                                 
<string>PreferencesGeneralButton</string>        
```

## In Advanced.plist
``` plist
<key>Icon</key>                                                                                 
<string>PreferencesAdvancedButton</string>        
```

This is sufficient to give us a nice Preferences screen:

![](/img-content/catalyst/settings_toolbar2.png)

# The final PLIST files

Here're the full `.plist` files for you.

## Root

``` plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>StringsTable</key>
	<string>Root</string>
	<key>PreferenceSpecifiers</key>
	<array>
		<dict>
			<key>Type</key>
			<string>PSToggleSwitchSpecifier</string>
			<key>Title</key>
			<string>Enabled</string>
			<key>Key</key>
			<string>enabled_another_preference</string>
			<key>DefaultValue</key>
			<true/>
		</dict>
		<dict>
			<key>Type</key>
			<string>PSChildPaneSpecifier</string>
			<key>Title</key>
			<string>Advanced</string>
			<key>File</key>
			<string>Advanced</string>
		</dict> 
	</array>
	<key>Icon</key>                                                                                 
        <string>PreferencesGeneralButton</string>        
</dict>
</plist>
```

## Advanced
``` plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>StringsTable</key>
	<string>Root</string>
	<key>PreferenceSpecifiers</key>
	<array>
		<dict>
			<key>Type</key>
			<string>PSToggleSwitchSpecifier</string>
			<key>Title</key>
			<string>Enable Export</string>
			<key>Key</key>
			<string>enabled_preference</string>
			<key>DefaultValue</key>
			<true/>
		</dict>
	</array>
	<key>Icon</key>
	<string>PreferencesAdvancedButton</string>
</dict>
</plist>
```

That should be it.
