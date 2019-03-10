[frontMatter]
title = "Result Types"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Result Types

Enums are also frequently used to map the result of JSON parsing into
the Swift type system. Here\'s a short example of this:

``` Swift
enum JSON {
    case JSONString(Swift.String)
    case JSONNumber(Double)
    case JSONObject([String : JSONValue])
    case JSONArray([JSONValue])
    case JSONBool(Bool)
    case JSONNull
}
```

Similarly, if you\'re parsing something else, you may use the very same
structure to convert your parsing results into Swift types. This also
makes perfect sense to only do it during the parsing / processing step
and then taking the `JSON enum` representation and converting it into
one of your application\'s internal `class` or `struct` types.
