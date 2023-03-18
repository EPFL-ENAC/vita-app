//
//  HttpClient.swift
//  OCR SwitUI
//
//  Created by Tom MERY on 18.03.23.
//

import Foundation

class HttpClient {
    let url = URL(string: "http://172.20.10.3:8080")!
    
    func sendRequest(jsonData: Data) async -> Data? {
        var request = URLRequest(url: self.url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        
        do {
            let (data, response) = try await URLSession.shared.upload(for: request, from: jsonData)
            if let response = response as? HTTPURLResponse {
                if response.statusCode == 480 {
                    print("Could not find a matching reader.")
                    return nil
                }
            }
            return data
        }
        catch {
            print("Request to server failed.")
            return nil
        }
    }
}
