[frontMatter]
description = "An introduction into the reduce function as an alternative to map, flatMap or filter for collection transformation"
title = "Reduce all the things"
created = "2015-11-30"
published = true
keywords = ["feature", "swift", "reduce", "map", "filter", "group", "partition", "split", "interpose", "chunk", "functional", "programming", "flatMap"]
slug = "2015-11-30-reduce-all-the-things.html"
tags = ["swift", "cocoa", "ios"]
---

<h6><a href="http://swift.gg/2015/12/10/reduce-all-the-things/">This post is also available in <b>🇨🇳Chinese</b></a><span> Thanks to </span><a href="http://swift.gg/tags/APPVENTURE/">SwiftGG</a></h6>

Even before Swift was released, iOS / Cocoa developers could use third
party frameworks like ObjectiveSugar or ReactiveCocoa in order to gain
functional programming constructs like `map`, `flatMap` or `filter`.
With Swift, they have become first class language citizens. There are
many advantages to using them over a standard `for` loop. They typically
express your intent better, they require less code, and they can be
chained together in order to build up complex logic in a clear way.

In this post, I\'d like to show another very cool functional addition to
Swift which can sometimes be a better solution than `map` / `filter`
constructs: `reduce`.

# A simple Problem

Consider this problem: You\'re getting a list of persons from a JSON
endpoint. You\'d like to know the average age from all people living in
California. The parsed data looks like this:

``` Swift
let persons: [[String: AnyObject]] = [["name": "Carl Saxon", "city": "New York, NY", "age": 44],
 ["name": "Travis Downing", "city": "El Segundo, CA", "age": 34],
 ["name": "Liz Parker", "city": "San Francisco, CA", "age": 32],
 ["name": "John Newden", "city": "New Jersey, NY", "age": 21],
 ["name": "Hector Simons", "city": "San Diego, CA", "age": 37],
 ["name": "Brian Neo", "age": 27]]
```

Note the last entry, which omits a `city` for the person in question.
Those cases have to be silently ignored.

The expected result in the example would be 3 persons , as we have three
persons from California. Let\'s try to implement this in Swift in terms
of `flatMap` and `filter`. The `flatMap` is used instead of `map` as
`flatMap` automatically ignores empty optionals. So
`flatMap([0, nil, 1, 2, nil])` results in `[0, 1, 2]`. This eases the
handling of persons without a proper city.

``` Swift
func infoFromState(state state: String, persons: [[String: AnyObject]]) 
     -> Int {
    return persons.flatMap( { $0["city"]?.componentsSeparatedByString(", ").last })
           .filter({$0 == state})
           .count
}
infoFromState(state: "CA", persons: persons)
//#+RESULTS:
//: 3
```

That\'s simple enough.

However, now consider the following complication: You\'d like to know
how many of those persons live in California, and you\'d like to know
their average age. If we try upgrading the above example, we soon
realize that his is a slightly harder problem. There are various
solutions, but they all seem to not fit well with functional constructs.
A loop-based approach feels much simpler.

When we think about why this does fit, we realize it is because the
shape of the data changes. `map`, `flatMap`, and `filter` all keep the
shape of the data similar. Array goes in, array goes out. The amount and
the contents of the array may change, but the array-shape stays. The
problem above, however, requires us to change the shape to a `struct` or
`tuple` with an **Integer average** and an **Integer sum**.

These are the kind of problems where you can apply `reduce`.

# Reduce

Reduce is sort of a generalized version of `map`, `flatMap`, or
`filter`. The basic idea is to **reduce** a sequence into a different
shape utilizing an **accumulator** that can keep incremental state. To
do this, we hand the function a **combinator** closure/function/method
which is called once for each item in the sequence. This may sound
complicated but becomes really easy with a couple of examples.

It is a method on `SequenceType` and looks like this (simplified):

``` Swift
func reduce<T>(initial: T, combine: (T, Self.Generator.Element) -> T) -> T
```

So we have an initial value, and we have a closure which expects us to
return the same type as the initial value. The final value of the
operation is also of the same type as the initial value.

If we take a very simple reduce operation - adding up a list of
integers, the evaluation will look like this:

``` Swift
func combinator(accumulator: Int, current: Int) -> Int {
   return accumulator + current
}
[1, 2, 3].reduce(0, combine: combinator)
// The following steps will be performed
combinator(0, 1) { return 0 + 1 } = 1
combinator(1, 2) { return 1 + 2 } = 3
combinator(3, 3) { return 3 + 3 } = 6
= 6
```

