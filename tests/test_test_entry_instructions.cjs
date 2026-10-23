const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync('IUEA_Teaching_Plan/test_portal/Index.html','utf8');
for(const course of ['CML3111','CML3112','CML3113']){
 const nodes={};let submit,success;
 for(const [,id] of html.matchAll(/id="([^"]+)"/g))nodes[id]={value:'synthetic',hidden:false,scrollIntoView(){},addEventListener(_,fn){submit=fn;},set textContent(v){this.text=v;if(id==='openStep')delete nodes.notebookLabel;},get textContent(){return this.text;}};
 const context={document:{getElementById:id=>nodes[id]||null},Date,Math,Blob,URL:{createObjectURL:()=> 'blob:synthetic',revokeObjectURL(){}},setInterval:()=>1,clearInterval(){},google:{script:{run:{withSuccessHandler(fn){success=fn;return {withFailureHandler(){return {requestTestFiles(){}}}}}}}}};
 vm.runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1].replace('<?!= JSON.stringify(testKey) ?>',JSON.stringify(course+'|TEST1')),context);
 const result={notebook:'{}',csv:'data',instructions:'guide',notebookName:'TEST1_student.ipynb',csvName:'engineering_data.csv',deadline:'deadline',personalDeadline:new Date(Date.now()+10000).toISOString(),serverNow:new Date().toISOString(),colabUrl:'https://colab.research.google.com/drive/synthetic'};
 for(let i=0;i<2;i++){submit({preventDefault(){}});success(result);assert.equal(nodes.get.disabled,false);assert.equal(nodes.files.hidden,false);assert.match(nodes.openStep.textContent,/saved copy/);assert.match(nodes.csv.textContent,/Backup/);}
}
console.log('PASS: three Test 1 pages can start/resume twice; backup labels and saved-copy instructions remain usable.');
