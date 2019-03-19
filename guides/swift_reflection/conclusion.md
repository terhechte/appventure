[frontMatter]
title = "Conclusion"
tags = ["reflection"]
created = "2019-03-01 11:47:01"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Conclusion

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
-   Converting to / from JSON (or other types)
-   Generated detailed logging / debugging information automatically
    (i.e. for externally generated objects)

# More Information

The source documentation of the Reflection API is very detailed. I\'d
encourage everyone to have a look at that as well.

Also, there\'s a much more exhaustive implementation of the techniques
showcased here in the [CoreValue](http://github.com/terhechte/corevalue)
project on GitHub which allows you to easily encode and decode from / to
Structs to CoreData.
