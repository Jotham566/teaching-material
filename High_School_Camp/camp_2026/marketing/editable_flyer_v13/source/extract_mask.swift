import Foundation
import Vision
import CoreImage
let handler=VNImageRequestHandler(url: URL(fileURLWithPath:CommandLine.arguments[1]))
let req=VNGenerateForegroundInstanceMaskRequest()
try handler.perform([req])
guard let result=req.results?.first else {fatalError("No foreground mask")}
let buffer=try result.generateScaledMaskForImage(forInstances:result.allInstances,from:handler)
try CIContext().writePNGRepresentation(of:CIImage(cvPixelBuffer:buffer),to:URL(fileURLWithPath:CommandLine.arguments[2]),format:.RGBA8,colorSpace:CGColorSpaceCreateDeviceRGB())
print("Foreground mask extracted")
