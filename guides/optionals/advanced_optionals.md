[frontMatter]
title = "Advanced Optionals"
tags = ["optionals", "if let", "guard let", "?"]
created = "2019-03-02 16:04:26"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Advanced Optionals

We've already seen the basics of handling optionals. However, there's much more you can do.
In this section we'll explore optionals even more and have a look at some advanced ways of
handling optionals

## Optional Chaining

Now imagine your work on a relationship database, and your data are
users and their relations. So you'd have a Person and then the person
could have an optional child and the child could have an optional 
sibling and that sibling could have an optional child, and so on.

Since all of these are `Person` types, we could model the type like this:

``` Swift
struct Person {
  var child: Person?
  var sibling: Person?
  var father: Person?
  var mother: Person?
}
```

All of our properties are optional because they can all be nil.
Now imagine you'd like to find the following relative:

``` bash
person -> child -> sibling -> child -> mother
```

So, how would we do that with `if let` in Swift? Let us have a try:

``` Swift
if let child = person.child,
   let sibling = person.sibling,
   let nextChild = person.child,
   let mother = nextChild.mother {
   print(mother)
   }
```

This is a lot of code and can quickly become confusing. Thankfully,
Swift has another feature which lets us write this in a much simpler fashion.

The idea being that in a chain of operations on optionals
(such as Optional.child -> Optional.silbing -> Optional.child) 
if any of these operations returns nil, we stop executing the chain early.

You represent this behaviour via a `?` before calling a method. Here is the
previous example implemented with the `optional chaining`:

``` Swift
if let mother = person.child?.sibling?.child?.mother {
  print(mother)
}
```

We're basically telling Swift "If the value of the child property of person is not
optional, then please get me the sibling property from it". And we do the same again
for the next propery.

This, also, works great for dictionaries where all return values are always optional.

  ``` Swift
  example["a"]?["b"]?["c"]
  ```

By adding `?` in between each call / access, Swift will
automatically unwrap if there is a value, or stop the chain as soon
as any one evaluates to nil.

## Map

Consider the following code:

``` Swift
func example() -> Int? {return 10}

if let value = example() {
    storeInDatabase(value * 2)
}
```

    If we break down the logic, what we\'re really trying to achieve,
    were it not for optionals, is the following:

    ``` Swift
    storeInDatabase(example() * 10)
    ```

    Optionals are still very useful here, as they prevent us from the
    danger of multiplying nil with 10 and trying to store that in the
    database. But still, we have to admit that the optionals code looks
    more convoluted. As you can imagine, there\'s a solution to this, of
    course.

    Optionals offer an implementation of the `map` function which will
    call the value of an optional with a supplied closure if
    the optional has a value.

``` Swift
let px: Int? = 5

// This will print "5"
px.map { print($0) }

// This will do nothing
let px: Int? = nil
px.map { print($0) }

```

This lets us rewrite our example from above in terms of `map` as follows:

``` Swift
example().map({ number in 
  storeInDatabase(number * 2) 
})
```

What happens here is: When the return value of `example()` is not optional, then the closure
will be called the value as `number` and so we can call the `storeInDatabase` function with our number multiplied by two. If the return value of `example()` is empty, nothing will happen.

With Swift's nice simplified closure syntax we can even simply this example to the following:

``` Swift
example().map { storeInDatabase($0 * 2) }
```
