//
//  ContentView.swift
//  OCR SwitUI
//
//  Created by Tom MERY on 10.03.23.
//

import SwiftUI

struct ContentView: View {
    @State private var showScannerSheet = false
    
    var body: some View {
        NavigationView{
            VStack {
                Button("Scan",
                       action: {self.showScannerSheet = true}
                )
            }
            .sheet(isPresented: $showScannerSheet, content: {
                self.makeScannerView()
            })
        }
    }
    
    private func makeScannerView() -> ScannerView {
        ScannerView(completion: {
            _ in
            self.showScannerSheet = false
        })
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
