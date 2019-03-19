[frontMatter]
title = "Group By"
tags = ["map", "compactMap", "filter", "reduce", "groupby"]
created = "2019-02-20 19:49:10"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Group By

Go over a list and return a new list with the previous list\' items
grouped by a discriminator function. The function in question needs to
return a `Hashable` type so that we can differentiate keys. The order of
the items will be preserved while the order of the groups won\'t
necessarily be preserved.

``` Swift
func groupby<T, H: Hashable>(_ items: [T], f: (T) -> H) -> [H: [T]] {
   return items.reduce([:], { (var ac: [H: [T]], o: T) -> [H: [T]] in 
       let h = f(o)
       if var c = ac[h] {
           c.append(o)
           ac.updateValue(c, forKey: h)
       } else {
           ac.updateValue([o], forKey: h)
       }
       return ac
   })
}
print(groupby([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], f: { $0 % 3 }))
// prints: [2: [2, 5, 8, 11], 0: [3, 6, 9, 12], 1: [1, 4, 7, 10]]
print(groupby(["Carl", "Cozy", "Bethlehem", "Belem", "Brand", "Zara"], f: { $0.characters.first! }))
// prints: ["C" : ["Carl" , "Cozy"] , "B" : ["Bethlehem" , "Belem" , "Brand"] , "Z" : ["Zara"]]
```
