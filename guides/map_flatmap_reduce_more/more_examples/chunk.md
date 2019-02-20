[frontMatter]
title = "Chunk"
tags = []
created = "2019-02-20 19:49:10"
description = ""
published = false

---

# Chunk

This function returns self, broken up into non-overlapping arrays of
length `n`:

``` Swift
func chunk<T>(list: [T], length: Int) -> [[T]] {
   typealias Acc = (stack: [[T]], cur: [T], cnt: Int)
   let l = list.reduce((stack: [], cur: [], cnt: 0), combine: { (ac: Acc, o: T) -> Acc in
      if ac.cnt == length {
          return (stack: ac.stack + [ac.cur], cur: [o], cnt: 1)
      } else {
          return (stack: ac.stack, cur: ac.cur + [o], cnt: ac.cnt + 1)
      }
   })
   return l.stack + [l.cur]
}
print(chunk([1, 2, 3, 4, 5, 6, 7], length: 2))
// : [[1, 2], [3, 4], [5, 6], [7]]
```

This function uses a more complicated `accumulator` consisting out of a
stack, the current list, and the count.
