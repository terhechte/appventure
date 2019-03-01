[frontMatter]
title = "Performance"
tags = []
created = "2019-03-01 11:47:01"
description = ""
published = false

---

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
