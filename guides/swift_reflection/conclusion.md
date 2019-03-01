[frontMatter]
title = "Conclusion"
tags = []
created = "2019-03-01 11:47:01"
description = ""
published = false

---

# Conclusion

So in the `Custom Mirrors` section we added several performance improvements. If we do another performance measurement now, there\'s even a slight improvement:

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
