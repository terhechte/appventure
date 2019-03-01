[frontMatter]
title = "Status Codes"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

---

# Status Codes

If you\'re working with an outside system which uses status codes (or
error codes) to convey information, like HTTP Status Codes, enums are
obviously a great way to encode the information. [^7]

``` Swift
enum HttpError: String {
  case Code400 = "Bad Request"
  case Code401 = "Unauthorized"
  case Code402 = "Payment Required"
  case Code403 = "Forbidden"
  case Code404 = "Not Found"
}
```
