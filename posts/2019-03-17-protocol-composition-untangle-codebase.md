[frontMatter]
description = "A simple way to untangle your codebase via protocols. Particularly useful for project configurations."
title = "Using protocol composition to untangle your codebase"
created = "2019-03-17"
published = true
keywords = ["ios", "macos", "swift", "protocol", "composition", "struct", "untagle"]
slug = "2019-03-17-protocol-composition-untangle-codebase.html"
tags = ["protocol", "composition"]
[meta]
static-feature-image = "http://appventure.me/img-content/2019-03-17-protocol-composition-untangle-codebase.jpg"
---

In this article, I\'d like to discuss the benefit of splitting protocols
into smaller mini-protocols. In order to exemplify this, we will look
into the imaginary implementation of a static site generator in Swift.
We will only cover the `structure` of a site generator, though. The
writing of an actual static site generator in Swift has to wait for
another time.

Static site generators take articles (usually written in Markdown) and
convert them into HTML. This, by itself, is easy, but there is a lot of
additional functionality that needs to be implemented for a static site
generator to be actually useful. Examples are:

-   Google sitemap support
-   RSS feeds
-   Copying assets (images, css, js)
-   Calculating tag clouds

## Configuration

The structure of different websites varies to a large degree, it is
almost safe to say that no two websites are equal. In order to
accomodate for that, our static site generator will need to provide a
configuration which allows the consumer to configure it depending on the
needs of the particular website. Obviously, we will have all time
favorites, such as the `title`, the `address` of the server,
`meta tags`, or the name of the `author`. We will store this
configuration in a Swift `struct`:

``` Swift
struct Configuration {
  let title = "My Website"
  let address = "https://terhech.de"
  let metaTags = ["swift", "website", "furry"]
  let author = "Benedikt Terhechte"
}
```

When our app starts up, we create one `Configuration` and
dependency-inject it into all of our components so that we can access
the configuration properties:

``` Swift
struct HTMLRenderer {
  private let config: Configuration
    init(with configuration: Configuration) {
      config = configuration
    }
}
```

Here is an example of our `HTMLRenderer` and how it uses the `config`
property to access the `Configuration` values via the `private`,
dependency-injected, `config` property:

``` Swift
// Somewhere in our `HTMLRenderer` code
template.write(Tag(name: "title", 
                  value: config.title))
template.write(Tag(name: "meta", 
             attributes: ["content": config.metaTags.join(", "),
                          "name": "keywords"]))
```

As we continue working on our engine we also add additional
configuration properties. The RSS Feed, the sitemap generator, the
assets and so on all require additional configuration properties.

``` Swift
struct Configuration {
  ...
  // RSS Properties
  let rssAddress = "https://terhech.de/feed.rss"
  let rssTitle = "My Website Feed"
  let maxAmountOfArticlesInRSS = 10

  // Sitemap configuration
  let sitemapFilename = "sitemap.xml"

  // Copy Folders Configuration
  let foldersToCopy = ["css", "js", "img", "playgrounds"]
}
```

At first, this works great. However, after some time we decide that
we\'d like to split up our codebase into multiple frameworks. The reason
is that much of the code that we wrote (such as our `RSS` generator) can
also be used in other projects.

Now, we have the problem that most of our code is dependent on our
central `Configuration` structure. For example, if somebody just wanted
to use our `SitemapGenerator.framework`, they\'d need to initialize a
`Configuration` `struct`, even though they don\'t need 90% of the actual
configuration.

In order to solve this, we decide to split the configuration up into
many smaller configurations, each for their specific use case:

``` Swift
struct HTMLConfiguration {
  let title = "My Website"
  let address = "https://terhech.de"
  let metaTags = ["swift", "website", "furry"]
  let author = "Benedikt Terhechte"
}

struct RSSConfiguration {
  let rssAddress = "https://terhech.de/feed.rss"
  let rssTitle = "My Website Feed"
  let maxAmountOfArticlesInRSS = 10
}

struct SitemapConfiguration {
  let sitemapFilename = "sitemap.xml"
}

struct FoldersConfiguration {
  let foldersToCopy = ["css", "js", "img", "playgrounds"]
}
```

Not only does this solve our problem, we also have the added benefit of
not needing additional documentation in the source code as the names of
the `struct` types are now self-explanatory.

While this is clearly better in terms of simplifying the experience of
using our many frameworks (such as the `SitemapGenerator.framework`), it
worsens the situation for our actual main product, the static site
generator.

In there, we have many components that use more than just one of our
frameworks. They suddenly require us to dependency-inject multiple,
different, configurations in their initializer.

Consider our HTML-Renderer which internally renders the HTML file but
also uses our `RSS.framework` and `SitemapGenerator.framework` to render
the sitemap and the rss feed. It now requires three different
configurations for startup:

``` Swift
struct HTMLRenderer {
  init(htmlConfiguration: HTMLConfiguration, 
      sitemapConfiguration: SitemapConfiguration, 
      rssConfiguration: RSSConfiguration) {
    ..
  }
}
```

Clearly, this is already getting out of hand, and it may become even
worse once we incoroporate more functionality into our static site
generator.

So, how do we solve this? As always - with protocols of course.

## Protocols to the rescue

Instead of defining `struct` types for our configurations, we can
obviously also define `protocol` types:

``` Swift
protocol HTMLConfigurationProtocol {
  var title: String { get }
  var address: String { get }
  var metaTags: [String] { get }
  var author: String { get }
}

protocol RSSConfigurationProtocol {
  var rssAddress: String { get }
  var rssTitle: String { get }
  var maxAmountOfArticlesInRSS: Int { get }
}

protocol SitemapConfigurationProtocol {
  var sitemapFilename: String { get }
}

protocol FoldersConfigurationProtocol {
  var foldersToCopy: [String] { get }
}
```

So, how does this exactly solve our problem? Our renderer code still
looks just as messy, only that now we added one level of indirection:

``` Swift
struct HTMLRenderer {
  init(htmlConfiguration: HTMLConfigurationProtocol, 
      sitemapConfiguration: SitemapConfigurationProtocol, 
      rssConfiguration: RSSConfigurationProtocol) {
    ..
  }
}
```

This, however, is not our renderer\'s final form.

## Protocol Composition

Swift has a particular nifty feature that allows you to define that a
type has to conform to a number of protocols by joining them via `&`. We
can use this in our renderer to state that it requires a configuration
type that conforms to the `HTMLConfigurationProtocol`, the
`SitemapConfigurationProtocol` and the `RSSConfigurationProtocol`:

``` Swift

struct HTMLRenderer {
  init(configuration: HTMLConfigurationProtocol & 
          SitemapConfigurationProtocol & 
          RSSConfigurationProtocol) {
    ..
  }
}

```

What we\'re doing here is telling Swift that only a type that conforms
to `HTMLConfigurationProtocol`, `SitemapConfigurationProtocol`, and
`RSSConfigurationProtocol` **at the same time** is allowed to be used
for the `configuration` of the `HTMLRenderer`.

This solves our problem in a very beautiful way:

-   Our specific frameworks just know about their specific Configuration
    protocols (such as `SitemapConfigurationProtocol`).
-   Our overarching **static site generator** knows about all the
    protocols of the sub-frameworks it incorporates and can conform to
    them accordingly
-   New projects leveraging one of our frameworks can easily extend
    their existing configuration to conform to the relevant protocol and
    don\'t need to introduce a wholy new type.

Most importantly, our `Configuration` struct in our main
`Static Site Generator` is just one type again, it just conforms to
multiple protocols.
