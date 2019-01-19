import folium
import pandas

pdSehirNufuslar=pandas.read_csv("sehirler.csv")
sehir=list(pdSehirNufuslar["sehir"])
enlem=list(pdSehirNufuslar["enlem"])
boylam=list(pdSehirNufuslar["boylam"])
nufus=list(pdSehirNufuslar["nufus"])


def Renklendir(sayi):
    if sayi <500000:
        return "green"
    elif 500000 <=sayi <1000000:
        return "blue"
    else:
        return "red"

    
harita=folium.Map(location=[38.9597594, 34.9249653],zoom_start=7,tiles="Mapbox Control Room")
nufusHaritasi=folium.FeatureGroup(name="Nufus Haritasi")

for il,en,boy,nuf in zip(sehir,enlem,boylam,nufus):
    renk=Renklendir(int(nuf.replace(".","")))
    nufusHaritasi.add_child(folium.Marker(location=[en,boy],tooltip=(il+"  nüfus:"+nuf),icon=folium.Icon(color=renk)))



sehirIndex=pdSehirNufuslar.set_index("sehir")
def NufusKontrol(shr):
    sonuc=int(sehirIndex.loc[shr, 'nufus'].replace(".",""))
    return Renklendir(sonuc)


ilSinirlari=folium.FeatureGroup(name="İl sınırları")

ilSinirlari.add_child(folium.GeoJson(open("turkey-il-sinirlar.json","r",encoding="utf-8-sig").read(),
style_function=lambda il: {'fillColor':NufusKontrol(il["properties"]["Name"])}))


harita.add_child(nufusHaritasi)    
harita.add_child(ilSinirlari)
harita.add_child(folium.LayerControl())
harita.save("turkey.html")
