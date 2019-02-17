[frontMatter]
title = "Type Matches"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Type Matches

Given Swift\'s strong type system, there\'s usually no need for runtime
type checks like it more often happens in Objective-C. However, when you
interact with legacy Objective-C code [(which hasn\'t been updated to
reflect simple generics
yet)](https://netguru.co/blog/objective-c-generics), then you often end
up with code that needs to check for types. Imagine getting an array of
NSStrings and NSNumbers:

``` Swift
let u = NSArray(array: [NSString(string: "String1"), NSNumber(int: 20), NSNumber(int: 40)])
```

When you go through this NSArray, you never know what kind of type you
get. However, `switch` statements allow you to easily test for types
here:

``` Swift
for x in u {
    switch x {
    case _ as NSString:
        print("string")
    case _ as NSNumber:
        print("number")
    default:
        print("Unknown types")
    }
}
```
