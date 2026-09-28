import Foundation
import Vision
import CoreImage
import AppKit
let input=URL(fileURLWithPath:CommandLine.arguments[1])
let output=URL(fileURLWithPath:CommandLine.arguments[2])
let handler=VNImageRequestHandler(url:input)
let request=VNGenerateForegroundInstanceMaskRequest()
try handler.perform([request])
guard let obs=request.results?.first else {fatalError("No foreground detected")}
let masked=try obs.generateMaskedImage(ofInstances:obs.allInstances,from:handler,croppedToInstancesExtent:false)
let ci=CIImage(cvPixelBuffer:masked)
try CIContext().writePNGRepresentation(of:ci,to:output,format:.RGBA8,colorSpace:CGColorSpaceCreateDeviceRGB())
print("Original-photo foreground exported; no image synthesis")
