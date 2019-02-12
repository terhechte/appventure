[frontMatter]
description = "this is a long long summary this is a long long summary this is a long long summary"
title = "Bit Operations in Swift"
tags = ["swift"]
created = "2015-09-01"
published = false
keywords = ["swift", "bit", "bitshift", "shift", "bits", "feature"]
slug = "2015-09-01-test-exports.html"
---

There\'s a huge difference between programming in C and programming in
Swift. The Swift compiler abstracts away a lot of the unsafe features of
C, such as direct memory access / manipulation. Additionally, the
advanced type system adds a lot of safety. In this regard, C is much
closer to the actual hardware than Swift. Structs are a nice example of
this. If you define a C struct, you know that the memory hardware layout
and padding is just as you defined it in your code. Not so with Swift
structs. There are, of course, ways around this such as `UnsafePointer`,
`unsafeDowncast`, or `withUnsafeMutablePointer`. Still, working closely
with the bits and bytes of the hardware is more complex than in C /
Objective-C.

``` {#feature-image .python exports="code" export-image="true"}
import os
for i in range(0, 10):
    print i
print ("done")
```

However, there is one area where Swift improves upon the C low level
workflow, and that is working with bits and bitfields.

# Bits and Bitfields

There\'re situations where the problem you\'re trying to solve requires
a list of boolean states.