The **combinator** function will be called once for each item in the
list `[1, 2, 3]`. The state will be kept in the **accumulator** variable
which is just an Integer.

Let\'s start re-implementing some of our other, trusted, functional
programming friends. In order to keep things simple for now, all these
functions will operate on `Int` or `Optional<Int>`; i.e. we will ignore
generics in here. Also, keep in mind that the implementations below
exist to explain the behaviour of `reduce`. The native Swift
implementations are usually much faster compared to the reduce versions
below[^1]. Reduce shines in a different set of problems, which will be
explained further below.

## Map

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

## Filter

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

# Reduce Examples

Let\'s start with a favorite of mine, the sum of a list of numbers:

``` Swift
[0, 1, 2, 3, 4].reduce(0, combine: +)
// 10
```

`+` is a valid `combinator` function as it will just add the `lhs` and
the `rhs` and return the result, which is specifically the requirement
`reduce` has.

Another example is building the product of a list of numbers:

``` Swift
[1, 2, 3, 4].reduce(1, combine: *)
// 24
```

Or what about reversing a list:

``` Swift
[1, 2, 3, 4, 5].reduce([Int](), combine: { [$1] + $0 })
// 5, 4, 3, 2, 1
```

Finally, something a tad more complicated. We\'d like to partition a
list based on a division criteria

