[frontMatter]
title = "Declarative Programming"
tags = ["swiftui"]
created = "2019-06-11 21:01:50"
description = "Quick introduction into declarative programming"
published = true

[meta]
feature_image = "/img-content/swiftui_article.jpg"

---

# Declarative.. what? Reactive.. what?

When SwiftUI came out some developers were quick to draw parallels to other existing app development technologies such as RxSwift, React, Flutter, Elm, and others. Indeed, some of the key ideas of SwiftUI are similar to what these other technologies offer. However, even if you've never used one of them, don't be afraid. While the general ideas are the same, the implementations vary wildly. You'd also not claim to be a `.NET` developer just because `Windows Forms` and UIKit are object oriented UI frameworks. In a similar manner the details matter and that is, really, where we all start as beginners again. 

Below, you will find a quick introduction into declarative and reactive programming. If you think you already know this, [just move on to the next part where we build a shoe composer in SwiftUI.](javascript:next())

# The beauty of a game engine

One point that was reiterated during 2019 WWDC as well as numerous conference talks, blog posts and tweets before that is that state is a very fickle thing. Many bugs manifest because we have a variable that is shared between places and one of the places updates it while the other doesn't register this update, and suddenly we have different state in two places and confusing things happen. Imagine a search field that doesn't update the result list when the user replaces the next with a paste command. The problem is not that we forgot to also remember to update the list on paste, the problem is that the state of the search field contents exists in two places: In the search field and in the result list as a predicate. The correct solution would be to have the state only in one place and both the list and the search field connect to this value. As the value changes, both the text field and the list redraw.

Most 3D game engines work this way. While the fundamentals of a game engine are incredibly complicated, the basics are stunningly simple. A game engine works as follows:

- Have a internal state of what the world looks like (which player is where, which enemies are where)
- Draw the whole world
- while True
  - Take user input, calculate enemy movement
  - Update the internal state
  - Draw the whole world

Can you pin-point what is so fundamentally simple about this? There are no UIViews or UIButtons or UITableViews that need to be updated once the user enters something. Everything is being re-rendered all the time. Each change to the internal state (the user moved) results in a complete re-render of the whole scene. There're no hidden views, forgotten UIViewController children, data sources, UI updates, and so on. The whole scene, really, is just a long list of draw calls based on the current state.

# Being lazy

Doing this with a traditional UI framework like UIKit would be rather cumbersome. Not only would the CPU be busy allocating and deallocating a lot of views all the time, all the user actions would also result in heavy flickering and jittery movements. That's because all of UIKit is build on the model that views are not recreated 60 times a second. However, our UI apps don't actually change like a game scene. Instead, only some elements change. In a game, each movement usually moves all the vertices of the scene around. In our apps, most of the time, just one element changes its state. Thus we can add an optimization to make this game engine approach much more feasible for our us: We only re-render what actually changed. If the user taps a button, this button needs to be re-rendered, everything else can be kept as is. This is one of the magic ingredients of SwiftUI.

# A game engine that does UI

SwiftUI does everything explained above. It forces you to share state with bindings among multiple views. If state changes, the views are compared to see if the new state would change their output. If that's the case they're re-rendered. If not, they're kept as is. With this approach, SwiftUI is like a game engine for UI apps. Instead of thinking how you would add and remove buttons, you just re-render your whole UI based on the current state. SwiftUI makes sure that only the relevant parts are actually updated. This is best explained with a simple example.

# A simple example

Imagine you have an app with a toggle button and a search field. The toggle button controls the visibility of the search field. Here is our UIKit implementation:

``` Swift
final class ButtonView: UIViewController {
    var toggleButton = UISwitch()
    var searchField = UISearchTextField()
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        toggleButton.addTarget(self, action: #selector(didTapButton(sender:)), for: .allTouchEvents)
        searchField.isHidden = true
        view.addSubview(toggleButton)
        view.addSubview(searchField)
    }
    
    @objc func didTapButton(sender: UISwitch) {
        searchField.isHidden = !toggleButton.isOn
    }
}
```

This is classic iOS code and while there are many things that can be improved here, it shows a standard pattern. In contrast to the game engine example we had earlier, this view is not re-rendered for every user action. In fact, this view has state in multiple places: `searchField.isHidden` and `toggleButton.isOn`. We assign them in `didTapButton`, but this is not a clear binding that UIKit knows about. If we just change `toggleButton.isOn = true` somewhere else, the searchfield will not change. Lets look at a (simplified) SwiftUI alternative:


