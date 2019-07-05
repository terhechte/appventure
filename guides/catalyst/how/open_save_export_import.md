[frontMatter]
title = "create file open / save / export / import dialogs?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I create file open / save / export / import dialogs

For these actions, you can use the `UIDocumentPickerViewController` or `UIDocumentBrowserViewController` controllers. Here is a quick example of using a `UIDocumentPickerViewController` to allow the user to export JSON data to disk.

Note, in order for this to work, you need to have the "User Selected File" permission in [the macOS sandbox](how/sandbox.md) set to `Read` or `Read/Write` depending on your use case.

``` swift
func exportJSONData(_ data: Data) {
   let filename = "Export.json"

   // Get a path in our document directory to temporarily store the data in
   guard let exportURL = FileManager.default
           .urls(for: .documentDirectory, in: .userDomainMask)
           .first?.appendingPathComponent(filename) else { return }

   // Write the data out into the file
   try? data.write(to: exportURL)

   // Present the save controller. We've set it to `exportToService` in order
   // to export the data
   let controller = UIDocumentPickerViewController(url: filePath, in: UIDocumentPickerMode.exportToService)
   present(controller, animated: true) {
       // Once we're done, delete the temporary file
       try? FileManager.default.removeItem(at: filePath)
   }
}
```

Similarly, for importing data, you would use `.import` as in:

``` swift
let controller = UIDocumentPickerViewController(url: filePath, in: .import)
```
