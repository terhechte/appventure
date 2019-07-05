[frontMatter]
title = "What are some issues that I will run into?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# What are some issues that I will run into?

- The bundle identifier for the macOS version of your app is different. If you use bundle identifiers for something specific, be aware of this
- KeyChain sharing differs briefly, [as outlined by Apple here](https://developer.apple.com/documentation/security/keychain_services/keychain_items/sharing_access_to_keychain_items_among_a_collection_of_apps) (search for "macOS" on that page)
- Custom multitouch behaviour can't be automated. Views have to be udpated for that
- Your app will not be killed if it consumes too much memory. The system will just swap

With Catalyst, you should use the newever versions of these old, deprecated, frameworks:

- AddressBook -> Contacts
- AddressBookUI -> ContactsUI
- AssetsLibrary -> Photos
- OpenGL ES -> Metal
- GLKit -> MetalKit
- UIWebView -> WKWebView
