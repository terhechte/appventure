[frontMatter]
description = "An easy way to add more structure to your classes by leveraging structs and enums"
title = "Cleaner Classes with Structs and Tuples"
created = "2019-02-24"
published = true
keywords = ["ios", "macos", "swift", "tuples", "classes", "structs"]
slug = "2019-02-24-anonymous-tuple-structs.html"
tags = ["tuple", "struct"]
[meta]
feature_image = "http://appventure.me/img-content/2019-02-24-anonymous-tuple-structs.jpg"
thumbnail = "/img-content/tuple_structure.png"
---

Imagine you\'re working on a social networking app and you have a
controller that is responsible for displaying a user image with a follow
and a like button. Imagine also, that - in line with the single
responsibility principle and view controller composition - the
****like**** and ****follow**** functionality is handled somewhere else.
Our social network does have premium user accounts as well as corporate
user accounts (companies) and so there\'re a couple of configuration
options available for your `InteractiveUserImageController` (naming was
never my strong suit). One possible option of our class could look
(partially) like this (for demonstration purposes, there\'re obviously a
lot of things that we can change here):

``` Swift
final class InteractiveUserImageController: UIView {
    /// Should the Premium Layout be used
    var isPremium: Bool
    /// What kind of account do we have
    var accountType: AccountType
    /// Tapping the view will highlight it
    var isHighlighted: Bool
    /// The username to display
    var username: String
    /// The profile image to display
    var profileImage: UIImage
    /// Can the current user like this user
    var canLike: Bool
    /// Can the current user follow this user
    var canFollow: Bool
    /// Should the big like button be used
    var bigLikeButton: Bool
    /// For some containers we need a special background color
    var alternativeBackgroundColor: Bool

    init(...) {}
}
```

Now, these are a lot of properties. As our app grows, we might end up
adding even more properties here. Of course, we can refactor and group
them by responsibility, but sometimes single responsibility still leads
to quite a few properties. So how can we possibly structure this a bit
better?

## Swift Struct Structure

Swift\'s `struct` types can actually be really helpful here. What we can
do is group these properties by their type by moving them into
**one-time** structs:

``` Swift
final class InteractiveUserImageController: UIView {
    struct DisplayOptions {
        /// Should the big like button be used
        var bigLikeButton: Bool
        /// For some containers we need a special background color
        var alternativeBackgroundColor: Bool
        /// Should the Premium Layout be used
        var isPremium: Bool
    }
    struct UserOptions {
        /// What kind of account do we have
        var accountType: AccountType
        /// The username to display
        var username: String
        /// The profile image to display
        var profileImage: UIImage
    }
    struct State {
        /// Tapping the view will highlight it
        var isHighlighted: Bool
        /// Can the current user like this user
        var canLike: Bool
        /// Can the current user follow this user
        var canFollow: Bool
    }

    var displayOptions = DisplayOptions(...)
    var userOptions = UserOptions(...)
    var state = State(...)

    init(...) {}
}
```

As you can see, what we\'ve done here is we moved the state into
seperate `struct` types. Not only does this make the class cleaner, it
also makes it easier for new developers to find related options.

This is already a very nice improvement, but we can do even better!

The issue we have here is that there is an additional step involved when
looking up a property.

Since we\'re using one-time struct types we have to define them
somewhere, (i.e. `struct DisplayOptions`), but we also have to
instantiate them somewhere (i.e.
`let displayOptions = DisplayOptions(...)`. This is in general **ok**,
but in larger classes this might still require an additional lookup to
figure out the type of `displayOptions`. However, there is no way in
Swift to create anonymous `struct` types like this [^1]:

``` Swift
let displayOptions = struct {
    /// Should the big like button be used
    var bigLikeButton: Bool
    /// For some containers we need a special background color
    var alternativeBackgroundColor: Bool
    /// Should the Premium Layout be used
    var isPremium: Bool
}
```

## Anonymous Structs nee Tuples

Actually, there is such a type in Swift. It is our good old friend, the
`tuple`. See for yourself:

``` Swift
var displayOptions: (
  bigLikeButton: Bool,
  alternativeBackgroundColor: Bool,
  isPremium: Bool
)
```

This defines a new type `displayOptions` that has three properties
(`bigLikeButton`, `alternativeBackgroundColor`, `isPremium`) and can be
accessed just like our `struct` from earlier:

``` Swift
user.displayOptions.alternativeBackgroundColor = true
```

Even better, the defintion does not need an additional initialization,
so everything is in the same place.

## Enforced Immutability

Finally, the whole `tuple` is either `mutable` or `immutable`. You can
see that in the first line: We\'re defining `var displayOptions` but no
`var` or `let` `bigLikeButton`. `bigLikeButton` is also a `var` just
like `displayOptions`. The advantage of this is that this enforces
moving static constant properties (i.e. line height, header height) into
a different (`let`) group than mutable properties.

## Add some data

As a nice addition, you can also use this feature when you need to
initialize these properties with values:

``` Swift
var displayOptions = (
  bigLikeButton: true,
  alternativeBackgroundColor: false,
  isPremium: false,
  defaultUsername: "Anonymous"
)
```

Very similar to the earlier code, this defines a tuple of options but
also initializes them with the correct values right away.

## Nesting

Naturally, you can also nest these tuple options easily, which makes it
even easier compared to our original struct approach:

``` Swift
class UserFollowComponent {
    var displayOptions = (
        likeButton: (
            bigButton: true,
            alternativeBackgroundColor: true
            ),
        imageView: (
            highlightLineWidth: 2.0,
            defaultColor: "#33854"
        )
    )
}
```

I hope you found this article useful. I\'m using this simple pattern
quit a lot in order to give my code more structure. Sometimes only for
2-3 properties, but even then it is already beneficial.

[^1]: Unlike C
