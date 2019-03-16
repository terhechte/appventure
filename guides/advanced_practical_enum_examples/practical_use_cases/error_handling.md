[frontMatter]
title = "Error Handling"
tags = ["error"]
created = "2019-03-01 16:31:41"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Error Handling

One of the prime examples of Enum usage in Swift is, of course, the new
error handling in Swift 2.0. Your throwing function can throw anything
which conforms to the empty `ErrorType` protocol. As the Swift
documentation succinctly observes:

> Swift enumerations are particularly well suited to modeling a group of
> related error conditions, with associated values allowing for
> additional information about the nature of an error to be
> communicated.

As an example, have a look at the popular [JSON Decoding library
Argo](https://github.com/thoughtbot/Argo). When their JSON Decoding
fails, it can fail due to two primary reasons.

1.  The JSON Data lacks a key which the end model requires (say your
    model has a property `username` and somehow the JSON lacks that)
2.  There\'s a type mismatch. Say instead of a String the `username`
    property in the JSON contains an `NSNull` [^6].

In addition to that, Argo also includes a custom error for anything not
fitting in these two categories above. Their `ErrorType enum` looks like
this:

``` Swift
enum DecodeError: Error {
  case typeMismatch(expected: String, actual: String)
  case missingKey(String)
  case custom(String)
}
```

All cases have associated values that contain additional information
about the error in question.

A more general `ErrorType` for complete HTTP / REST API handling could
look like this:

``` Swift
enum APIError : Error {
    // Can't connect to the server (maybe offline?)
    case connectionError(error: NSError)
    // The server responded with a non 200 status code
    case serverError(statusCode: Int, error: NSError)
    // We got no data (0 bytes) back from the server
    case noDataError
    // The server response can't be converted from JSON to a Dictionary
    case JSONSerializationError(error: Error)
    // The Argo decoding Failed
    case JSONMappingError(converstionError: DecodeError)
}
```

This `ErrorType` implements the complete REST Stack up to the point
where your app would get the completely decoded native `struct` or
`class` object.

More information on `ErrorType` and more `enum` examples in this context
can be found in the official documentation
[here](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/ErrorHandling.html).
