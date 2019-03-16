[frontMatter]
title = "How to handle optionals"
tags = ["optionals"]
created = "2019-03-02 16:04:26"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# How to handle optionals

As we saw in the [previous](javascript:prev()) chapter, Optionals are 
really just `enum` types. However, as they're deeply ingrained into
the language, Swift offers a lot of additional possibilities of
handling `Optionals`.

## If Let

Certainly the most used one is the so-called if let. You're basically telling
Swift "If this optional value `myOptionalValue` actually contains a value, please give me the contained value
into the variable named `myUnwrappedValue`":

``` Swift
if let myUnwrappedValue = myOptionalValue {
  print(myUnwrappedValue)
}
```

If `myOptionalValue` is actually empty, then the `print` statement
would never be executed. As with any typical `if` statement, this
can also have an else expression:

``` Swift
if let myUnwrappedValue = myOptionalValue {
  print(myUnwrappedValue)
} else {
  print("No Value")
}
```

You can also combine multiple `if let` statements if you need to handle
multiple `Optional` values:

``` Swift
if let firstValue = firstOptionalValue,
   let secondValue = secondOptionalValue,
   let thirdValue = thirdOptionalValue {
   print(firstValue, secondValue, thirdValue)
} 
```

Finally, you can mix and match the `if let` pattern with normal if expressions:

``` Swift
if let firstValue = firstOptionalValue,
   firstValue > 10
   let secondValue = secondOptionalValue,
   secondValue == "HTTP",
   let thirdValue = thirdOptionalValue {
   print(firstValue, secondValue, thirdValue)
} 
```

In this example, we only print the three values if the firstOptionalValue is not empty and has a value > 10, and if the second optional value is not empty and has the value "HTTP" and if the third optional value is not empty.

## Guard

Another nice feature of Swift are the `guard` statements. They're basically like inverted `if` statements. You usually use them at the beginning of a block of code to make sure that all your requirements are held. The main difference compared to `if let` is that you're required to leave the current scope (i.e. `return`, `continue`, or `break`) if the `guard` does not succeed. Lets look at this nonsensical function that tries to do addition with two `Optional` `Int` values. For that to work, we need to make sure that 

``` Swift
func addOptionals(firstNumber: Int?, secondNumber: Int?) -> Int? {
  guard let first = firstNumber, let second = secondNumber
        else { return nil }
  return first + second
}
```

So here, we do the `guard let` in order to make sure that both `firstNumber` and `secondNumber` have a value, otherwise we can't really do the addition. So if one of them (or both) don't have a value, we return early in the `else { return nil}` block. 

Observe how with `if let` the code-to-be-executed is within the `if` braces, while with `guard let` it is not:

``` Swift
if let a = b {
  print(b)
}

guard let a = b else { return }
print(b)
```

This makes it easier to follow the structure of code because your main code is not nested but only at the very left side of the function.

## Switch

We already mentioned this in the [previous](javascript:previous()) chapter, but you can also use `switch` to handle `Optionals`:

``` Swift
switch myOptionalValue {
 case let value?: print(value)
 default: ()
}
```

We have a whole guide on pattern matching with Swift where this is explained
in much more detail.

## Forced Unwrap

Sometimes, if you're absolutely sure that your `Optional` has a value, you can 
also use the `forced unwrap`. This tells Swift to handle this `Optional` value as if
it was a non-optional value.

This works great, but it means that the optional has to have a value. If
you try a forced unwrap on an empty optional (i.e. nil) it will cause a
runtime error (meaning, crash).

``` Swift
let oneValue: Int? = 5
let twoValue: Int? = nil

print(oneValue!) // No Crash
print(twoValue!) // Crash
```

But wait, there's more. The next section in our guides discusses two additional methods of
handling optionals that are also really, really useful: Optional Chaining and Map.
