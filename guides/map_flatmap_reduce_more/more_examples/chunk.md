[frontMatter]
title = "Chunk"
tags = ["map", "compactMap", "filter", "reduce"]
created = "2019-02-20 19:49:10"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Chunk

This function returns self, broken up into non-overlapping arrays of
length `n`:

``` Swift
func chunk<T>(_ list: [T], length: Int) -> [[T]] {
   // Simplify the type signature by introducing a `typealias`
   typealias Acc = (stack: [[T]], cur: [T], cnt: Int)
   
   // Start with a `cnt` of 0
   let reducedList = list.reduce((stack: [], cur: [], cnt: 0), { (ac: Acc, o: T) -> Acc in
      if ac.cnt == length {
          return (stack: ac.stack + [ac.cur], cur: [o], cnt: 1)
      } else {
          return (stack: ac.stack, cur: ac.cur + [o], cnt: ac.cnt + 1)
      }
   })
   return reducedList.stack + [reducedList.cur]
}
print(chunk([1, 2, 3, 4, 5, 6, 7], length: 2))
// [[1, 2], [3, 4], [5, 6], [7]]
```

This function uses a more complicated `accumulator` consisting out of a
stack, the current list, and the count.
