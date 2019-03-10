[frontMatter]
description = "In this post I'll examine the Swift reflection API, see how fast it is, and will try to show use cases where it can be applied successfully."
title = "The Swift Reflection API and what you can do with it"
created = "2015-10-24"
published = true
keywords = ["feature", "swift", "reflection", "struct", "class", "displayType", "mirror", "api", "reflecting", "any", "anyobject"]
slug = "2015-10-24-swift-reflection-api-what-you-can-do.html"
tags = ["swift", "cocoa", "ios"]
---

<h6><a href="http://swift.gg/2015/11/23/swift-reflection-api-what-you-can-do/">This post is also available in <b>🇨🇳Chinese</b></a><span> Thanks to </span><a href="http://swift.gg/tags/APPVENTURE/">SwiftGG</a></h6>

Even though Swift stresses strong types, compile time safety, static
dispatch it still offers a Reflection mechanism as part of the standard
library. You may already have seen it in various blog posts or projects
like [here
(Tuples)](http://design.featherless.software/enumerating-tuple-values-swift/?utm_campaign%3DSwift%252BSandbox&utm_medium%3Demail&utm_source%3DSwift_Sandbox_12),
[here (Midi
Packets)](http://design.featherless.software/enumerate-messages-midipacket-swift-reflection/)
or [here (Core Data).](https://github.com/terhechte/corevalue) Maybe
you\'re interested in using in one of your projects, or you may want to
better understand the problem domains on which reflection can be
applied. This is an overview of the possibilities of the Swift
Reflection API based a talk I held recently at the [Macoun
conference](http://www.macoun.de) in Frankfurt, Germany.

# API Overview

The best understanding of the topic can be achieved by having a look at
the API to see what it offers us.

## Mirrors

Swift\'s reflection capabilities are based around a `struct` called
**Mirror**. You create a mirror for a particular `subject` and the
mirror will then let you query it.

Before we do that, let\'s define a simple data structure that we can use
as our subject.

``` Swift
import Foundation.NSURL

public class Store {
    let storesToDisk: Bool = true
}
public class BookmarkStore: Store {
    let itemCount: Int = 10
}
public struct Bookmark {
   enum Group {
      case Tech
      case News
   }
   private let store = {
       return BookmarkStore()
   }()
   let title: String?
   let url: NSURL
   let keywords: [String]
   let group: Group
}

let aBookmark = Bookmark(title: "Appventure", url: NSURL(string: "appventure.me")!, keywords: ["Swift", "iOS", "OSX"], group: .Tech)
```

## Creating a Mirror

The easiest way of creating a mirror is the `reflecting` initializer:

``` Swift
public init(reflecting subject: Any)
```

Lets use it with our `aBookmark` `struct`:

``` Swift
let aMirror = Mirror(reflecting: aBookmark)
print(aMirror)
// prints : Mirror for Bookmark
```

So this creates a `Mirror for Bookmark`. As you can see, the type of the
subject is `Any`. This is the most general type in Swift. Anything under
the Swift Sun is at least of type `Any` [^1]. So this makes the mirror
compatible with `struct`, `class`, `enum`, `Tuple`, `Array`,
`Dictionary`, `set`, etc.

There are three additional initializers in the Mirror struct, however
those are mostly used for circumstances where you\'d want to provide
your own, custom mirror. We [will explain those additional initializers
below when we discuss custom mirrors](#custommirrors).

## What\'s in a Mirror

The `Mirror struct` contains several `types` to help you identify the
information you\'d like to query.

The first one is the `DisplayStyle` `enum` which tells you the type of
the subject:

``` Swift
public enum DisplayStyle {
    case Struct
    case Class
    case Enum
    case Tuple
    case Optional
    case Collection
    case Dictionary
    case Set
}
```

Those are the supported types of the reflection API. As we saw earlier,
reflection only requires an `Any` type, and there\'re many things in the
Swift standard library that are of type `Any` but aren\'t listed in the
`DisplayStyle` enum above. What happens when you try to reflect over one
of those, say a closure?

``` Swift
let closure = { (a: Int) -> Int in return a * 2 }
let aMirror = Mirror(reflecting: closure)
```

In this case, you\'d get a mirror, but the `DisplayStyle` would be nil
[^2]

There\'s also a `typealias` for the child elements of a `Mirror`:

``` Swift
public typealias Child = (label: String?, value: Any)
```

So each child consists out of an optional **label** and a **value** of
type `Any`. Why would the label be an `Optional`? If you think about it,
it makes sense, not all of the structures that are supported by
reflection have children with names. A `struct` has the property\'s name
as the label, but a Collection only has indexes, not names. Tuples are a
little bit special. In Swift values in tuple could have optional labels.
Doesn\'t matter if value in tupple is labeled or not, in reflection
tuple will have labels \".0\", \".1\" and so on.

Next up is the `AncestorRepresentation` `enum` [^3]:

``` Swift
public enum AncestorRepresentation {
    /// Generate a default mirror for all ancestor classes.  This is the
    /// default behavior.
    case Generated
    /// Use the nearest ancestor's implementation of `customMirror()` to
    /// create a mirror for that ancestor.      
    case Customized(() -> Mirror)
    /// Suppress the representation of all ancestor classes.  The
    /// resulting `Mirror`'s `superclassMirror()` is `nil`.
    case Suppressed
}
```

This `enum` is used to define how superclasses of the reflected subject
should be reflected. I.e. this is only used for subjects of type
`class`. The default (as you can see) is that Swift generates an
additional mirror for each superclass. However, if you need more
flexibility here, you can use the `AncestorRepresentation enum` to
define how superclasses are being mirrored. [We will have a look at that
further below](#custommirrors).

## How to use a Mirror

So we have our `aMirror` instance variable that reflects our `aBookmark`
of type `Bookmark` subject. What do we do with it?

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
// prints: Optional(Swift.Mirror.DisplayStyle.Struct)
```

### children

This returns a `AnyForwardCollection<Child>` with all the children that
the subject contains. Children are not limited to entries in an `Array`
or `Dictionary`. All properties of a `struct` or `class`, for example,
are also children returned by this property. The protocol
`AnyForwardCollection` means that this is a collection type with indices
that support forward traversal.

``` Swift
for case let (label?, value) in aMirror.children {
    print (label, value)
}
//prints:
//: store main.BookmarkStore
//: title Optional("Appventure")
//: url appventure.me
//: keywords ["Swift", "iOS", "OSX"]
//: group Tech
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
print(Mirror(reflecting: NSNull()).subjectType)
//print : NSNull
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
print(Mirror(reflecting: aBookmark.store).superclassMirror())
// prints: Optional(Mirror for Store)

```

# Practical Example

## Structs to Core Data

Imagine we\'re working at the newest, hot, tech startup: **Books
Bunny**. We offer an Artificial Intelligence with a browser plugin that
automatically analyses all the sites that the user visits and
automatically bookmarks the relevant urls.

It\'s 2016, Swift is already open source, so our server backend is
obviously written in Swift. Since we have millions of site visits active
in our system at a time, we\'d like to use `structs` for the analysis
part of each site that a user visits. However, if our AI decides that
this is worthy of a bookmark, we\'d like to use CoreData to store this
type in a database.

Now, we don\'t want to write custom serialization to Core Data code
whenever we introduce a new `struct`. Rather, we\'d like to develop this
in a way so that we can utilize it for all future `structs` we develop.

So, how do we do that?

## A Protocol

Remember, we have a `struct` and want to automatically convert this to
`NSManagedObject` (**Core Data**).

If we want to support different `structs` or even types, we can
implement this as a protocol and then make sure our desired types
conform to it. So which functionality should our imaginary protocol
offer?

-   First, it should allow us to define the name of the **Core Data
    Entity** that we want to create
-   Second, it should have a way to tell it to convert itself to an
    `NSManagedObject`

Our `protocol` could look something like this:

``` Swift
protocol StructDecoder {
    // The name of our Core Data Entity
    static var EntityName: String { get }
    // Return an NSManagedObject with our properties set
    func toCoreData(context: NSManagedObjectContext) throws -> NSManagedObject
}
```

The `toCoreData` method uses the new Swift 2.0 exception handling to
throw an error, if the conversion fails. There\'re several possible
error cases, which are outlined in the `ErrorType` `enum` below:

``` Swift
enum SerializationError: ErrorType {
    // We only support structs
    case StructRequired
    // The entity does not exist in the Core Data Model
    case UnknownEntity(name: String)
    // The provided type cannot be stored in core data
    case UnsupportedSubType(label: String?)
}
```

We have three error cases that our conversion has to look out for. The
first one is that we\'re trying to apply it to something that is not a
`struct`. The second is that the `entity` we\'re trying to create does
not exist in our Core Data Model. The third is that we\'re trying to
write something into Core Data which can not be stored there (i.e. an
`enum`).

Let\'s create a struct and add protocol conformance:

## Bookmark struct

``` Swift
struct Bookmark {
   let title: String
   let url: NSURL
   let pagerank: Int
   let created: NSDate
}
```

Next, we\'d like to implement the `toCoreData` method.

## Protocol Extension

We could, of course, write this anew for each `struct`, but that\'s a
lot of work. Structs do not support inheritance, so we can\'t use a base
class. However, we can use a `protocol extension` to extend to all
conforming `structs`:

``` Swift
extension StructDecoder {
    func toCoreData(context: NSManagedObjectContext) throws -> NSManagedObject {
    }
}
```

As this extension is being applied to our conforming `structs`, this
method will be called in the structs context. Thus, within the
extension, `self` refers to the `struct` which we\'d like to analyze.

So, the first step for us is to create an `NSManagedObject` into which
we can then write the values from our `Bookmark struct`. How do we do
that?

## A Bit of Core Data

Core Data is a tad verbose, so in order to create an object, we need the
following steps:

1.  Get the name of the entity which we\'d like to create (as a string)
2.  Take the `NSManagedObjectContext`, and create an
    `NSEntityDescription` for our entity
3.  Create an `NSManagedObject` with this information.

When we implement this, we have:

``` Swift
// Get the name of the Core Data Entity
let entityName = self.dynamicType.EntityName

// Create the Entity Description
// The entity may not exist, so we're using a 'guard let' to throw 
// an error in case it does not exist in our core data model
guard let desc = NSEntityDescription.entityForName(entityName, inManagedObjectContext: context)
    else { throw UnknownEntity(name: entityName) }

// Create the NSManagedObject
let managedObject = NSManagedObject(entity: desc, insertIntoManagedObjectContext: context)
```

## Implementing the Reflection

Next up, we\'d like to use the Reflection API to read our bookmarks
properties and write it into our `NSManagedObject` instance.

``` Swift
// Create a Mirror
let mirror = Mirror(reflecting: self)

// Make sure we're analyzing a struct
guard mirror.displayStyle == .Struct else { throw SerializationError.StructRequired }
```

We\'re making sure that this is indeed a `struct` by testing the
`displayStyle` property.

So now we have a `Mirror` that allows us to read properties, and we have
a `NSManagedObject` which we can set properties on. As the mirror offers
a way to read all children, we can iterate over them and set the values.
So let\'s do that.

``` Swift
for case let (label?, value) in mirror.children {
    managedObject.setValue(value, forKey: label)
}
```

Awesome. However, if we try to compile this, it will fail. The reason is
that `setValueForKey` requires an object of type `AnyObject?`, however
our `children` property only returns a `tuple` of type `(String?, Any)`
- i.e. our value is of type `Any` but we need an `AnyObject`. To solve
this, we have to test the value for `AnyObject` conformance. This also
means that we can throw an error if we receive a property with a type
that does not conform to `AnyObject` (such as an `enum`, for example).

``` Swift
let mirror = Mirror(reflecting: self)

guard mirror.displayStyle == .Struct 
  else { throw SerializationError.StructRequired }

for case let (label?, anyValue) in mirror.children {
    if let value = anyValue as? AnyObject {
        managedObject.setValue(child, forKey: label)
    } else {
        throw SerializationError.UnsupportedSubType(label: label)
    }
}
```

Now, our `setValueForKey` method will only be called if and only if the
child is of type `AnyObject`.

Now, the only thing left to do is return our `NSManagedObject`. The
complete code looks like this:

``` Swift
extension StructDecoder {
    func toCoreData(context: NSManagedObjectContext) throws -> NSManagedObject {
        let entityName = self.dynamicType.EntityName

        // Create the Entity Description
        guard let desc = NSEntityDescription.entityForName(entityName, inManagedObjectContext: context)
            else { throw UnknownEntity(name: entityName) }

        // Create the NSManagedObject
        let managedObject = NSManagedObject(entity: desc, insertIntoManagedObjectContext: context)

        // Create a Mirror
        let mirror = Mirror(reflecting: self)

        // Make sure we're analyzing a struct
        guard mirror.displayStyle == .Struct else { throw SerializationError.StructRequired }

        for case let (label?, anyValue) in mirror.children {
            if let value = anyValue as? AnyObject {
                managedObject.setValue(child, forKey: label)
            } else {
                throw SerializationError.UnsupportedSubType(label: label)
            }
        }

        return managedObject
    }
}
```

That\'s it. We\'re converting our `struct` to `NSManagedObject`.

# Performance

So, how fast is this? Can this be used well in production? I did some
testing:

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

        <h3 class='ggx'>Create 2000 NSManagedObjects</h3>

        <div class="linechart greenxx" style="width: 30%">
            <span>Native: 0.062 seconds</span>
        </div>
        <div class="linechart redxx">
            <span>Reflection: 0.207 seconds</span>
        </div>
        </div>

Native, here, means creating an `NSManagedObject` and setting the
property values via `setValueForKey`. If you create a `NSManagedObject`
subclass within Core Data and set the values directly on the properties
(without the dynamic `setValueForKey` overhead) this is probably even
faster.

So, as you can see, using reflection slows the whole process of creating
`NSManagedObjects` down by about **3.5x**. This is fine when you\'re
using this for a limited amount of items, or when you don\'t have to
care about speed. However, when you need to reflect over a huge amount
of `structs`, this will probably kill your app\'s performance.

# Custom Mirrors {#custommirrors}

As we already discussed earlier, there\'re other options creating a
Mirror. This is useful, for example, if you need to customize just how
much of your **subject** can be seen with a mirror. The `Mirror Struct`
has additional initializers for this.

## Collections

The first special `init` is tailor-made for collections:

``` Swift
public init<T, C : CollectionType where C.Generator.Element == Child>
  (_ subject: T, children: C, 
   displayStyle: Mirror.DisplayStyle? = default, 
   ancestorRepresentation: Mirror.AncestorRepresentation = default)
```

Compared to the `init(reflecting:)` initializer above, this one allows
us to define much more details about the reflection process.

-   It only works for collections
-   We can set the subject to be reflected **and** the children of the
    subject (the collection contents)

## Classes or Structs

The second can be used for a `class` or a `struct`.

``` Swift
public init<T>(_ subject: T, 
  children: DictionaryLiteral<String, Any>, 
  displayStyle: Mirror.DisplayStyle? = default, 
  ancestorRepresentation: Mirror.AncestorRepresentation = default)
```

Interesting to note, here, is that you provide the children (i.e.
properties) of your subject as a `DictionaryLiteral` which is a bit like
a dictionary only that it can be used directly as function parameters.
If we implement this for our `Bookmark struct`, it looks like this:

``` Swift
extension Bookmark: CustomReflectable {
    func customMirror() -> Mirror {
        let children = DictionaryLiteral<String, Any>(dictionaryLiteral: 
        ("title", self.title), ("pagerank", self.pagerank), 
        ("url", self.url), ("created", self.created), 
        ("keywords", self.keywords), ("group", self.group))

        return Mirror.init(Bookmark.self, children: children, 
            displayStyle: Mirror.DisplayStyle.Struct, 
            ancestorRepresentation:.Suppressed)
    }
}
```

If we do another performance measurement now, there\'s even a slight
improvement:

        <div style="background-color: #ccc; padding: 20px; border-radius: 16px;">

        <h3 class="ggx">Create 2000 NSManagedObjects</h3>

        <div class="linechart greenxx" style="width: 30%">
            <span>Native: 0.062 seconds</span>
        </div>
        <div class="linechart redxx">
            <span>Reflection: 0.207 seconds</span>
        </div>
        <div class="linechart orangexx" style="width: 98%">
            <span>Reflection: 0.203 seconds</span>
        </div>
</div>

But hardly worth the effort, as it defeats our initial purpose of
reflecting over our `struct`\'s members.

# Use Cases

So, where does this leave us? What are good use cases for this?
Obviously, if you\'re working a lot of `NSManagedObject`\'s, this will
considerably slow down your code base. Also if you only have one or two
`structs`, it is easier, more performant, and less magical if you simply
write a serialization technique yourself with the domain knowledge of
your individual `struct`.

Rather, the reflection technique showcased here can be used if you have
many, complicated structs, and you\'d like to store some of those
sometimes.

Examples would be:

-   Setting Favorites
-   Storing Bookmarks
-   Staring Items
-   Keeping the last selection
-   Storing the ast open item across restarts
-   Temporary storage of items during specific processes.

Apart from that, of course, you can also use reflection for other use
cases:

-   Iterate over tuples
-   Analyze classes
-   Runtime analysis of object conformance
-   Generated detailed logging / debugging information automatically
    (i.e. for externally generated objects)

# Discussion

The Reflection API exists primarily as a tool for the Playgrounds.
Objects conforming to the reflection API can easily be displayed in a
hierarchical way in the playgrounds sidebar. Thus, the performance is
not optimal. Nevertheless, this has still interesting use cases outside
of playgrounds as we explained in the **Use Cases** chapter.

# More Information

The source documentation of the Reflection API is very detailed. I\'d
encourage everyone to have a look at that as well.

Also, there\'s a much more exhaustive implementation of the techniques
showcased here in the [CoreValue](http://github.com/terhechte/corevalue)
project on GitHub which allows you to easily encode and decode from / to
Structs to CoreData.

[^1]: In particular, `Any` is an empty protocol and everything
    implicitly conforms to this protocol

[^2]: Or rather, an empty optional

[^3]: I\'ve shortened the documentation a bit
