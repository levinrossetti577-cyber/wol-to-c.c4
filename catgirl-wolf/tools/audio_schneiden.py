# Erwartet full.wav im selben Ordner: ffmpeg -i <deine.mp3> -ac 1 -ar 44100 full.wav ; Ausgabe nach out/
import subprocess, json
src='full.wav'
# (name, start, end, target_peak_db, role, beschreibung)
cuts=[
 ("meow_idle_1",   0.99,1.67,-3,"ambient","kurzes helles 'nya~', Tonhöhe steigt und fällt (ca. 400→750→420 Hz)"),
 ("meow_growl_1",  2.03,3.45,-3,"growl","startet tief und gepresst (~240–300 Hz), steigt dann zu 'nyaa' an – ernstester Laut der Aufnahme"),
 ("meow_idle_2",   3.88,4.52,-3,"ambient/hurt","hohes, kurzes 'nya' (~600–660 Hz), fallend"),
 ("meow_whine_1",  5.19,5.49,-6,"whine","sehr leiser, kurzer fallender Laut (440→350 Hz)"),
 ("meow_bark_1",   5.61,6.27,-2,"ambient(bark)","energisches 'nya!' mit schnellem Anstieg auf ~700 Hz"),
 ("meow_death_1",  7.31,8.39,-3,"death","längeres, langsam abfallendes Miauen (580→350 Hz), wird leiser"),
 ("meow_whine_2",  8.70,9.06,-6,"whine/pant","leiser, kurzer flacher Laut (~345 Hz)"),
 ("meow_pant_1",   9.27,9.56,-12,"pant","stimmloser Atemhauch, kein Ton erkennbar"),
 ("meow_hurt_1",  10.24,10.81,-2,"hurt/bark","lautester Laut, schneller hoher Ansatz (~760 Hz), abrupter Abfall – klingt erschrocken"),
 ("meow_howl_1",  11.47,14.07,-3,"howl","langgezogenes Miauen, 2,5 s, steigt von 315 auf 450 Hz und klingt zweiteilig aus"),
 ("meow_idle_3",  14.59,15.19,-3,"ambient(bark)","helles 'nya' mit Anstieg auf ~670 Hz"),
]
import numpy as np, scipy.io.wavfile as w
sr,x=w.read(src); x=x.astype(float)/32768
rows=[]
for n,a,b,pk,role,desc in cuts:
    s=x[int(a*sr):int(b*sr)]
    gain=pk-20*np.log10(abs(s).max())
    d=b-a
    af=f"atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d-0.04:.3f}:d=0.04,volume={gain:.2f}dB"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i",src,"-af",af,"-ac","1","-ar","44100","-c:a","libvorbis","-q:a","6",f"out/{n}.ogg"],check=True)
    rows.append(dict(file=n+".ogg",start=a,end=b,dur=round(d,2),gain=round(gain,1),role=role,desc=desc))
json.dump(rows,open('cuts.json','w'),ensure_ascii=False,indent=1)
