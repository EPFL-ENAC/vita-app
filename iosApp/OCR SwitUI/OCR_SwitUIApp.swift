//
//  OCR_SwitUIApp.swift
//  OCR SwitUI
//
//  Created by Tom MERY on 10.03.23.
//

import SwiftUI

@main
struct OCR_SwitUIApp: App {
    @StateObject private var fileController = FileController()
    @StateObject private var client = HttpClient()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(fileController)
                .environmentObject(client)
        }
    }
}
