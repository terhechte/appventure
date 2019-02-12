[frontMatter]
title = "Using Core Data with Structs in Swift"
created = "2015-07-06"
published = false
keywords = ["swift", "core", "data", "optional", "struct"]
slug = "2015-07-06-using-core-data-with-structs.html"
tags = ["swift"]
---

Describe the way to use reflection for interacting with core data

Proof of Concept:

``` {.Javascript}

protocol NSManagedStruct {
    var EntityName: String {get}
}

enum NSManagedStructError : ErrorType {
    case StructConversionError()
}


func toCoreData(context: NSManagedObjectContext)(entity: NSManagedStruct) throws -> NSManagedObject {

    let mirror = Mirror(reflecting: entity)

    if let style = mirror.displayStyle where style == .Struct || style == .Class {

        // try to create an entity
        let desc = NSEntityDescription.entityForName(entity.EntityName, inManagedObjectContext:context)
        let result = NSManagedObject(entity: desc!, insertIntoManagedObjectContext: nil)

        for (labelMaybe, valueMaybe) in mirror.children {

            guard let label = labelMaybe else {
                continue
            }

            if ["EntityName"].contains(label) {
                continue
            }

            switch valueMaybe {
            case let k as Int16:
                result.setValue(NSNumber(short: k), forKey: label)
            case let k as AnyObject:
                result.setValue(k, forKey: label)
            default:
                continue
            }

        }

        return result
    }

    throw NSManagedStructError.StructConversionError()
}

```
