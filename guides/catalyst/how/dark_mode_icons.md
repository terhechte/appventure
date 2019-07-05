[frontMatter]
title = "How do I support macOS icons?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



Fortunately, each icon in the assets catalog (you're using assets catalogs, are you?) supports different varieties, including macOS. If you enable the "Mac" setting for any icon, additional slots will appear where you can add macOS specific icons to your asset. Catalyst will then automatically choose the right icons. This is what that looks like:

![](/img-content/catalyst/mac_icon_assets.png)

## General Icons

You could just use your general iOS icons on the Mac, but keep the following things in mind:
- iOS icons are scaled down 77% on macOS / Catalyst. This can add artifacts
- Many Macs still have non-retina displays (i.e. the Macbook Air 13" is still non-retina and still being sold)
- If you don't have @1x variants of your icons, Catalyst will scale down the @2x variants, creating additional artifacts
- Icons might not look as good anymore in a scaled down manner. You might want to include separate macOS icons for some use cases


## The App Icon

For a proper macOS app icon, the following sizes are needed:
- 16pt, 16pt @ 2x
- 32pt, 32pt @ 2x
- 128pt, 128pt @ 2x
- 256pt, 256pt @ 2x
- 512pt, 512pt @ 2x

That's 10 icons. However, if you don't care about the ability to add additional detail for retina variants, then you just need the following sizes - as some of those sizes overlap: 16, 32, 64, 128, 256, 512, 1024
