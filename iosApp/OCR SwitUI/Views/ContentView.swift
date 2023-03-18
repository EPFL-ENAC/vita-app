//
//  ContentView.swift
//  OCR SwitUI
//
//  Created by Tom MERY on 10.03.23.
//

import SwiftUI

struct ContentView: View {
    @State private var showScannerSheet = false
    @State private var ocrData: Data?
    
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
            .onChange(of: ocrData) { jsonData in
                if let data = jsonData {
                    Task {
                        await makeServerRequest(data: data)
                    }
                }
            }
        }
    }
    
    private func makeScannerView() -> ScannerView {
        ScannerView(completion: {
            jsonData in
            self.ocrData = jsonData
            self.showScannerSheet = false
        })
    }
    
    func makeServerRequest(data: Data) async {
        let client = HttpClient()
        await client.sendRequest(jsonData: data)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
