[frontMatter]
description = "FIXME FIXME FIXME"
title = "Debugging entitlement issues in Maps, iCloud, In-App, Keychain, or GameCenter"
created = "2014-01-21"
published = true
keywords = ["ios", "cocoa", "entitlements"]
slug = "2014-01-21-debugging-entitlement-maps-icloud-gamecenter-issues.html"
tags = ["ios", "cocoa"]
---

I recently ran into an issue where a Mac App did lack an entitlement
even though I had all entitlements properly set up in my account. I also
had performed rigourous testing prior to submission, which made it even
more worrisome as I had no idea how to proceed.

Since everything was running fine on my machine, and since the error in
question was happening when users installed the app, I needed a way to
figure out what happened to the binary right before Xcode submits it to
the App Store.

If you happen to have such an issue, i.e. an Apple Maps or iCloud or
Game Center or Keychain Sharing or In-App Purchase error that only
happens on your customers system, there is indeed a way to debug this
issue.

[In Technical Note TN2265, Troubleshooting Push
Notifications](https://developer.apple.com/library/mac/technotes/tn2265/_index.html),
Apple explains a very useful process that explains what to do in such
situations as outlined above. In the \'**Error Delegate Callback**\'
section, the document explains how you can export the App from the
Organizer just as it would be submitted to the App Store, and how you
can inspect the result in order to figure out whether all the correct
entitlements are set:

1.  Export the app as Mac Installer Package, using the same identity
    that you use when submitting to the Mac App Store
2.  Locate the generated Pkg file in the Terminal
3.  Run the following code in the Terminal

``` bash
pkgutil --expand "YourApp.pkg" Expanded_pkg
open Expanded_pkg/com.yourcompany.yourapp/Payload
codesign -d --entitlements - "Expanded_pkg/com.yourcompany.yourapp/YourApp.app"
```

This will show you the list of entitlements that are included in your
app upon submission to the App Store. This is a very useful thing to
know, in fact so useful, that Apple writes, right below the process.

> Note: This is a useful test to perform on your distribution builds
> before submitting them to the App Store.

Absolutely, it would also be great if such a Gem wasn\'t hidden in a
page that just deals with Push Notification issues.
