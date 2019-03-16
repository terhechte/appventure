[frontMatter]
title = "How to use a Mirror"
tags = ["reflection", "mirror"]
created = "2019-03-01 11:47:01"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# How to use a Mirror

So we have our `myMirror` instance variable that reflects our `Bookmark`. What do we do with it?

These are the available properties / methods on a `Mirror`:

-   `let children: Children`: The child elements of our subject
-   `displayStyle: Mirror.DisplayStyle?`: The display style of the
    subject
-   `let subjectType: Any.Type` : The type of the subject
-   `func superclassMirror() -> Mirror?`: The mirror of the subject\'s
    superclass

In the next step, we will analyze each of these.

### displayStyle

This is easy. It will just return a case of the `DisplayStyle` `enum`.
If you\'re trying to reflect over an unsupported type, you\'ll get an
empty `Optional` back (as explained above).

``` Swift
print (aMirror.displayStyle)
// prints: Optional(Swift.Mirror.DisplayStyle.struct)
```

### children

This returns a `AnyCollection<Child>` with all the children that
the subject contains. Children are not limited to entries in an `Array`
or `Dictionary`. All properties of a `struct` or `class`, for example,
are also children returned by this property. The protocol
`AnyCollection` means that this is a type [erased `Collection`.](apv::type-erase)

``` Swift
for case let (label?, value) in myMirror.children {
    print (label, value)
}
//prints:
//: store main.BookmarkStore
//: title Optional("Appventure")
//: url appventure.me
//: keywords ["Swift", "iOS", "OSX"]
//: group tech
```

### SubjectType

This is the type of the subject:

``` Swift
print(aMirror.subjectType)
//prints : Bookmark
print(Mirror(reflecting: 5).subjectType)
//prints : Int
print(Mirror(reflecting: "test").subjectType)
//prints : String
print(Mirror(reflecting: Null()).subjectType)
//print : Null
```

However, the Swift documentation has the following to say:

> This type may differ from the subject\'s dynamic type when `self` is
> the `superclassMirror()` of another mirror.

### SuperclassMirror

This is the mirror of the superclass of our subject. If the subject is
not a class, this will be an empty `Optional`. If this is a class-based
type, you\'ll get a new `Mirror`:

``` Swift
// try our struct
print(Mirror(reflecting: aBookmark).superclassMirror())
// prints: nil
// try a class
print(Mirror(reflecting: myBookmark.store).superclassMirror())
// prints: Optional(Mirror for Store)

```
