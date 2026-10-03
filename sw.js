// Yuki Sensei offline helper: keeps the app page and every voice clip you've played (or saved for the
// travel translator) on the phone, so they work with no internet. The page itself is always fetched fresh
// when online (auto-update keeps working); the saved copy is only used offline.
self.addEventListener("install",()=>self.skipWaiting());
self.addEventListener("activate",e=>e.waitUntil(self.clients.claim()));
self.addEventListener("fetch",e=>{
  const req=e.request,u=new URL(req.url);
  if(req.method!=="GET"||u.origin!==location.origin)return;
  if(u.pathname.includes("/audio/")){e.respondWith(audio(req,u));return;}
  if(req.mode==="navigate")e.respondWith(page(req));
});
async function page(req){
  try{const r=await fetch(req);if(r.ok){const c=await caches.open("yuki-page");await c.put("./",r.clone());}return r;}
  catch(err){const c=await caches.open("yuki-page");return(await c.match("./"))||Response.error();}
}
// Audio: from the phone if saved, else from the internet (and saved). Safari asks for byte ranges, so
// those are cut from the saved file.
async function audio(req,u){
  const c=await caches.open("yuki-audio"),key=u.origin+u.pathname;
  let hit=await c.match(key);
  if(!hit){
    try{const r=await fetch(key);if(r.status!==200)return r;await c.put(key,r.clone());hit=r;}
    catch(err){return Response.error();}
  }
  const range=req.headers.get("range");
  if(!range)return hit;
  const buf=await hit.clone().arrayBuffer(),size=buf.byteLength,m=/bytes=(\d*)-(\d*)/.exec(range);
  const start=m&&m[1]?+m[1]:0,end=m&&m[2]?Math.min(+m[2],size-1):size-1;
  return new Response(buf.slice(start,end+1),{status:206,headers:{"Content-Type":"audio/mpeg","Content-Range":`bytes ${start}-${end}/${size}`,"Content-Length":String(end-start+1),"Accept-Ranges":"bytes"}});
}
