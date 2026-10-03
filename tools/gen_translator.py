# Records the travel translator's sentences in Ryusei's voice (louder than lesson audio, for noisy places).
# Usage:
#   docker run -d --rm -p 50021:50021 voicevox/voicevox_engine:cpu-latest
#   python3 tools/gen_translator.py translator.json audio
# translator.json = JSON list of [kana shown, spoken form] from trRecList() in index.html.
# File name = recId(kana shown) (code points in hex joined by "_"); existing files are kept.
import json,urllib.request,urllib.parse,subprocess,os,sys,concurrent.futures as cf
items=json.load(open(sys.argv[1]));out=sys.argv[2]+"/ryusei";SPEAKER=13
os.makedirs(out,exist_ok=True)
def fid(t):return "_".join(format(ord(c),"x") for c in t)
def gen(item):
    shown,spoken=item;path=f"{out}/{fid(shown)}.mp3"
    if os.path.exists(path):return 0
    q=urllib.request.urlopen(urllib.request.Request("http://localhost:50021/audio_query?"+urllib.parse.urlencode({"text":spoken,"speaker":SPEAKER}),method="POST")).read()
    q=json.loads(q);q["speedScale"]=0.95;q["volumeScale"]=1.6;q["prePhonemeLength"]=0.08;q["postPhonemeLength"]=0.15;q["outputSamplingRate"]=24000
    wav=urllib.request.urlopen(urllib.request.Request(f"http://localhost:50021/synthesis?speaker={SPEAKER}",data=json.dumps(q).encode(),headers={"Content-Type":"application/json"})).read()
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i","pipe:0","-af","alimiter=limit=0.95","-ac","1","-ar","24000","-b:a","40k",path],input=wav,check=True)
    return 1
with cf.ThreadPoolExecutor(3) as ex:print("generated",sum(ex.map(gen,items)))
