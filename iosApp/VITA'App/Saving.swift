//
//  Saving.swift
//  VITA'App
//
//  Created by Son Pham-Ba on 19.01.23.
//  Copyright © 2023 ImTech. All rights reserved.
//

import Foundation
import UIKit


let JPEG_QUALITY = 0.8


func getSaveDirectory() -> URL {
    return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
}


// TODO: keep track of last generated filename and check for uniqueness
func generateNewFilename() -> String {
    let currentDate = Date()
    let formatter = DateFormatter()
    formatter.dateFormat = "yyyy-MM-dd HH-mm-ssSSS"
    // force 24h format
    formatter.locale = Locale(identifier: "en_US_POSIX")
    let filename = formatter.string(from: currentDate)
    return filename
}


func generatePath(_ filename: String, _ fileExtension: String) -> URL {
    let dir = getSaveDirectory()
    let path = dir.appendingPathComponent("\(filename).\(fileExtension)", isDirectory: false)
    return path
}


func saveImage(_ image: UIImage, _ path: URL) {
    // Save picture in local file system
    guard let jpg = image.jpegData(compressionQuality: JPEG_QUALITY) else {
        print("Error: Could not get jpg data of image")
        return
    }
    
    do {
        try jpg.write(to: path)
        print("Picture saved successfully")
    }
    catch {
        print("Error: could not save picture. \(error)")
    }
}
