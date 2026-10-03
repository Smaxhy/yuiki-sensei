# Records the free Japanese practice audio in audio/<voice>/ with VOICEVOX.
# Usage:
#   docker run -d --rm -p 50021:50021 voicevox/voicevox_engine:cpu-latest
#   python3 tools/gen_audio.py texts.json audio
# texts.json = JSON list of every CARDS[*].say value (only missing files are generated).
# File name = each character's code point in hex joined by "_" (same as recId() in index.html).
import json,urllib.request,urllib.parse,subprocess,os,sys,concurrent.futures as cf
texts=json.load(open(sys.argv[1]));out=sys.argv[2]
VOICES={"himari":14,"ryusei":13}
def fid(t):return "_".join(format(ord(c),"x") for c in t)
def gen(v,sid,t):
    path=f"{out}/{v}/{fid(t)}.mp3"
    if os.path.exists(path):return 0
    q=urllib.request.urlopen(urllib.request.Request("http://localhost:50021/audio_query?"+urllib.parse.urlencode({"text":t,"speaker":sid}),method="POST")).read()
    q=json.loads(q);q["speedScale"]=0.95;q["prePhonemeLength"]=0.08;q["postPhonemeLength"]=0.12;q["outputSamplingRate"]=24000
    wav=urllib.request.urlopen(urllib.request.Request(f"http://localhost:50021/synthesis?speaker={sid}",data=json.dumps(q).encode(),headers={"Content-Type":"application/json"})).read()
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i","pipe:0","-ac","1","-ar","24000","-b:a","40k",path],input=wav,check=True)
    return 1
for v in VOICES:os.makedirs(f"{out}/{v}",exist_ok=True)
n=0
with cf.ThreadPoolExecutor(3) as ex:
    for r in ex.map(lambda a:gen(*a),[(v,s,t) for v,s in VOICES.items() for t in texts]):n+=r
print("generated",n)
