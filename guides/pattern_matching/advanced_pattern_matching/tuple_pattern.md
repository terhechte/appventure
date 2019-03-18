[frontMatter]
title = "Tuple Pattern"
tags = ["pattern matching", "switch", "tuple"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Tuple Pattern

[We have a full article on tuples](lnk::tuple), but here is a quick overview:

``` Swift
let age = 23
let job: String? = "Operator"
let payload: Any = NSDictionary()

switch (age, job, payload) {
case (let age, _?, _ as NSDictionary):
    print(age)
default: ()
}
```

Here, we\'re combining three values into a tuple (imagine they\'re
coming from different API calls) and matching them in one go. Note that
the pattern achieves three things:

1.  It extracts the age
2.  It makes sure there is a job, even though we don\'t need it
3.  It makes sure that the payload is of kind `NSDictionary` even though
    we don\'t need the actual value either.
