[frontMatter]
description = "Taming SourceKitService for less Xcode memory consumption"
title = "Taming SourceKitService for Less Xcode Memory Consumption"
created = "2017-10-08"
published = true
keywords = ["xcode", "sourcekit", "swift", "SourceKitService"]
slug = "2017-10-08-taming-sourcekitd.html"
tags = ["swift", "cocoa", "ios"]
category = ["Swift Tricks", "All"]

[meta]
swift_version = "2.3"
---

# Update \[10/15/2017\]

\<a href=\"<https://t.co/aJc8ZZSm9c>\"\>It seems that Xcode 9.1 beta 2
fixes this issue.\</a\>

In my preliminary testing, everything worked fine. This feels really
good.

# Original Article

There were recently two popular Swift posts on Hacker News[^1] [^2], and
one issue I saw coming up multiple times was the memory consumption of
the tooling nee Xcode. One particular problem is that for some codebases
the Swift sourcecode process `SourceKitService` consumes a huge amount
of memory. I\'ve had it rise to 30GB and beyond - at which point my
system usually stalls and I\'m not able to continue working for a couple
of minutes.

Oftentimes memory issues like these can be solved by reviewing your
sourcecode with the same tools you also use to reduce your compile
times. See:

-   <https://www.jessesquires.com/blog/measuring-compile-times-xcode9/>
-   <https://www.swiftbysundell.com/posts/improving-swift-compile-times>

However, for some, complex, codebases this may not be enough. I\'ve
employed an **awful** little hack in order to at least keep my machine
from stalling. I wrote a small little bash script that check the memory
consumption of the `SourceKitService` every `n` seconds and if it goes
beyond `x` megabytes of memory (by default **5.000**) I restart it. I
feel that this may be useful to some others so I\'m sharing it here for
posterity. Note that this is an awful hack and future versions of
`SourceKitService` will probably (hopefully!) not need this anymore.
Meanwhile, this might be of help to others:

``` bash
#!/bin/bash

# Amount of seconds to wait between measures
n=1
# Limit memory consumption to this many megabytes before killing the process
x=5000

name="SourceKitService"
while true; do 
  fields=`ps aux -m | grep -v grep | grep -i $name | tr -s ' '`
  mem=`echo $fields | cut -d ' ' -s -f 6| awk '{$1=$1/1024; print $1;}' | cut -d '.' -f 1`
  pid=`echo $fields | cut -d ' ' -s -f 2`
  if [ -z "$mem" ]; then
      echo "$name not running"
      sleep 15
      continue
  fi
  if [ "$mem" -gt $x ]; then
      echo "Killing $name pid $pid with mem $mem"
      kill -9 $pid
      sleep 5
  fi
  sleep $n
done
```

To use this just paste that code into a file (say `sourcekill.sh`) and
do:

``` bash
chmod +x ./sourcekill.sh
./sourcekill.sh
```

If you want to kill it, just hit `CTRL=C`.

[^1]: Why many developers still prefer Objective-C
    <https://news.ycombinator.com/item?id=15421073>

[^2]: Dictionary and Set Improvements in Swift 4.0
    <https://news.ycombinator.com/item?id=15403882>
