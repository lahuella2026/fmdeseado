# Baja los titulares de Google Noticias y los guarda en titulares.json
import json, urllib.request, email.utils, datetime, xml.etree.ElementTree as ET
FUENTES = {
  "Puerto Deseado": "https://news.google.com/rss/search?q=%22Puerto+Deseado%22+when:3d&hl=es-419&gl=AR&ceid=AR:es-419",
  "Santa Cruz": "https://news.google.com/rss/search?q=%22Santa+Cruz%22+provincia+when:2d&hl=es-419&gl=AR&ceid=AR:es-419",
  "País": "https://news.google.com/rss?hl=es-419&gl=AR&ceid=AR:es-419",
}
MAX_DIAS = 3
ahora = datetime.datetime.now(datetime.timezone.utc)
salida = {"actualizado": ahora.isoformat(), "fuentes": {}}
for nombre, url in FUENTES.items():
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        raiz = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
        for it in raiz.iter("item"):
            fecha = email.utils.parsedate_to_datetime(it.findtext("pubDate"))
            if (ahora - fecha).days >= MAX_DIAS: continue
            items.append({"title": it.findtext("title") or "", "link": it.findtext("link") or "",
                          "fuente": it.findtext("source") or "", "fecha": fecha.isoformat()})
    except Exception as e:
        print("Error en", nombre, e)
    items.sort(key=lambda x: x["fecha"], reverse=True)
    salida["fuentes"][nombre] = items[:30]
    print(nombre, len(items))
json.dump(salida, open("titulares.json", "w"), ensure_ascii=False, indent=1)
