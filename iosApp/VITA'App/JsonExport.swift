//
//  JsonExport.swift
//  VITA'App
//
//  Created by Son Pham-Ba on 10.01.23.
//  Copyright © 2023 ImTech. All rights reserved.
//

import Foundation


struct Point: Codable {
    var x: Double = 0
    var y: Double = 0
}


struct Bbox: Codable {
    var bottomLeft:  Point = Point()
    var bottomRight: Point = Point()
    var topLeft:     Point = Point()
    var topRight:    Point = Point()
}


struct DetectedText: Codable {
    var text: String
    var bbox: Bbox = Bbox()
}


func exportJson(data: [DetectedText], to: URL) {
    do {
        let jsonEncoder = JSONEncoder()
        let jsonData = try jsonEncoder.encode(data)
        let jsonString = String(data: jsonData, encoding: .utf8)!
        let path = to.path
        try jsonString.write(toFile: path, atomically: true, encoding: String.Encoding.utf8)
        print("File successfully written")
    } catch {
        print("Error exporting JSON: \(error)")
    }
}
