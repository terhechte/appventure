[frontMatter]
description = "A tutorial on how to create a Swift Package for X11 on Linux and use it to write a simple X11 app"
title = "Fast String Operations in Swift"
tags = ["swift", "ios", "mac"]
created = "2016-01-24"
published = false
keywords = ["swift", "string", "nsstring", "trim", "newlines", "split"]
slug = "2016-01-24-fast-string-operations-swift.html"
---

Strings in Swift and string operations in particular are a bit different
compared to the way strings are handled in Objective-C\`s `NSString`. By
now, most of `` NSString=`s operations, such as =enumerateLines `` are
also available directly on any `String`, but even then there is only
limited functionality available on the `String` type itself; instead,
you\'ll have to use one of the different character views that the string
type offers: `Characters`, `UTF8`, `UTF16`, and `UnicodeScalar`. Swift
offers excellent Unicode support, which means that all the complex
details of multibyte unicode codepoints are properly supported[^1]. I
don\'t want to go into detail here. [Ole
Begemann](https://twitter.com/olebegemann) did a really good job
explaining [the unicode details in terms of NSString
here.](https://www.objc.io/issues/9-strings/unicode/) In this article,
I\'d rather give a couple of hints on the common pitfalls when you need
to implement fast string code. The only required knowledge here is that
one visible character, in unicode, can be composed out of multiple
singular codepoints. I.e. the on-screen letter `é` can be composed out
of the `e` character and the `´`
[Diacritic](https://en.wikipedia.org/wiki/Diacritic). Here\'s a great
summary from [Ole
Begemann](http://oleb.net/blog/2014/07/swift-strings/):

> A Swift Character represents one perceived character (what a person
> thinks of as a single character, called a grapheme). Since Unicode
> often uses two or more code points (called a grapheme cluster) to form
> one perceived character, this implies that a Character can be composed
> of multiple Unicode scalar values if they form a single grapheme
> cluster. (Unicode scalar is the term for any Unicode code point except
> surrogate pair characters, which are used to encode UTF-16.)

# String Views

First, a short reminder of the different character views in Swift. A
much more detailed explanation [can be found in the Apple Swift
documentation](https://developer.apple.com/library/ios/documentation/Swift/Conceptual/Swift_Programming_Language/StringsAndCharacters.html#//apple_ref/doc/uid/TP40014097-CH7-ID290).

## `String.characters`

Individual Character values as Unicode extended grapheme clusters. This
view is similar to what a user would see on screen. If the visible
character is composed out of 5 code points, the `characters.count`
property would return 1 instead of 5.

## `String.utf8`

A collection of UTF-8 code units.

## `String.utf16`

A collection of UTF-16 code units. This is the same encoding as is used
by `NSString`.

## `String.unicodeScalars`

A collection of 21-bit Unicode scalar values, equivalent to the string's
UTF-32 encoding form.

## `NSString`

If you import `Foundation` you can also use NSString bridging to convert
a string into a NSString representation.

??figure out if this is indeed an expensive operation?? ??write more
tests to see in which situations is which behaviour the fastest.

-   \[ \] with objective-c, for pure speed, you could just write the
    algorithm in C

``` {.c org-language="C"}
// http://codereview.stackexchange.com/questions/20897/trim-function-in-c
  void trim(char *input) {
     char *dst = input, *src = input;
     char *end;

     // Skip whitespace at front...
     while (isspace((unsigned char)*src)) {
        ++src;
     }

     // Trim at end
     end = src + strlen(src) - 1;
     while (end > src && isspace((unsigned char)*end)) {
        *end-- = 0;
     }

     // Move if needed.
     if (src != dst) {
        while ((*dst++ = *src++));
     }
  }
```

-   \[ \] theres characters, utf8, unicodescalar, utf16, and string.
-   \[ \] speed differences
-   \[ \] however, there\'s also the ~core~, which are low level
    operations and can be accessed via some functions (on string?,
    research this): quote:
    <https://github.com/apple/swift/blob/8917eb0e5ac50e424800bac8a57266a1cd945ab1/stdlib/public/core/String.swift>
    // FIXME(performance): this code assumes UTF-16 in-memory
    representation. // It should be switched to low-level APIs.

-   \[ \] using nsstring methods:

*/* \`String\` is bridged to Objective-C as \`NSString\`, and a
\`String\` */* that originated in Objective-C may store its characters
in an */* \`NSString\`. Since any arbitrary subclass of \`NSString\` can
*/* become a \`String\`, there are no guarantees about representation or
*/* efficiency in this case. Since \`NSString\` is immutable, it is */*
just as though the storage was shared by some copy: the first in */* any
sequence of mutating operations causes elements to be copied */* into
unique, contiguous storage which may cost \`O(N)\` time and */* space,
where \`N\` is the length of the string representation (or */* more, if
the underlying \`NSString\` has unusual performance
<https://github.com/apple/swift/blob/8917eb0e5ac50e424800bac8a57266a1cd945ab1/stdlib/public/core/String.swift>

StringCore // Implementation note: We try hard to avoid branches in this
code, so // for example we use integer math to avoid switching on the
element // size with the ternary operator. This is also the cause of the
// extra element requirement for 8 bit elements. See the

[^1]: `NSString`, in contrast, has issues here, i.e. the combination of
    codepoints `e + ´` to generate the letter `é` will result in an
    `NSString` of length 2, instead of length 1
