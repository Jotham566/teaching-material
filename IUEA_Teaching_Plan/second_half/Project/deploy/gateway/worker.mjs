import page from './page.mjs';
import projectPage from './project_page.mjs';
const projectKeyPattern=/^CML311[123]\|ML_(PROJECT|REHEARSAL)$/;
const keyPattern=/^CML311[123]\|(TEST1|ML_PROJECT|ML_REHEARSAL)$/;
const retiredKeyPattern=/^CML311[123]\|TEST2$/;
const retiredTestMessage='Practical Test 2 was withdrawn and replaced by the Engineering ML final project. Follow your lecturer’s project instructions.';
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
   if(retiredKeyPattern.test(key))return new Response(retiredTestMessage,{status:410,headers});
   if(!keyPattern.test(key))return new Response('Open the course/Test 1 link provided by your lecturer.',{status:400,headers});
  return new Response(request.method==='HEAD'?null:(projectKeyPattern.test(key)?projectPage:page).replace('__TEST_KEY_JSON__',JSON.stringify(key)),{headers:{...headers,'Content-Type':'text/html; charset=utf-8','Content-Security-Policy':"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"}});
 }
 // ML project collection (14 November 2026): the class-list check while typing, the silent backups from Colab, and the entry page's
 // Check my work, I have finished and status. The allocation code (issued once, unguessable) identifies the attempt; no token.
 if(['/api/check','/api/backup','/api/mywork','/api/finish','/api/status'].includes(url.pathname)){
  if(request.method!=='POST')return json({ok:false,error:'Use POST.'},405);
  if(!(request.headers.get('Content-Type')||'').startsWith('application/json'))return json({ok:false,error:'Invalid request.'},415);
  // Backups come from Colab's Python, which sends no Origin. Everything else comes from the entry page itself (same origin only).
  if(url.pathname!=='/api/backup'&&request.headers.get('Origin')!==url.origin)return json({ok:false,error:'Open your lecturer’s test page and try again.'},403);
  let body;
  try{body=JSON.parse(await limitedText(request,url.pathname==='/api/backup'?12*1024*1024:4096));}catch{return json({ok:false,error:'The request is too large or not readable.'},400);}
  const attempt=typeof body.attempt==='string'&&/^T-[A-Za-z0-9-]{8,64}$/.test(body.attempt)?body.attempt:'';
  let target,payload;
  if(url.pathname==='/api/check'){
   if(!projectKeyPattern.test(String(body.test||''))||typeof body.registration!=='string'||!body.registration.trim()||body.registration.length>40||/[\x00-\x1f\x7f]/.test(body.registration))return json({ok:false,error:'Enter your registration number.'},400);
   if(!env.PORTAL_GATEWAY_KEY||env.PORTAL_GATEWAY_KEY.length<32)return json({ok:false,error:'Portal connection unavailable. Tell your lecturer.'},503);
   target=env.APPS_SCRIPT_URL;payload={secret:env.PORTAL_GATEWAY_KEY,action:'check',input:{test:body.test,registration:body.registration.trim()}};
  }else{
   if(!env.COLLECTOR_GATEWAY_KEY||env.COLLECTOR_GATEWAY_KEY.length<32||!env.COLLECTOR_URL)return json({ok:false,error:'The collection service is unavailable. Tell your lecturer.'},503);
   if(!attempt)return json({ok:false,error:'Open your project from the entry page first.'},400);
   const action={'/api/backup':'backup','/api/mywork':'checkwork','/api/finish':'finish','/api/status':'status'}[url.pathname];
   if(action==='backup'&&(typeof body.notebook!=='string'||typeof body.href!=='string'||body.href.length>500))return json({ok:false,error:'Invalid backup.'},400);
   payload={secret:env.COLLECTOR_GATEWAY_KEY,action,attempt};
   if(action==='backup'){payload.notebook=body.notebook;payload.href=body.href;}
   target=env.COLLECTOR_URL;
  }
  try{
   const backend=new URL(target);
   if(backend.origin!=='https://script.google.com'||!/^\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(backend.pathname)||backend.search)throw Error();
   const response=await upstream(backend.href,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),redirect:'follow',signal:AbortSignal.timeout(28000)});
   if(!response.ok)throw Error();
   const data=JSON.parse(await limitedText(response,64*1024));
   if(data.ok===true&&data.result&&typeof data.result==='object')return json({ok:true,result:data.result});
   if(data.ok===false&&typeof data.error==='string')return json({ok:false,error:data.error,result:data.result&&typeof data.result==='object'?data.result:undefined},409);
   throw Error();
  }catch{return json({ok:false,error:'The connection could not complete. Try again in a minute. If it continues, tell your lecturer.'},502);}
 }
 if(url.pathname!=='/api/files')return json({ok:false,error:'Page not found.'},404);
 if(request.method!=='POST')return json({ok:false,error:'Use Get my test files.'},405);
 if(request.headers.get('Origin')!==url.origin)return json({ok:false,error:'Open your lecturer’s test page and try again.'},403);
 if(!(request.headers.get('Content-Type')||'').startsWith('application/json'))return json({ok:false,error:'Invalid request.'},415);
 let input;
 try{
  const body=JSON.parse(await limitedText(request,8192));
  if(retiredKeyPattern.test(body.test))return json({ok:false,error:retiredTestMessage},410);
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
