[frontMatter]
title = "Iterating over Enum Cases"
tags = ["enum", "CaseIterable"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.0"
updated = "true"
---

# Iterating over Enum Cases

Say you've created a nice new enum with several cases:

``` Swift
enum Drink: String {
  case coke, beer, water, soda, lemonade, wine, vodka, gin
}
```

Now, you'd like to display all of those drinks at runtime in a list. You somehow want to run a `for-each` loop over all of your enum cases. The `enum` type does not offer this ability out-of-the-box. Instead, you have to explicitly tell the Swift compiler that you wish for your enum to be iterable. You do this by conforming to the empty `CaseIterable` protocol:

``` Swift
enum Drink: String, CaseIterable {
  case coke, beer, water, soda, lemonade, wine, vodka, gin
}
```

Now, you can easily iterate over your `enum` with the new `allCases` property:

``` Swift
for drink in Drink.allCases {
  print("For lunch I like to drink \(drink)\)")
}
```

This works only if your `enum` cases do not contain any associated values:

``` Swift
enum Drink: CaseIterable {
  case beer 
  case cocktail(ingredients: [String])
}
```

This code will not compile and the reason for that is simple. The Swift compiler does not know how to construct the `cocktail` case. And for good reason, should it be a Gin Tonic, or a Cuba libre? You wouldn't want the Swift compiler to decide that, but it has to! Because in order for you use `allCases` it will need to return an `enum` case including associated values.

So there it is, `CaseIterable` is a great Swift feature, however keep in mind that it can only be used with simple `enum` cases.

