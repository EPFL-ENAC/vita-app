//
//  Saving.swift
//  VITA'APP SwitUI
//
//  Created by Tom MERY on 10.03.23.
//

import Foundation
import UIKit


let JPEG_QUALITY = 0.8


func getSaveDirectory() -> URL {
    return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
}


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
