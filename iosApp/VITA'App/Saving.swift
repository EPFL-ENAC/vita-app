//
//  Saving.swift
//  VITA'App
//
//  Created by Son Pham-Ba on 19.01.23.
//  Copyright © 2023 ImTech. All rights reserved.
//

import Foundation


func getSaveDirectory() -> URL {
    return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
}


/** Structure for filename generation */
class Filename {
    private var filename = ""
    
    func generate() {
        let currentDate = Date()
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH-mm-ssSSS"
        // force 24h format
        formatter.locale = Locale(identifier: "en_US_POSIX")
        filename = formatter.string(from: currentDate)
    }
    
    func get() -> String {
        return filename
    }
}

let filename = Filename()
