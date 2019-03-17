[frontMatter]
title = "Word Frequencies"
tags = ["pattern matching", "switch", "compactMap", "map", "filter"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Word Frequencies

We have a sequence of pairs, each representing a word and its frequency
in some text. Our goal is to filter out those pairs whose frequency is
below or above a certain threshold, and then only return the remaining
words, without their respective frequencies.

Here\'re our words:

``` Swift
let wordFreqs = [("k", 5), ("a", 7), ("b", 3)]
```

A simple solution would be to model this with [`map` and `filter`](lnk::map-filter-reduce):

``` Swift
let res = wordFreqs.filter({ (e) -> Bool in
    if e.1 > 3 {
        return true
    } else {
        return false
    }
}).map { $0.0 }
print(res)
```

However, with `compactMap` a map that only returns the non-nil elements, we
can improve a lot upon this solution. First and foremost, we can get rid
of the `e.1` and instead have proper destructuring by utilizing (you
guessed it) tuples. And then, we only need one call `compactMap` instead of
`filter` and then `map` which adds unnecessary performance overhead.

``` Swift
let res = wordFreqs.compactMap { (e) -> String? in
    switch e {
    case let (s, t) where t > 3: return s
    default: return nil
    }
}
print(res)
```
