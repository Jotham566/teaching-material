import Foundation
import CoreImage
import AppKit
let filter = CIFilter(name: "CIQRCodeGenerator")!
filter.setValue(Data("https://forms.gle/n8XLwbK1QxcUsRnx5".utf8), forKey: "inputMessage")
filter.setValue("M", forKey: "inputCorrectionLevel")
let qr = filter.outputImage!
let padded = qr.composited(over: CIImage(color: CIColor.white).cropped(to: qr.extent.insetBy(dx: -4, dy: -4)))
let normalized = padded.transformed(by: CGAffineTransform(translationX: 4, y: 4)).transformed(by: CGAffineTransform(scaleX: 20, y: 20))
try CIContext().writePNGRepresentation(of: normalized, to: URL(fileURLWithPath: CommandLine.arguments[1]), format: .RGBA8, colorSpace: CGColorSpaceCreateDeviceRGB())
print("Registration QR generated")
