[frontMatter]
title = "Conclusion"
tags = ["box", "associated"]
created = "2019-03-01 11:01:50"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Conclusion

`Associated types` are a powerful concept however they come with a fair
share of difficulties. Most notably, as soon as you introduce an
`associated type` you can\'t use it like you\'d use normal full types.
This article provided several patterns that make it a bit easier to
handle `associated type` problems in your codebase. Each of these
patterns has downsides though. In general, if you intend to use
`associated types` in a `protocol`, one of the best solutions is to try
to only use the types that implement this `protocol` instead of the
`protocol` itself. Because then you don\'t even need those patterns.
