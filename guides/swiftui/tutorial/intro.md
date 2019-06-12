[frontMatter]
title = "Intro: A Shoe Designer"
tags = ["swiftui"]
created = "2019-06-12 21:01:50"
description = "An app that designs shoes."
published = true

[meta]
feature_image = "/img-content/swiftui_article.jpg"

---

In order to better understand how SwiftUI works, we will develop a simple tutorial app. We will continue adding features to this app in the next chapters. For now, the first thing we will build is a simple way for users to customize / design sneakers. In order to allow this, we need a preview of the current sneaker, a way to change the colors of the current sneaker, and a way to store the current sneaker. 

Here is a small GIF of what we are about to create.

<img src="/img-content/swiftui_tutorial_anim.gif" width="30%" />

## The Model

Lets start with the model as it will help us shape the rest of the application. Currently, our model will only store the colors of the current sneaker. However, future chapters will also add the manufacturers name, shoe name, shoe model, etc. So in order to prepare for that we will have a more general `ShoeConfiguration` type that will contain a more distinct `ShoeColors` type. We will first have a look at this `ShoeColors` type.

``` swift
struct ShoeColors {
    /// Outline Color
    var outline: Color
    /// Base Color
    var base: Color
    /// Side Color
    var side: Color
    /// Sole Color
    var sole: Color
    /// Back Cage Color
    var cage: Color
}
```

Our configuration has colors for multiple parts of the shoe. The outline, the base color, the side color, and so on. Note that we're not using `UIColor` or `NSColor` or `CGColor`, or even `CIColor`; no, there's a new color type in SwiftUI. It has a limited set of default color defintions, but it is sufficient for our use case here. 

The next part is to have a configuration for our shoe. The colors will be just one part of the configuration. A first draft would look something like this:

``` swift
class ShoeConfiguration {
    
    var shoeColors: ShoeColors 
    
    init() {
        shoeColors = ShoeColors(outline: .black, base: .white, side: .orange, sole: .purple, cage: .gray)
    }
}
```

We're creating a simple `class` that acts as the configuration of one shoe. Currently, we're only hosting `shoeColors`, so there's not really much going on. What we do do, though, is to configure a default shoe in the initializer. 

``` swift
import SwiftUI
import Combine

class ShoeConfiguration: BindableObject {
    
    struct ShoeColors {
        var outline: Color
        var base: Color
        var side: Color
        var sole: Color
        var cage: Color
    }
    
    var shoeColors: ShoeColors {
        didSet {
            didChange.send(self)
        }
    }
    
    var didChange = PassthroughSubject<ShoeConfiguration, Never>()
    
    init() {
        shoeColors = ShoeColors(outline: .black, base: .white, side: .orange, sole: .purple, cage: .gray)
    }
}

struct ShoeView : View {
    
    @Binding var colors: ShoeConfiguration.ShoeColors
    
    private func colorParts() -> [(name: String, color: Color)] {
        return [
            ("base", colors.base),
            ("side", colors.side),
            ("sole", colors.sole),
            ("cage", colors.cage),
            ("outline", colors.outline)
        ]
    }
    
    var body: some View {
        ZStack {
            ForEach(colorParts().identified(by: \.name)) { shoePart in
                Image(shoePart.name).resizable()
                    .renderingMode(.template)
                    .foregroundColor(shoePart.color)
            }
        }
    }
}

extension View {
    func scaledFrame(from geometry: GeometryProxy, scale: CGFloat) -> some View {
        self.frame(width: geometry.size.width * scale, height: geometry.size.height * scale)
    }
}

struct ColorPickerEntry : View {
    var selected: Bool
    var shoeColor: Color
    
    private let outerScale: CGFloat = 0.7
    private let innerScale: CGFloat = 0.5
    
    var body : some View {
        GeometryReader { geometry in
            Group {
                if self.selected {
                    Circle().fill(self.shoeColor)
                        .overlay(Circle().stroke(Color.black, lineWidth: 2.0))
                        .scaledFrame(from: geometry, scale: self.outerScale)
                } else {
                    Circle().stroke(Color.gray)
                        .scaledFrame(from: geometry, scale: self.innerScale)
                        .overlay(Circle().fill(self.shoeColor)
                            .scaledFrame(from: geometry, scale: self.innerScale), alignment: .center)
                        .overlay(Circle().stroke(Color.gray)
                            .scaledFrame(from: geometry, scale: self.outerScale))
                }
            }.frame(width: geometry.size.width, height: geometry.size.height)
        }
    }
}


struct ColorPicker : View {
    @Binding var selectedColor: Color
    var name: String
    var body : some View {
        VStack(alignment: HorizontalAlignment.center, spacing: 0) {
            Text(name).font(.body)
            HStack {
                ForEach([Color.black, Color.white, Color.orange, Color.purple, Color.gray].identified(by: \.hashValue)) { color in
                    Button(action: {
                        self.selectedColor = color
                    }) {
                        ColorPickerEntry(selected: self.selectedColor.hashValue == color.hashValue, shoeColor: color)
                            .frame(width: 38, height: 38)
                    }
                }
            }
        }
    }
}


struct ShoeConfigurator : View {
    
    @ObjectBinding var shoeConfiguration = ShoeConfiguration()
    
    var body: some View {
        VStack {
            ShoeView(colors: $shoeConfiguration.shoeColors)
                .frame(width: 250, height: 114, alignment: .center)
            ColorPicker(selectedColor: $shoeConfiguration.shoeColors.base,
                        name: "Base")
            ColorPicker(selectedColor: $shoeConfiguration.shoeColors.cage,
                        name: "Cage")
            ColorPicker(selectedColor: $shoeConfiguration.shoeColors.side,
                        name: "Side")
            ColorPicker(selectedColor: $shoeConfiguration.shoeColors.sole,
                        name: "Sole")
        }
    }
}

struct ContentView : View {
    @State private var selection = 0
    
    var body: some View {
        ShoeConfigurator()
    }
}

#if DEBUG
struct ContentView_Previews : PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
#endif

```
