import page from './page.mjs';
const keyPattern=/^CML311[123]\|TEST[12]$/;
const headers={'Cache-Control':'no-store, private','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer'};
const json=(value,status=200)=>new Response(JSON.stringify(value),{status,headers:{...headers,'Content-Type':'application/json; charset=utf-8'}});
async function limitedText(request,limit){
 const reader=request.body?.getReader();if(!reader)return '';
 const chunks=[];let size=0;
 try{while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>limit){await reader.cancel();throw Error('too large');}chunks.push(value);}}
 finally{reader.releaseLock();}
 const bytes=new Uint8Array(size);let at=0;for(const chunk of chunks){bytes.set(chunk,at);at+=chunk.length;}return new TextDecoder().decode(bytes);
}
export async function handle(request,env,upstream=fetch){
 const url=new URL(request.url);
 if(url.pathname==='/'&&(request.method==='GET'||request.method==='HEAD')){
  const key=url.searchParams.get('test')||'';
  if(!keyPattern.test(key))return new Response('Open the course/test link provided by your lecturer.',{status:400,headers});
  return new Response(request.method==='HEAD'?null:page.replace('__TEST_KEY_JSON__',JSON.stringify(key)),{headers:{...headers,'Content-Type':'text/html; charset=utf-8','Content-Security-Policy':"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"}});
 }
 if(url.pathname!=='/api/files')return json({ok:false,error:'Page not found.'},404);
 if(request.method!=='POST')return json({ok:false,error:'Use Get my test files.'},405);
 if(request.headers.get('Origin')!==url.origin)return json({ok:false,error:'Open your lecturer’s test page and try again.'},403);
 if(!(request.headers.get('Content-Type')||'').startsWith('application/json'))return json({ok:false,error:'Invalid request.'},415);
 let input;
 try{
  const body=JSON.parse(await limitedText(request,8192));
  input={test:body.test,name:body.name,email:body.email,registration:body.registration};
  if(!keyPattern.test(input.test))throw Error();
  for(const [key,max] of [['name',160],['email',254],['registration',160]]){
   if(typeof input[key]!=='string'||!input[key].trim()||input[key].length>max||/[\x00-\x1f\x7f]/.test(input[key]))throw Error();
   input[key]=input[key].trim();
  }
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.email))throw Error();
 }catch{return json({ok:false,error:'Check your name, Google email and Student Registration Number.'},400);}
 if(!env.PORTAL_GATEWAY_KEY||env.PORTAL_GATEWAY_KEY.length<32)return json({ok:false,error:'Portal connection unavailable. Tell your lecturer.'},503);
 try{
  const backend=new URL(env.APPS_SCRIPT_URL);
  if(backend.origin!=='https://script.google.com'||!/^\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(backend.pathname)||backend.search)throw Error();
  // Only this server sees Google redirects. No browser cookies or credentials are forwarded.
  const response=await upstream(backend.href,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({secret:env.PORTAL_GATEWAY_KEY,input}),redirect:'follow',signal:AbortSignal.timeout(25000)});
  if(!response.ok)throw Error();
  const data=JSON.parse(await limitedText(response,4*1024*1024));
  if(data.ok!==true){if(data.ok!==false||typeof data.error!=='string')throw Error();return json({ok:false,error:data.error},409);}
  const result=data.result;
  if(result?.course+'|'+result?.test!==input.test||!['notebook','csv','instructions','deadline','notebookName','csvName'].every(k=>typeof result[k]==='string'))throw Error();
  return json({ok:true,result});
 }catch{return json({ok:false,error:'The connection could not complete. Try again using the same details. If it continues, tell your lecturer.'},502);}
}
export default {fetch:(request,env)=>handle(request,env)};
