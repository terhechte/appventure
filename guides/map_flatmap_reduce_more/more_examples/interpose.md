[frontMatter]
title = "Interpose"
tags = []
created = "2019-02-20 19:49:10"
description = ""
published = false

---

# Interpose

This function returns the given `items`, with `element` inserted between
every `count` items. The implementation below makes sure that the
elements are only interposed and not appended at the end.

``` Swift
func interpose<T>(items: [T], element: T, count: Int = 1) -> [T] {
   typealias Acc = (ac: [T], cur: Int, cnt: Int)
   return items.reduce((ac: [], cur: 0, cnt: 1), combine: { (a: Acc, o: T) -> Acc in 
       switch a {
          // the last item will not have any interposition
          case let (ac, cur, _) where (cur+1) == items.count: return (ac + [o], 0, 0)
          // interpose
          case let (ac, cur, c) where c == count:
             return (ac + [o, element], cur + 1, 1)
          // next
          case let (ac, cur, c):
             return (ac + [o], cur + 1, c + 1)
       }
   }).ac
}
print(interpose([1, 2, 3, 4, 5], element: 9))
// : [1, 9, 2, 9, 3, 9, 4, 9, 5]
print(interpose([1, 2, 3, 4, 5], element: 9, count: 2))
// : [1, 2, 9, 3, 4, 9, 5]
```
