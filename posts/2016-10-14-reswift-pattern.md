[frontMatter]
description = "Swift 3 replaces NSData with the Data value type. Implement a Doom Wad file parser with the new Data type to understand the differences."
title = "Introduction into Reactive Programming with ReSwift"
tags = ["swift", "cocoa", "ios"]
created = "2016-10-14"
published = false
keywords = ["swift", "doom", "wad", "lumps", "data", "nsdata", "swift3", "binary", "bytes"]
slug = "2016-10-14-reswift-pattern.html"
---

# TODO:

-   Fix link to pragma conferences
-   Fix link to MVP, Viper, MVVM, etc
-   fix links to reswift
-   fix links to benjamin encz, also, fix his name
-   look up archimedian method. Was it that? The method of finding a
    solution by asking questions.

I just attended the fantastic \#pragmaconf in Spain and tremendously
enjoyed it. One thing that I noted not only during \#pragma but also at
other conferences was a raising interest into alternative application
design patterns such as Model-View-Presenter (MVP), VIPER, or
Model-View-ViewModel (MVVM). Another pattern which is also frequently
mentioned, but much less known, is ReSwift.

ReSwift is a specific implementation of the much more general reactive
programming development model one can find in RxSwift or ReactiveCocoa.
In comparison to those, ReSwift is much simpler to understand and
implement. General reactive programming, on the other hand, is much more
flexible. One could easily implement ReSwift - and much more - within
the constraints of RxSwift.

This, as I find, makes ReSwift a particularly compelling pattern for a
soft introduction into reactive programming. Make no mistake, ReSwift is
not a toy though. It is being used in production codes and his bigger
brother, Redux (see below) is a very commonly used design pattern in the
Javascript world.

In this post, I\'ll give a detailed introduction into ReSwift in order
to explain the basic idea behind reactive programming. I\'ll also be
constructing a simple app to better understand how the different
building blocks of a ReSwift application fit together. The contents of
this post are based on a talk about ReSwift that I held at CocoaHeads
Hamburg in May 2016. Let\'s go.

# ReSwift

ReSwift was brought into begin by Bejamin Engz. It is the Swift
implementation of a design pattern found in the Javascript world called
Redux. Before diving in, why don\'t we have a look at the projects
Github pages to see how they\'re pitching themselves. This is also a
good excercise in understanding why reactive programming is sometimes
considered hard. ReSwift says on their website:

> ReSwift is a **Redux**-like implementation of the **unidirectional
> data flow** architecture in Swift.

Ok, interesting. That doesn\'t really help us, does it? It just adds
`Redux` and `unidirectional data flow` to our list of unknown words.
Lets look them up.

> Redux evolves the ideas of **Flux**, but avoids its complexity by
> taking cues from **Elm**.

Ah that helps... not. We have to add `Flux` and `Elm` to our list of
things to look up. So, what\'s Flux, then?

> Flux: An application architecture for **React** utilizing a
> **unidirectional data flow**.

We already heard about unidirectional data flow, so thankfully we don\'t
have to add that to our list. Also, React is really well known nowadays
so we kinda don\'t have to add it - though do we really know what it is
and how it works? Also, we still haven\'t searched Google for Elm:

> Elm uses the **functional reactive programming** style and **purely
> functional graphical layout** to build user interface without any
> destructive updates. It enforces a "model view update" architecture,
> where the update has the following signature: (action, state) -\>
> state

Ok, lets step back for a moment and see what we have:

<div align="center">
<img src="/img-content/reswift-redux-matroska.png" srcset="/img-content/reswift-redux-matroska@2x.png 2x" /><br/>
<br/>
<br/>

This already looks more difficult than the block diagrams for MVVM or
MVP and I\'m afraid when we look up the other terms it will not help us
solve this riddle. So instead, we will try to take a step back and
inspect the original problem that these approaches try to solve. From
there, we will use the good old archimedian method to (hopefully) arrive
at the same solution as Redux / ReSwift.

# State: The Original [Sin]{.underline} Problem

Every app necessarily requires state. The classic example is the
non-temporary Core Data model. But other examples are:

-   Temporary loaded information from a REST API
-   Temporary user input (UITextField for a Tweet)
-   State specific to a Viewcontroller (`isLoading`, `isWaitingFor`,
    `currentSearchTerm`)

While MVC presses us to keep temporary state in a `Model`, we\'re
usually given much more leeway for the temporary state that defines our
app. They\'re usually stored as instance variables or properties in our
viewcontroller. Apple is leading by example here, too: If you look into
the Objective-C headers (where these things, unlike Swift, still bleed
out), you can see a lot of properties for internal state.

The major problem with this state of affairs[^1] is that there\'s no
dedicated, central, place to store it. The state is spread out all over
your app. If state were immutable, that wouldn\'t be a problem. But
oftentimes we find ourselves in situations where state is mutable, and
where multiple actors in our system need to be addressed in case state
changes. We have multiple solutions for these problems, such as
Singletons, KVO, Bindings, Notifications, Closures, Delegation, and
more. These measures don\'t solve the underlying problem, they\'re
merely complex constructs build around it:

> Apps built upon MVC often end up with a lot of complexity around state
> management and propagation. We need to use callbacks, delegations,
> Key-Value-Observation and notifications to pass information around in
> our apps and to ensure that all the relevant views have the latest
> state.
>
> This approach involves a lot of manual steps and is thus error prone
> and doesn\'t scale well in complex code bases.
>
> It also leads to code that is difficult to understand at a glance,
> since dependencies can be hidden deep inside of view controllers.
> Lastly, you mostly end up with inconsistent code, where each developer
> uses the state propagation procedure they personally prefer.

If you\'ve been doing MVC for a long time, this may not feel like such a
problem. After all, one of the tennets of OOP is the encapsulation of
state: Objects hide away their state and manage it via exposed methods.
It is not necessary to know about the (maybe very complex) state in
order to use the object. This is obviously true, but the more objects
you have that interact with each other in a specific way, the more data
is being shared between objects, the more state restoration your app
requires, the more problematic this whole business becomes. Have a look
at the following example.

# A Social Network Client

We\'ve been tasked with adding a search feature to the comment list of a
social network client. The requirements are simple:

1.  There\'s a list of all comments with a \"Find\" button at the top
2.  When the user taps the \"Find\" button, the button should highlight,
    and
3.  A \"Search Field\" should appear
4.  The last-entered search term should be visible there
5.  The cell background color should change so that the user can
    immediately understand that this is a filtered list
6.  The list should be filtered by the current search term
7.  The matches should highlight the search term

Here\'s a gallery showcasing the different steps of the process.


Imagine this scenario:

``` {.swift}

class ListViewController: UIViewController {

}

```

-   NO GENERAL STORAGE ETC

[^1]: Pun intended
