[frontMatter]
title = "Interdig"
tags = []
created = "2019-02-20 19:49:10"
description = ""
published = false

---

# Interdig

This function allows you to combine two sequences by alternately
selecting elements from each.

``` Swift
func interdig<T>(list1: [T], list2: [T]) -> [T] {
   return Zip2Sequence(list1, list2).reduce([], combine: { (ac: [T], o: (T, T)) -> [T] in 
        return ac + [o.0, o.1]
   })
}
print(interdig([1, 3, 5], list2: [2, 4, 6]))
// : [1, 2, 3, 4, 5, 6]
```
