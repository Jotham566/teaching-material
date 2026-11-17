// Local Apple Vision OCR, explicitly separate from the historical Tesseract experiment.
import Foundation
import Vision
var outputs:[[String:Any]]=[]
for file in CommandLine.arguments.dropFirst() {
    let request=VNRecognizeTextRequest()
    request.recognitionLevel = .fast
    request.usesCPUOnly = true
    request.revision = VNRecognizeTextRequestRevision2
    request.recognitionLanguages = ["en-US"]
    request.usesLanguageCorrection = false
    do {
        try VNImageRequestHandler(url:URL(fileURLWithPath:file),options:[:]).perform([request])
        let lines=(request.results ?? []).compactMap { $0.topCandidates(1).first }
        outputs.append(["file":file,"text":lines.map{$0.string}.joined(separator:"\n"),"line_confidences":lines.map{Double($0.confidence)},"error":NSNull()])
    } catch { outputs.append(["file":file,"text":"","error":String(describing:error)]) }
}
let result:[String:Any] = ["engine":"Apple Vision VNRecognizeTextRequest","configuration":"fast, revision 2, CPU only, en-US, language correction off","system":ProcessInfo.processInfo.operatingSystemVersionString,"images":outputs]
let data=try JSONSerialization.data(withJSONObject:result,options:[.prettyPrinted,.sortedKeys])
print(String(data:data,encoding:.utf8)!)
