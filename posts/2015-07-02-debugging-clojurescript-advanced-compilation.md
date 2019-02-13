[frontMatter]
description = "FIXME FIXME FIXME"
title = "Debugging advanced compilation errors in ClojureScript"
created = "2015-07-02"
published = true
keywords = ["debugging", "clojure", "clojurescript", "externs"]
slug = "2015-07-02-debugging-clojurescript-advanced-compilation.html"
tags = ["clojure"]
---

Just a quick note so I can easily look this up again and maybe help
others in a similar situation. When you\'re working on a ClojureScript
app and there\'re errors in advanced compilation mode which do not
appear in the dev environment, tracking down these bugs can be quite
daunting.

Thankfully, there\'s a compiler setting which tries to emit readable
names during compilation: `:pseudo-names true`. The documentation says:

> With :advanced mode optimizations, determines whether readable names
> are emitted. This can be useful when debugging issues in the optimized
> JavaScript and can aid in finding missing externs. Defaults to false.

Together with `:pretty-print true` this helps a lot in finding out just
where the bug you\'re seeing originated.

**An Example:**

``` Swift
{
    :optimizations :advanced
    :pretty-print true
    :pseudo-names true
}

```
