//
//  HttpClient.swift
//  OCR SwitUI
//
//  Created by Tom MERY on 18.03.23.
//

import Foundation

class HttpClient {
    let url = URL(string: "https://reqres.in/api/cupcakes")!
    
    func sendRequest(jsonData: Data) async {
        var request = URLRequest(url: self.url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        
        do {
            let (data, _) = try await URLSession.shared.upload(for: request, from: jsonData)
            print(data)
        }
        catch {
            print("Request to server failed.")
        }
    }
}
