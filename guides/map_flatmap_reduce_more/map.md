[frontMatter]
title = "Map"
tags = []
created = "2019-02-20 19:49:10"
description = ""
published = false

---

# Map

``` Swift
func rmap(elements: [Int], transform: (Int) -> Int) -> [Int] {
    return elements.reduce([Int](), combine: { (var acc: [Int], obj: Int) -> [Int] in
       acc.append(transform(obj))
       return acc
    })
}
print(rmap([1, 2, 3, 4], transform: { $0 * 2}))
// [2, 4, 6, 8]
```

This is a good example to understand the basics of `reduce`.

-   First, we\'re calling reduce on a sequence of elements
    `elements.reduce...`.
-   Next, We\'re giving it the accumulator, i.e. an empty Int array,
    which will form or return type / result `[Int]()`
-   After that, we\'re handing in the `combinator` which takes two
    parameters. The first is the accumulator which we just provided
    `acc: [Int]`, the second is the current object from our sequence
    `obj: Int`.
-   The actual code in the `combinator` is simple. We simply transform
    the obj and append it onto the accumulator. We then return the
    accumulator.

This looks like much more code than just calling `map`. That\'s indeed
true, but the version above is extra detailed in order to better explain
how `reduce` works. We can simplify it.

``` Swift
func rmap(elements: [Int], transform: (Int) -> Int) -> [Int] {
    return elements.reduce([Int](), combine: {$0 + [transform($1)]})
}
print(rmap([1, 2, 3, 4], transform: { $0 * 2}))
// [2, 4, 6, 8]
```

This still works fine. What happened here? We\'re using the convenient
fact that in Swift, the `+` operator also works for two sequences. So
`[0, 1, 2] + [transform(4)]` takes the left sequence and adds the right
sequence, consisting out of the transformed element, to it.

It should be noted that, as of right now, `[1, 2, 3] + [4]` is slower
than `[1, 2, 3].append(4)`. If you operate on huge lists, instead of
using collection + collection, you should have a mutable accumulator and
mutate it in place:

``` Swift
func rmap(elements: [Int], transform: (Int) -> Int) -> [Int] {
    return elements.reduce([Int](), combine: { (var ac: [Int], b: Int) -> [Int] in 
        ac.append(transform(b))
        return ac
    })
}
```

In order to better understand `reduce` we will now go on and also
implement `flatMap` and `filter`.

``` Swift
func rflatMap(elements: [Int], transform: (Int) -> Int?) -> [Int] {
    return elements.reduce([Int](), 
       combine: { guard let m = transform($1) else { return $0 } 
                  return $0 + [m]})
}
print(rflatMap([1, 3, 4], transform: { guard $0 != 3 else { return nil }; return $0 * 2}))
// [2, 8]
```

The main difference is that we\'re adding a `guard` to make sure the
optional contains a value.
