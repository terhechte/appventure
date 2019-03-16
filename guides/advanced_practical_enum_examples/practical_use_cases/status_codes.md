[frontMatter]
title = "Status Codes"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Status Codes

If you\'re working with an outside system which uses status codes (or
error codes) to convey information, like HTTP Status Codes, enums are
obviously a great way to encode the information. [^7]

``` Swift
enum HttpError: String {
  case code400 = "Bad Request"
  case code401 = "Unauthorized"
  case code402 = "Payment Required"
  case code403 = "Forbidden"
  case code404 = "Not Found"
}
```
