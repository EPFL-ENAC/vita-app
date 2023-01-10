//
//  JsonExport.swift
//  VITA'App
//
//  Created by Son Pham-Ba on 10.01.23.
//  Copyright © 2023 ImTech. All rights reserved.
//

import Foundation


struct Bbox: Codable {
    var bottomLeft:  [Double] = []
    var bottomRight: [Double] = []
    var topLeft:     [Double] = []
    var topRight:    [Double] = []
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
