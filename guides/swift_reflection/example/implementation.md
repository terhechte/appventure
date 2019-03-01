[frontMatter]
title = "Structs to Core Data"
tags = []
created = "2019-03-01 11:47:01"
description = ""
published = false

---

# Structs to Core Data

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
