[frontMatter]
title = "Performance"
tags = ["map", "compactMap", "filter", "reduce"]
created = "2019-02-20 19:49:10"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Performance

Apart from the higher flexibility that `reduce` offers, it has another
advantage: Oftentimes, chaining `map` and `filter` induces a performance
penalty as Swift has to iterate over your collection multiple times in
order to generate the required data. Imagine the following code:

``` Swift
[0, 1, 2, 3, 4].map({ $0 + 3})
    .filter({ $0 % 2 == 0})
    .reduce(0, combine: +)
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

[^2]: In an earlier version of this post I was falsely assuming Swift\'s
    laziness feature to be the culprit of the difference. [Thanks to
    this Reddit thread for pointing out my
    mistake](https://www.reddit.com/r/swift/comments/3uv1hy/reduce_all_the_things_alternatives_to_mapfilter/)
