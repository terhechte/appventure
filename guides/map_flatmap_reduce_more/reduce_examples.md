[frontMatter]
title = "Reduce Examples"
tags = ["reduce", "partition"]
created = "2019-02-20 19:49:10"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Reduce Examples

Let\'s start with a favorite of mine, the sum of a list of numbers:

``` Swift
[0, 1, 2, 3, 4].reduce(0, +)
// 10
```

`+` is a valid `combinator` function as it will just add the `lhs` and
the `rhs` and return the result, which is specifically the requirement
`reduce` has.

Another example is building the product of a list of numbers:

``` Swift
[1, 2, 3, 4].reduce(1, *)
// 24
```

Or what about reversing a list:

``` Swift
[1, 2, 3, 4, 5].reduce([Int](), { [$1] + $0 })
// 5, 4, 3, 2, 1
```

Finally, something a tad more complicated. We\'d like to partition a
list based on a division criteria

``` Swift
typealias Acc = (l: [Int], r: [Int])
func partition(_ lst: [Int], criteria: (Int) -> Bool) -> Acc {
   return lst.reduce((l: [Int](), r: [Int]()), { (ac: Acc, o: Int) -> Acc in 
      if criteria(o) {
        return (l: ac.l + [o], r: ac.r)
      } else {
        return (r: ac.r + [o], l: ac.l)
      }
   })
}
partition([1, 2, 3, 4, 5, 6, 7, 8, 9], criteria: { $0 % 2 == 0 })
//: ([2, 4, 6, 8], [1, 3, 5, 7, 9])
```

The most interesting thing we\'re doing above is using a `tuple` as the
accumulator. As you\'ll find out, once you start trying to incorporate
`reduce` into your daily work-flow, `tuples` are a great way of quickly
combining related data during a reduce operation.
