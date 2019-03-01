[frontMatter]
title = "Private State"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Private State

In addition to the previous example, there are also use cases where
using tuples beyond a temporary scope is useful. Following Rich
Hickey\'s \"If a tree falls in the woods, does it make a sound?\", as
long as the scope is private and the tuple\'s type isn\'t littered all
over the implementation, using tuples to store internal state can be
fine.

A simple and contrived example would be storing a static UITableView
structure that displays various information from a user profile and
contains the key path to the actual value as well as a flag noting
whether the value can be edited when tapping on the cell.

``` Swift
let tableViewValues = [
    (title: "Age", value: "user.age", editable: true),
    ("Name",           "user.name.combinedName",  true),
    ("Username",       "user.name.username",      false),
    ("ProfilePicture", "user.pictures.thumbnail", false)]
```

The alternative would be to define a struct, but if the data is a purely
private implementation detail, a tuple works just as well.

A better example is when you define an object and want to add the
ability to add multiple change listeners to your object. Each listener
consists of a name and the closure to be called upon any change:

``` Swift
typealias Action = (_ change: Any?) -> Void
func addListener(name: String, action: @escaping Action) { }
func removeListener(name: String) { }
```

How will you store these listeners in your object? The obvious solution
would be to define a struct, but this is a very limited scope, and the
struct will only be internal, and it will be used in only three cases.
Here, using a tuple may even be the better solution, as the
destructuring makes things simpler:

``` Swift

class ListenerStuff {

    typealias Action = (_ change: Any?) -> Void

    var listeners: [(String, Action)] = []

    func addListener(name: String, action: @escaping Action) {
        listeners.append((name, action))
    }

    func removeListener(name: String) {
        if let idx = listeners.index(where: { $0.0 == name }) {
            listeners.remove(at: idx)
        }
    }

    func execute(change: Int) {
        for (_, listener) in listeners {
            listener(change as Any?)
        }
    }
}

var stuff = ListenerStuff()
let ourAction: ListenerStuff.Action = { x in print("Change is \(x ?? "NONE").") }
stuff.addListener(name: "xx", action: ourAction)
stuff.execute(change: 17)
```

As you can see in the `execute` function, the destructuring abilities
make tuples especially useful in this case, as the contents are directly
destructured into the local scope.
