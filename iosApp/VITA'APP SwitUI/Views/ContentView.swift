//
//  ContentView.swift
//  VITA'APP SwitUI
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
                
                Button(action: {
                      browseFiles()
                  }) {
                      Text("Open in Files App").frame(minWidth: 0, maxWidth: .infinity)
                  }
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
    
    func browseFiles() {
        let documentsUrl = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        print(documentsUrl)
        if let sharedUrl = URL(string: "shareddocuments://\(documentsUrl.path)") {
            if UIApplication.shared.canOpenURL(sharedUrl) {
                UIApplication.shared.open(sharedUrl, options: [:])
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
