[frontMatter]
title = "Directory Traversion"
tags = ["pattern matching", "switch", "where"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Directory Traversion

Imagine you want to traverse a file hierachy and find:

-   all \"psd\" files from customer1 and customer2
-   all \"blend\" files from customer2
-   all \"jpeg\" files from all customers.

``` Swift
guard let enumerator = FileManager.default.enumeratorAtPath("/customers/2014/")
    else { return }

for url in enumerator {
    switch (url.pathComponents, url.pathExtension) {

    // psd files from customer1, customer2
    case (let f, "psd") 
            where f.contains("customer1") || f.contains("customer2"): print(url)

    // blend files from customer2
    case (let f, "blend") 
            where f.contains("customer2"): print(url)

    // all jpg files
    case (_, "jpg"): print(url)

    default: ()
    }
}
```

Note that `contains` stops at the first match and doesn\'t traverse the
complete path. Again, pattern matching lead to very succinct and
readable code.