``` Swift
typealias Acc = (l: [Int], r: [Int])
func partition(lst: [Int], criteria: (Int) -> Bool) -> Acc {
   return lst.reduce((l: [Int](), r: [Int]()), combine: { (ac: Acc, o: Int) -> Acc in 
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

# Reduce vs. Chaining Performance

Apart from the higher flexibility that `reduce` offers, it has another
advantage: Oftentimes, chaining `map` and `filter` induces a performance
penalty as Swift has to iterate over your collection multiple times in
order to generate the required data. Imagine the following code:

``` Swift
[0, 1, 2, 3, 4].map({ $0 + 3}).filter({ $0 % 2 == 0}).reduce(0, combine: +)
```

Apart from being nonsensical, it is also wasting CPU cycles. The initial
sequence will be iterated over 3 times. First to map it, then to filter
it, and finally to sum up the contents. Instead, all of this can just as
well be implemented as one reduce call, which greatly improves the
performance:

``` Swift
[0, 1, 2, 3, 4].reduce(0, combine: { (ac: Int, r: Int) -> Int in 
   if (r + 3) % 2 == 0 {
     return ac + r + 3
   } else {
     return ac
   }
})
```

Here\'s a quick benchmark of running both versions and the for-loop
version below over an list with 100.000 items:

``` Swift
var ux = 0
for i in Array(0...100000) {
    if (i + 3) % 2 == 0 {
        ux += (i + 3)
    }
}
```

        <style type="text/css">
         .linechart {
             border: 3px solid white;
             border-radius: 32px;
             font-family: Sans-Serif;
             color: white;
             font-weight: normal;
             padding: 4px;
             margin-bottom: 20px;
         }
         .redxx {
             background-color: red;
         }
         .greenxx {
             background-color: green;
         }
         .linechart > span {
             padding: 4px;
         }
         h3.ggx {
             font-family: Sans-Serif;
font-weight: normal;
         }
         .orangexx {
             background-color: orange;
         }
        </style>
        <div style="background-color: #ccc; padding: 20px; border-radius: 16px;">

        <div class="linechart greenxx" style="width: 41%">
            <span>For Loop: 0.030 seconds</span>
        </div>
        <div class="linechart orangexx" style="width: 47%">
            <span>Reduce: 0.034 seconds</span>
        </div>
        <div class="linechart redxx">
            <span>Map/Filter: 0.072 seconds</span>
        </div>
        </div>

As you can see, the `reduce` version\' performance is very close to the
mutating for loop and more than twice as fast as the chaining operation.

However, in other situations, chained operation can greatly outperform
`reduce`. Consider the following example:

``` Swift
Array(0...100000).map({ $0 + 3}).reverse().prefix(3)
// 0.027 Seconds
```

``` Swift
Array(0...100000).reduce([], combine: { (var ac: [Int], r: Int) -> [Int] in
    ac.insert(r + 3, atIndex: 0)
    return ac
}).prefix(3)
// 2.927 Seconds
```

Here, we have a stark performance difference of 0.027s for the chained
operation vs. 2.927s for the reduce operation, what\'s happening
here?[^2]

foBrowsing on Reddit points out that reduce\'s semantics means that the
parameters to the closure (if mutated) are copied once for every element
in the underlying sequence. In our case, this means that the
**accumulator** parameter `ac` will be copied for each item in our
0...100000 range. A better, more detailed explanation of this can be
[found in this Airspeedvelocity blog
post](http://airspeedvelocity.net/2015/08/03/arrays-linked-lists-and-performance/).

So, when you\'re replacing a set of operations with `reduce`, always
keep mind whether reduction is indeed a good use case for the situation
in question.

We can now go back to our initial count & average problem and try to
solve it with `reduce`.

# InfoFromState, take two

``` Swift

  func infoFromState(state state: String, persons: [[String: AnyObject]]) 
      -> (count: Int, age: Float) {

      // The type alias in the function will keep the code cleaner
      typealias Acc = (count: Int, age: Float)

      // reduce into a temporary variable
      let u = persons.reduce((count: 0, age: 0.0)) {
          (ac: Acc, p) -> Acc in

          // Retrive the state and the age
          guard let personState = (p["city"] as? String)?.componentsSeparatedByString(", ").last,
                personAge = p["age"] as? Int

            // make sure the person is from the correct state
            where personState == state

            // if age or state are missing, or personState!=state, leave
            else { return ac }

          // Finally, accumulate the acount and the age
          return (count: ac.count + 1, age: ac.age + Float(personAge))
      }

  // our result is the count and the age divided by count
  return (age: u.age / Float(u.count), count: u.count)
}
print(infoFromState(state: "CA", persons: persons))
// prints: (count: 3, age: 34.3333)
```

As in earlier examples above, we\'re once again using a `tuple` to share
state in the accumulator. Apart from that, the code is easy to
understand.

We also defined a `typealias` **Acc** within the `func` in order to
simplify the type annotations a bit.

# Summary

This was a short overview of the power behind the `reduce` method. It is
particularly helpful if you end up chaining a lot of functional methods
together, **or** when output shape of your data differs from the input
shape. I\'ll end this post with more reduce examples to give you
inspirations for various use cases where reduce can easily be applied:

# More Examples

The following examples display additional `reduce` use cases. Keep in
mind that they\'re educational in nature. I.e. they exist to stress the
usage of reduce, not to be general solutions for your codebase. Most of
the examples can be written in a better and faster way (i.e. by using
extensions or generics). There are better implementations of these
examples in various Swift libraries such as
[SwiftSequence](https://github.com/oisdk/SwiftSequence) or
[Dollar.swift](https://github.com/ankurp/Dollar.swift)

## Minimum

Return the minimum entry in a given list. Obviously,
`[1, 5, 2, 9, 4].minElement()` would be a better solution.

``` Swift
[1, 5, 2, 9, 4].reduce(Int.max, combine: min)
```

## Unique

Return a list with all duplicates removed. The better solution would be
to use a `Set`.

``` Swift
[1, 2, 5, 1, 7].reduce([], combine: { (a: [Int], b: Int) -> [Int] in
if a.contains(b) {
   return a
} else {
   return a + [b]
}
})
// prints: 1, 2, 5, 7
```

## Group By

Go over a list and return a new list with the previous list\' items
grouped by a discriminator function. The function in question needs to
return a `Hashable` type so that we can differentiate keys. The order of
the items will be preserved while the order of the groups won\'t
necessarily be preserved.

``` Swift
func groupby<T, H: Hashable>(items: [T], f: (T) -> H) -> [H: [T]] {
   return items.reduce([:], combine: { (var ac: [H: [T]], o: T) -> [H: [T]] in 
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

## Interpose

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

## Interdig

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

## Chunk

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

# Changes

****12/01/2015****

-   Fixed the `rFlatMap` type signature
-   Added additional explanations for the code examples
-   Fixed issue where performance differences were attributed to
    laziness

[^1]: For reasons why, [have a look at this blog
    post](http://airspeedvelocity.net/2015/08/03/arrays-linked-lists-and-performance/)

[^2]: In an earlier version of this post I was falsely assuming Swift\'s
    laziness feature to be the culprit of the difference. [Thanks to
    this Reddit thread for pointing out my
    mistake](https://www.reddit.com/r/swift/comments/3uv1hy/reduce_all_the_things_alternatives_to_mapfilter/)
