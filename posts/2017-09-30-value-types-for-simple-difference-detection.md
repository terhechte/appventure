[frontMatter]
description = "Utilize value types to quickly determine a differences between two sets of data"
title = "Value Types for Simple Difference Detection"
created = "2017-09-30"
published = true
keywords = ["swift", "value", "types", "uitableview", "uicollectionview", "valuetypes", "struct", "class", "equatable", "tuple"]
slug = "2017-09-30-value-types-for-simple-difference-detection.html"
tags = ["swift", "cocoa", "ios"]
category = ["Swift Tricks", "All"]

[meta]
swift_version = "2.3"
---

Following sage advice I received from [John
Sundell](https://www.swiftbysundell.com/) half a year ago (I am a slow
learner) I will try to write about smaller pieces instead of focusing on
longform content. This should make it easier to update appventure more
often. Thanks John!.

Today, I\'ll write about value types: Value types are a very useful
addition to Swift. Objective-C did offer C `struct` types and
(obviously) classical value types such as numbers, but Swift goes way
beyond that by allowing us to also define more complex structures such
as `Array`, `Set`, or `Dictionary` as value types. One of the best
properties of value types is that they can easily be compared given that
they\'re values:

``` Swift
let one = [1, 2, 3]
let two = [1, 2, 3]
print(one == two) // returns true
```

This way of easily comparing arrays is something we can use to implement
a simple difference detection algorithm without using more heavy-weight
solutions. Imagine you have a simple app that downloads a list of
entries from a server and displays them in a table view. Once a minute
you download a new list and reload the table view. This is not a
particularly nice solution as you\'re reloading the table view even when
there\'re no changes. If your data is defined as a `struct` and you
implement the `Equatable` protocol, then you can simply use the equality
operator to see if the table view needs to be reloaded:

``` Swift
struct Data: Equatable {
  let username: String
  let userid: Int
  static func ==(lhs: Data, rhs: Data) -> Bool {
    return lhs.username == rhs.username && lhs.userid == rhs.userid
  }
}
let oldData: [Data] = currentData()
let newData: [Data] = retrieveNewData()
guard oldData != newData else {
    return
}
updateData(with: newData)
```

However, it may be that your data is modelled using `struct` types, but
that they\'re very complex and change often. So you\'ve never
implemented `Equatable`. Then you have three different options:

1.  Wait for Swift 4.1 which will [hopefully merge a PR which will
    auto-generate](https://github.com/apple/swift-evolution/blob/master/proposals/0185-synthesize-equatable-hashable.md)
    `Equatable` for `struct` types if all properties of a `struct` also
    conform to `Equatable`.
2.  Use Krzysztof Zabłocki\'s
    [Sourcery](https://github.com/krzysztofzablocki/Sourcery) which is a
    meta programming framework that allows you to auto generate things
    like `Equatable` conformance for your types (and much more).
3.  This I will explain in more detail as it is also a pattern that you
    can use if your data is modelled using `class` types.

The idea here is to store just the absolutely necessary information in a
seperate difference detection cache. Imagine the following data model:

``` Swift
final class Story {
  let story_id: Int
  let views: Int
  let last_updated: TimeInterval
  let description: String
}
```

In this example, a Story will never change its id and description. In
order to create a simple cache, we can now just use the information we
absolutely need to determine a change and store them in tuples. Tuples
with up to 6 elements will automatically generate `Equatable`
conformance:

``` Swift
let a = (1, 2, 3)
let b = (1, 2, 3)
print(a == b)
```

With this in mind, we can generate our tuples:

``` Swift
let newInformation: [(Int, Int, TimeInterval)] = 
  stories.map({ ($0.story_id, $0.views, $0.last_updated) })

guard newInformation != oldInformation else { return }
```

This is a simple solution that leverages value types to give us an easy
solution for comparing sets of data. However, if you also need to
determine insertions, deletions and moves then you can still do so with
value types, but you need a proper diff algorithm such as
[Dwifft](https://github.com/jflinter/Dwifft).

Nevertheless, for many simpler use cases it is good to remember that we
can easily build a comparison cache of tuples or structs to determine
general changes to data.
