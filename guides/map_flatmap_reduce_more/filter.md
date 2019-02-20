[frontMatter]
title = "Filter"
tags = []
created = "2019-02-20 19:49:10"
description = ""
published = false

---

# Filter

``` Swift
func rFilter(elements: [Int], filter: (Int) -> Bool) -> [Int] {
    return elements.reduce([Int](), 
       combine: { guard filter($1) else { return $0 } 
                  return $0 + [$1]})
}
print(rFilter([1, 3, 4, 6], filter: { $0 % 2 == 0}))
// [4, 6]
```

Again, a simple operation. We\'re leveraging guard again to make sure
our filter condition holds.

Up until now, `reduce` may feel like a more complicated version of `map`
or `filter` without any major advantages. However, the combinator does
not need to be an array. It can be anything. This makes it easy for us
to implement various reduction operations in a very simple way.
