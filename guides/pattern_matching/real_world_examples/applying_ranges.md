[frontMatter]
title = "Applying ranges for grading"
tags = ["pattern matching", "switch", "range"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Applying ranges for grading

So you\'re writing the grading iOS app for your local Highschool. The
teachers want to enter a number value from 0 to 100 and receive the
grade character for it (A - F). Pattern Matching to the rescue:

``` Swift
let aGrade = 84

switch aGrade {
case 90...100: print("A")
case 80...90: print("B")
case 70...80: print("C")
case 60...70: print("D")
case 0...60: print("F")
default: print("Incorrect Grade")
}
```

You can also always have ranges as parts of nested types, such as tuples or even
`struct` types, when you implement the [`~=`](apv::match-operator) operator.

``` Swift
let student = (name: "John Donar", grades: (english: 77, chemistry: 21, math: 60, sociology: 42))
switch student {
case (let name, (90...100, 0...50, 0...50, _)): print("\(name) is good at arts")
case (let name, (0...50, 90...100, 90...100, _)): print("\(name) is good at sciences")
default: ()
}
```
