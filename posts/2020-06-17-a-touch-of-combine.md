[frontMatter]
description = "A simple way of introducing Combine into your codebase"
title = "A touch of Combine"
created = "2020-06-17"
published = true
keywords = ["swift", "combine"]
tags = []

[meta]
feature_image = "https://appventure.me/img-content/title_combine.jpg"
---

Combine was released at WWDC 2019, therefore it only targets iOS 13 and up. There're even [Open Source Combine solutions](https://github.com/broadwaylamb/OpenCombine) that target earlier iOS versions. Combine is a very well-designed framework, but it solves problems in a very different way then you'd normally do on iOS (if you weren't using RxSwift already). Nevertheless, you might want to start using Combine from time to time, especially once you can drop iOS 12 support in your app.

This article shows a way of using Combine in a very limited approach within your code, mostly to handle events within the scope of a single controller. 
You can obviouly do much more with Combine, but oftentimes this requires bigger changes to more components than just one function within an existing controller.

## Debounce and Throttle

One pattern that Combine solves in a nice way is controlling the flow of events. Say you have an app with a slider which the user can use to change a value that forces a redraw of your UI. If the user moves the slider very slowly, events are emitted at a very slow rate. If the user moves the slider really fast, though, events are emitted at a very fast rate. Now lets imagine that your redraw operation is very expensive (say you're rendering an image with a simple raytracer). In this case, having too many render operations at once will overload your CPU. 

Another, similar problem is if you download something from the network when the user taps a button. That's fine if the user taps the button once, but if the user taps it 50 times in 10 seconds, then you might be overloading something

The usual solution for this problem is to have a cancellation token that remembers the last event:

``` swift
private class Cancellation {
  var cancelled: Bool = false
}

private var lastCancellation: Cancellation?

func event() {
  lastCancellation?.cancelled = true
  let newToken = Cancellation()
  lastCancellation = newToken
  downloader.downloadOperation { result in 
    if newToken.cancelled { return 
  }
  ...
}

```

This works mostly fine. However, it hides a clear responsibility between multiple lines of code. Especially once this code is split up over multiple places in a large controller, the clear meaning becomes harder to understand. Also, it lacks a lot of control. Maybe you want every 10th event to go through, and more.

## Enter Combine

Combine offers a nice way of controlling the event flow in this case via the `throttle` and `debounce` operators:

### Throttle:

[The docs say:](https://developer.apple.com/documentation/combine/passthroughsubject/3204657-throttle)

> Publishes either the most-recent or first element published by the upstream publisher in the specified time interval.

### Debounce:

[The docs say:](https://developer.apple.com/documentation/combine/anypublisher/3204205-debounce)

> Publishes elements only after a specified time interval elapses between events.

## Using Throttle and Combine

There's an easy way of introducing throttle and combine into your view controller without exposing much of Combine to other parts of your code. What we're doing here is creating a Combine Subject and a Combine Cancellation token at the same time. We're also using a closure as the type of the Subject. By doing it this way, we can use it for any action which should be throttled. I'll first list the code and then explain it:

``` swift
var delayedDebounce: (
   publisher: PassthroughSubject<() -> Void, Never>,
   cancellable: AnyCancellable?
   ) = {
       let publisher: PassthroughSubject<() -> Void, Never> = PassthroughSubject()
       let sink = publisher
         .debounce(for: .milliseconds(400), scheduler: RunLoop.main)
         .sink { action in
             action()
   }
   return (publisher, sink)
}()

```

In the first line, we're creating a `Tuple` named `delayedDebounce. The tuple will only have two items, the `Subject` and the `AnyCancellable` cancellation token:

``` swift
var delayedDebounce: (publisher: PassthroughSubject, cancellable: AnyCancellable?)
```

`PassthroughSubject` is a default Combine `Subject` which does not have a default value. Any value it receives will be forwarded through the Combine stream. A subject is a Combine `Publisher` that exposes a method for outside callers to publish elements.

Next up, we're initializing the `Tuple` with a lazy evaluated closure:

``` swift
var delayedDebounce: (publisher: PassthroughSubject, cancellable: AnyCancellable?) = { ... }()
```

Within this closure, we're setting up the actual publisher. Lets inspect this code in detail:

``` swift
let publisher: PassthroughSubject<() -> Void, Never> = PassthroughSubject()
let sink = publisher
   .debounce(for: .milliseconds(400), scheduler: RunLoop.main)
   .sink { action in
     action()
}
```

Initially, we need to create our `PassthroughSubject` (which is a `Publisher`). It generic over two types, the `Output` it will **pass through** and the `Failure` that can happen. In our case, we don't expect any errors so the `Failure` type is `Never`. The `Output` we want to pass through is an action that will be executed: `() -> Void`.

Now that we have our publisher, we can use it to [perform any of the methods that are exposed on the `Publisher` protocol](https://developer.apple.com/documentation/combine/publisher). In our case, `debounce` or  `throttle`:

``` swift
let sink = publisher.debounce(for: .milliseconds(400), scheduler: RunLoop.main)
```

In the example above, we tell it to wait 400 milliseconds between events before a event is passed through. So the final thing we need is to execute the action that was delayed and debounced by 400 milliseconds. That's what the `sink` is for:

``` swift
.sink { action in
     action()
}
````

With this setup, we can execute actions and rest assured that there's a 400ms interval between events. We use the `send` method of the `Subject` to achive this:

``` swift
delayedDebounce.publisher.send { 
  view.layoutIfNeeded()
}

```

# Abstractions

This code already works. However, if you use it a lot, you might want to abstract it into a simple `struct` that simplifies the setup even more:

``` swift
struct Debouncer {
  private var delayedDebounce: (
     publisher: PassthroughSubject<() -> Void, Never>,
     cancellable: AnyCancellable?
     ) = {
         let publisher: PassthroughSubject<() -> Void, Never> = PassthroughSubject()
         let sink = publisher
           .debounce(for: .milliseconds(400), scheduler: RunLoop.main)
           .sink { action in
               action()
     }
     return (publisher, sink)
  }()

  func execute(_ action: () -> Void) {
    delayedDebounce.publisher.send(action)
  }
}
```

Doing it this way has the downside that you can't configure the Combine stream any more. For example, with the initial implementation, you could also do this:


``` swift
var delayedDebounce: (
   publisher: PassthroughSubject<() -> Void, Never>,
   cancellable: AnyCancellable?
   ) = {
       let publisher: PassthroughSubject<() -> Void, Never> = PassthroughSubject()
       let sink = publisher
         .debounce(for: .milliseconds(400), scheduler: RunLoop.main)
         .throttle(for: .milliseconds(20), scheduler: RunLoop.main, latest: true)
         .delay(for: 2, scheduler: RunLoop.main)
         .sink { action in
             action()
   }
   return (publisher, sink)
}()
```

Here, we're first debouncing, then throttling, and finally delaying for 2 seconds. This is only for illustrative purposes.

