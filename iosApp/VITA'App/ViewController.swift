//
//  ViewController.swift
//  VITA'App
//
//  Created by Mikhael on 25/07/2022.
//  Copyright © 2022 ImTech. All rights reserved.
//

import UIKit
import Vision
import VisionKit

class ViewController: UIViewController {
    
    private var ocrTextView = OcrTextView(frame: .zero, textContainer: nil)
    private var scanButton = ScanButton(frame: .zero)
    private var scanImageView = ScanImageView(frame: .zero)
    private var ocrRequest = VNRecognizeTextRequest(completionHandler: nil)
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        configure()
        configureOCR()
    }

    
    private func configure() {
        view.addSubview(ocrTextView)
        view.addSubview(scanImageView)
        view.addSubview(scanButton)
        
        let padding: CGFloat = 16
        NSLayoutConstraint.activate([
            scanButton.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: padding),
            scanButton.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -padding),
            scanButton.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -padding),
            scanButton.heightAnchor.constraint(equalToConstant: 50),
            
            ocrTextView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: padding),
            ocrTextView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -padding),
            ocrTextView.bottomAnchor.constraint(equalTo: scanButton.topAnchor, constant: -padding),
            ocrTextView.heightAnchor.constraint(equalToConstant: 500),
            
            scanImageView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: padding),
            scanImageView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: padding),
            scanImageView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -padding),
            scanImageView.bottomAnchor.constraint(equalTo: ocrTextView.topAnchor, constant: -padding),
            scanImageView.heightAnchor.constraint(equalToConstant: 600)
        ])
        
        scanButton.addTarget(self, action: #selector(scanDocument), for: .touchUpInside)
    }
    
    
    @objc private func scanDocument() {
        let scanVC = VNDocumentCameraViewController()
        scanVC.delegate = self
        present(scanVC, animated: true)
    }
    
    
    private func saveImage(_ image: UIImage) {
        // Save picture in local file system
        guard let png = image.pngData() else {
            print("Error: Could not get png data of image")
            return
        }
        // guard let dir = getSaveDirectory() else { return }
        do {
            let dir = getSaveDirectory()
            let path = dir.appendingPathComponent("cropped.png") // appendingPathComponent is deprecated!
            try png.write(to: path)
            print("Picture saved successfully")
        }
        catch {
            print("Error: could not save picture. \(error)")
        }
    }
    
    private func processImage(_ image: UIImage) {
        guard let cgImage = image.cgImage else { return }

        ocrTextView.text = ""
        scanButton.isEnabled = false
        
        let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        do {
            try requestHandler.perform([self.ocrRequest])
        } catch {
            print(error)
        }
    }

    
    private func configureOCR() {
        ocrRequest = VNRecognizeTextRequest { (request, error) in
            guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
        
            // Output detected text in JSON string
            /* format:
            [
                {
                    text: String,
                    bbox: {
                        bottomLeft:  [Double, Double],
                        bottomRight: [Double, Double],
                        topleft:     [Double, Double],
                        topRight:    [Double, Double]
                    }
                 }
            ]
            */
            var ocrText = "["
            for observation in observations {
                guard let topCandidate = observation.topCandidates(1).first else { return }
                
                ocrText += "{\"text\": \"\(topCandidate.string)\", "
                // create range for bounding box detection
                let startIndex = topCandidate.string.startIndex
                let endIndex = topCandidate.string.index(startIndex, offsetBy: 1)
                let range = startIndex ..< endIndex
                
                ocrText += "\"bbox\": {"
                do {
                    let bbox: VNRectangleObservation = try topCandidate.boundingBox(for: range)!
                    
                    func jsonFromCGPoint(point: CGPoint, jsonKey: String) -> String {
                        return "\"\(jsonKey)\": [\(point.x), \(point.y)]"
                    }
                    
                    ocrText += jsonFromCGPoint(point: bbox.bottomLeft,  jsonKey: "bottomLeft")  + ", "
                    ocrText += jsonFromCGPoint(point: bbox.bottomRight, jsonKey: "bottomRight") + ", "
                    ocrText += jsonFromCGPoint(point: bbox.topLeft,     jsonKey: "topLeft")     + ", "
                    ocrText += jsonFromCGPoint(point: bbox.topRight,    jsonKey: "topRight")
                } catch {} // Cannot get bounding box
                ocrText += "}},\n"
            }
            
            // remove trailing comma
            ocrText.remove(at: ocrText.index(ocrText.endIndex, offsetBy: -2))
            ocrText += "]"
            
            
            DispatchQueue.main.async {
                self.ocrTextView.text = ocrText
                self.scanButton.isEnabled = true
                //print(ocrText)
                
                // Saving detected text into file text in local file system
                do{
                    let dir = try String(contentsOf: getSaveDirectory())
                    try ocrText.write(toFile: "\(dir)/detectedText.json", atomically: true, encoding: String.Encoding.utf8)
                    print(dir)
                    print("File successfully written")
                }
                catch {
                    print("Error: \(error)")
                }
            }
        }
        
        ocrRequest.recognitionLevel = .accurate
        ocrRequest.recognitionLanguages = ["en-US", "en-GB", "fr-FR"]
        ocrRequest.usesLanguageCorrection = true
    }
}


extension ViewController: VNDocumentCameraViewControllerDelegate {
    func documentCameraViewController(_ controller: VNDocumentCameraViewController, didFinishWith scan: VNDocumentCameraScan) {
        guard scan.pageCount >= 1 else {
            controller.dismiss(animated: true)
            return
        }
        
        let image = scan.imageOfPage(at: 0)
        scanImageView.image = image
        saveImage(image)
        processImage(image)
        controller.dismiss(animated: true)
    }
    
    func documentCameraViewController(_ controller: VNDocumentCameraViewController, didFailWithError error: Error) {
        //Handle properly error
        controller.dismiss(animated: true)
    }
    
    func documentCameraViewControllerDidCancel(_ controller: VNDocumentCameraViewController) {
        controller.dismiss(animated: true)
    }
}


func getSaveDirectory() -> URL {
    return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
}

