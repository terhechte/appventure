[frontMatter]
title = "API Endpoints"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

---

# API Endpoints

Rest APIs are a great use case for enums. They\'re naturally grouped,
they\'re limited to a finite set of APIs, and they may have additional
query or named parameters which can be modelled through associated
values.

Take, for example, a look at a simplified version of the [**Instagram
API**](https://instagram.com/developer/endpoints/media/)

``` Swift
enum Instagram {
  enum Media {
    case Popular
    case Shortcode(id: String)
    case Search(lat: Float, min_timestamp: Int, lng: Float, max_timestamp: Int, distance: Int)
  }
  enum Users {
    case User(id: String)
    case Feed
    case Recent(id: String)
  }
}
```

[Ash Furrow\'s **Moya** library](https://github.com/Moya/Moya) is based
around this idea of using `enums` to map rest endpoints.