``` swift
struct ButtonView : View {
    @State var visible: Bool = false
    var body : some View {
        VStack {
            Toggle(isOn: $visible) {
                Text("Toggle")
            }
            if visible {
                Text("Hello World")
            }
        }
    }
}
```

So what is happening here? First of all, we're missing a lot of ceremony around the initialization and creation of UI elements. Where is our toggle initialized, and where is our text initialized? Also, where are we setting the value from the toggle on the `hidden` property of the text? Also, what's with the weird `some View`, `@State`, `VStack`, and `$visible`. We will explain one after the other. 

First of all, remember what we said earlier. SwiftUI is like a lazy game engine. Whenever something changes, the UI is rerendered. Since our UI is always rerendered, we don't have to care about state, about the allocation and creation and initialization of buttons. Instead, we just describe to Swift what the UI should look like (akin to the `draw` calls in a game engine). That's what's happening here. Our `var body : some View` is a property that returns the complete description of our current UI. The UI is composed out of UI components. In our example this is `VStack`, `Toggle`, and `Text`.

- `VStack`: This is a vertical stack. It aligns its children in a vertical list. 
- `Toggle`: Is our toggle button. However, compared to UIKit the toggle button requires a value that stores the current toggle value. *It doesn't store it itself*. There is no internal toggle state. Instead, the toggle requires you to tell it where to store its state. We do this with the `$NameOfVariable`. The syntax for this might look a bit alien, but we will ignore this for now for the sake of simplicity.
- `Text`: This will construct a new `label`. Easy.
- `if visible`: This also looks kinda obvious. If the variable `visible` is set to `true` then, please render the text field. But.. how does this update? Initially, `visible` is set to false, so how does the `Text` become visible again? Remember, just like a game engine, whenever the state changes, we re-render the UI. So that means that whenever `visible` changes its value, the `if visible` is executed again.

But how does Swift figure out that `var visible` has changed? We did not set a `didSet` or `set {} get {}` for this property, neither did we use `@managed`, `@objc` or `@dynamic`. Instead there is a new thing! `@State`. This is what tells Swift that `visible` should be a special variable that we can bind components to. Components such as our `Toggle` button. `@State` is used for component / view local state. The way it works is as follows:

1. `@State var visible: Bool` will create a new variable with a lot of update and subscription machinery in the background. 
2. `Toggle(isOn: $visible)` will bind to this `visisble` value. Whenever `visible` changes, our toggle will change. Changing our toggle will always also change `visible`. These two are linked.
3. Since we're referring to our `visible` variable from within our `body` (via `if visible`) Swift knows that our `body` is dependent upon `visible`. This means that whenever `visible` changes, Swift will be like "Oh, visible changed, this means the view is probably out of date, I will re-render the view". 

So, our `if visible { Text(...) }` will be re-executed whenever our toggle is pressed.

## Multiple toggles

With the above, you might wonder, what happens if we add multiple toggles and or buttons to modify our state? Does it still work? Of course it does! Here's a convoluted example:

<img src="/img-content/swiftui_intro_toggles.png" width="40%" style="box-shadow: 2px 2px 24px 0px rgba(0, 0, 0, 0.6);" />

``` swift
struct ButtonView : View {
    @State var visible: Bool = false
    var body : some View {
        VStack {
            Toggle(isOn: $visible) {
                Text("Toggle")
            }
            Toggle(isOn: $visible) {
                Text("Toggle")
            }
            Button(action: {
                self.visible.toggle()
            }) {
                Text("Yeah")
            }
            if visible {
                Text("Hello World")
            }
        }
    }
}
```

Here, we have not one, not two, but there toggles that all refer to our `visible`. Tapping any one of them will change our state and will also update all our other toggles. This shows how powerful it is to have a declarative UI system that uses bindings to make sure there is only one source of truth.

This was a brief overview of how SwiftUI works, and in the next section (coming soon!) we will build a UI to customize sneakers. Here's a preview already:

<img src="/img-content/swiftui_intro_preview_sneakers.png" width="30%" style="box-shadow: 2px 2px 24px 0px rgba(0, 0, 0, 0.6);" />

