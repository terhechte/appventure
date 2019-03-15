[frontMatter]
description = "This quickly explains how you use private apis from Swift in order to figure out the manufacturer of your fancy new iPhone 6S CPU"
title = "Getting your iPhone 6s Chip Foundry from Swift"
created = "2015-09-30"
published = true
keywords = ["swift", "iphone6s", "iphone", "tsmc", "samsung", "gestalt", "private", "api", "foundation"]
slug = "2015-09-30-getting-iphone6s-foundry-from-swift.html"
tags = []
category = ["Hands On", "All"]

[meta]
swift_version = "2.3"
---

[Here\'s a small Github project by
WUD](https://github.com/WDUK/A9ChipSource) which uses the private
[libMobileGestalt](https://gist.github.com/Cykey/5216992) to identify
the manufacturer of the CPU in your fancy new iPhone 6S. Because, as you
may not know, this year Apple is sourcing the chips from two different
foundries: Samsung and TSMC. So which one did you get? You could, of
course, just run the aforementioned GitHub project on your phone.
However, that\'s all Objective-C and out of curiosity I wondered: How
would you pull that off in Swift?

# Step One: Adding a header

The first obstacle is already a tricky one. `LibMobileGestalt` doesn\'t
offer a header as it is a private library. So how do you tell Swift /
the linker that the function you want to call will indeed exist at
compile time. At first glance it seems that pure Swift doesn\'t offer
any facilities for this (if you\'re impatient, there\'s another solution
below ;-), so we can always resort back to the [Bridging
Header](https://developer.apple.com/library/ios/documentation/Swift/Conceptual/BuildingCocoaApps/MixandMatch.html)
that Apple introduced to easily bridge the Swift and the Objective-C/C
worlds. [Here
is](https://bohemianpolymorph.wordpress.com/2014/07/11/manually-adding-a-swift-bridging-header/)
a short guide on how to add a bridging header to your project. Basically
add a new header file, and add the path to your target\'s Build Settings
under `Objective-C Bridging Header`.

Then, add the following code to your header:

``` C
#if __cplusplus
extern "C" {
#endif
    CFPropertyListRef MGCopyAnswer(CFStringRef property);
#if __cplusplus
}
#endif
```

But what if you\'re writing a pure Swift project and don\'t want to add
a bridging header? There\'s a mostly undocumented ([Thanks to someone on
HN for pointing it out to
me](https://news.ycombinator.com/item?id%3D10305664)) Swift attribute
called `@asmname` that allows us to do something similar straight in
Swift. [Russ Bishop has a post on this and much more you can do in this
realm.](http://www.russbishop.net/swift-don-t-do-this)

Using the `@asmname` keyword, the code looks like this (and you can
remove the bridging header):

``` Swift
@asmname("MGCopyAnswer")
func MGCopyAnswer(_: CFStringRef) -> Optional<Unmanaged<CFPropertyListRef>>;
```

We\'re basically telling Swift that this function exists, and we\'re
telling it specifically what it requires and what it will return.

# Step Two: Writing Swift

Next up, we want to write the Swift code to call this function, so
let\'s do it:

``` Swift
chipInfo = MGCopyAnswer("HardwarePlatform")
```

We might expect that the result of this is already the required
`String`, but Swift is a safe language so first of all it is returning
an `Optional` here, since the key in question (\"HardwarePlatform\")
might not even exist. We first have to get the value out. To do that,
we\'ll use the new Swift 2 `guard` statement.

``` Swift
guard let chipInfo = MGCopyAnswer("HardwarePlatform")
    else { fatalError("Could not read hardware") }
```

If we look at the type of `chipInfo`, sadly, we still don\'t have a
`String`. Instead, we\'re getting `Unmanaged<CFPropertyList>`. What\'s
that?

The Apple Documentation has this to say about `Unmanaged`:

> A type for propagating an unmanaged object reference.
>
> When you use this type, you become partially responsible for keeping
> the object alive.

Of course, we\'re getting a value from the Core Foundation world where
ARC does not know how to manage the memory. Objective-C uses the
`__bridge` keyword to manage this, and in Swift it smartly changes the
type so that we definitely don\'t forget that this variable\'s memory is
currently not managed. [NSHipster](http://nshipster.com/unmanaged/), and
[Apple](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Reference/Swift_Unmanaged_Structure/index.html)
have more documentation for this. What we\'ll do is call the
`takeRetainedValue` method:

``` Swift
guard let chipInfo = MGCopyAnswer("HardwarePlatform")
    else { fatalError("Could not read hardware") }
chipInfo.takeRetainedValue()
```

So, do we finally have a String? No, but we\'re close. We\'re getting a
`CFPropertyList` object back. The Apple Documentation has this to say
about this type:

> CFPropertyListRef can be a reference to any of the property list
> objects: CFData, CFString, CFArray, CFDictionary, CFDate, CFBoolean,
> and CFNumber.

This means that if the result is indeed of type `CFString`, since
`CFString` is toll-free-bridged to `NSString` and since `NSString` is
bridged to Swift\'s `String`, we could just force cast this to the
`String` type and be done with it. Swift is a safe language however, and
when possible we should strive to do everything the safe way. So instead
we\'ll do an optional cast to String and if that works out, we can get
the actual String value out of the `Optional`.

If we do it this way, it will not blow up whtn the contents of the
reference are, say, a `CFDate` or a `CFBoolean`. This is particularly
easy with [Swift\'s Pattern Matching
syntax](http://appventure.me/2015/08/20/swift-pattern-matching-in-detail/):

``` Swift
guard let chipInfo = MGCopyAnswer("HardwarePlatform")
    else { fatalError("Could not read hardware") }

switch chipInfo.takeRetainedValue() as? String {
case "s8000"?:
    print("Samsung")
case "s8003"?:
    print("TSMC")
default:
    print("Unknown")
}
```

The question mark at the end of the two codes **(\"s8000\"?)** signifies
that we\'re not matching against a `String`, but against an
`Optional<String>`.

# Step Three: Add the Framework

There we are. Awesome it works. Except, it doesn\'t. You still have to
add the `libMobileGestalt.tbd` library and the `Core Foundation`
framework to your project target\'s `Linked Frameworks and Libraries`.

I\'ve [also created a small GitHub project that includes all
this](https://github.com/terhechte/SwiftiPhone6sChipFinder) including
the correct library setup etc.
