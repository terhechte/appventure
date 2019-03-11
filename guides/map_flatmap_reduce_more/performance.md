[frontMatter]
title = "Performance & inout"
tags = ["reduce", "inout", "valuetype", "copy-on-write"]
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
    .reduce(0, +)
```

Apart from being nonsensical, it is also wasting CPU cycles. The initial
sequence will be iterated over 3 times. First to map it, then to filter
it, and finally to sum up the contents. Instead, all of this can just as
well be implemented as one reduce call, which greatly improves the
performance:

``` Swift
[0, 1, 2, 3, 4].reduce(0, { (ac: Int, r: Int) -> Int in 
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
<div style="background-color: #ccc; padding: 20px; border-radius: 16px; margin-bottom: 20px;">
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
`reduce`. Consider the following example where we add *3* to each entry in the array.

``` Swift
Array(0...100000).map({ $0 + 3}).reverse().prefix(3)
// 0.027 Seconds
```

And the `reduce` version:

``` Swift
Array(0...100000).reduce([], { (ac: [Int], r: Int) -> [Int] in
    return ac + [r + 3]
}).prefix(3)

// 2.927 Seconds
```

<div style="background-color: #ccc; padding: 20px; border-radius: 16px; margin-bottom: 20px;">
<div class="linechart" style="width: 100%">
<span>For Loop: 0.027 seconds</span>
</div>
<div class="linechart redxx" style="width: 100%">
<span>Reduce: 2.927 seconds</span>
</div>
</div>

Here, we have a stark performance difference of 0.027s for the chained
operation vs. 2.927s for the reduce operation, what\'s happening
here?

`Arrays` in Swift are value types with so-called `copy on write` semantics.

# Copy on Write

Imagine you had a struct `User`: 
``` Swift
struct User {
  var username: String
}
var benedikt = User(username: "Benedikt")
var secondBenedikt = benedikt
var thirdBenedikt = benedikt
```

`struct` types in Swift are value types. Value type means that each copy
is a new distinct value. So if I were to change the `username` value of `secondBenedikt` to
`Klaus`, then the `username` value of the other two benedikts (`benedikt`, `thirdBenedikt`)
would still be `Benedikt` and not `Klaus`. So, everytime you do a `a = b`, `b` is **copied** to `a`.

Copy operations, however, are expensive. All that memory has to be copied from `a` to `b`. So Swift employs
a smart trick: As long as you don't **mutate / modify** a variable, it will just not copy it. 

So in our example above, `benedikt`, `secondBenedikt`, and `thirdBenedikt` are the same thing, they point
to the same memory. Only once you change one of them (say `benedikt.username = 'Hans'`) will they be copied
into distinct types.

So what's all that to do with our `reduce` issue here?

# Array Value Types

Arrays are `value types`, too. This means that whenever an array is mutated, a new copy is created.
So in our `reduce` function:

``` Swift
Array(0...100000).reduce([], { (ac: [Int], r: Int) -> [Int] in
    return ac + [r + 3]
}).prefix(3)
```

This will copy the array 100000 times. That's why the performance is so abysmal. 
So how do we fix this?

# The power of `inout`

There's another version of `reduce` with slightly different parameters. Its function signature
looks like this (simplified):

``` Swift
func reduce<Result>(into initialResult: Result, 
  _ updateAccumulatingResult: (inout Result, Element) throws -> ()) rethrows -> Result
```

The magic is the `inout Result`. Inout is a special attribute that you can use
in function signatures to denote to Swift that you wish to refer to the same instance of
a type without making copies. The name implies how it works: When the function is called, the
value is `moved in` to the function, when the function is done, the value is `moved out` again.

In the case of our arrays, instead of making multiple copies, we will always modify the same array.

So if we rewrite our `reduce` from above with `reduce(into:)` what is the performance?

Here is the updated code:

``` Swift
Array(0...100000).reduce(into: [Int](), { ac, r in
                return ac.append(r + 3)
            }).prefix(3)
```

And this is the new performance:

<div style="background-color: #ccc; padding: 20px; border-radius: 16px; margin-bottom: 20px;">
<div class="linechart" style="width: 100%">
<span>Map: 0.0295 seconds</span>
</div>
<div class="linechart" style="width: 100%">
<span>Reduce Into: 0.0376 seconds</span>
</div>
<div class="linechart redxx" style="width: 100%">
<span>Reduce: 1.49 seconds</span>
</div>
</div>

We're almost reached the speed of the simpler `map` implementation. It is much
faster now. Awesome!

