//
//  HttpClient.swift
//  OCR SwitUI
//
//  Created by Tom MERY on 18.03.23.
//

import Foundation

class HttpClient {
    let url = URL(string: "http://172.20.10.3:8080")!
    
    func sendRequest(jsonData: Data) async -> [[String: String]]? {
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

            if let structuredData = parseResponse(data: data) {
                return structuredData
            }
            else {
                return nil
            }
        }
        catch {
            print("Request to server failed.")
            return nil
        }
    }
    
    func parseResponse(data: Data) -> [[String: String]]? {
        do {
            let jsonArray = try JSONSerialization.jsonObject(with: data, options: []) as! [[String: String]]
            return jsonArray
        } catch {
            print("Error decoding JSON: \(error.localizedDescription)")
            return nil
        }
    }
}
