from datetime import datetime, time, date, timedelta
from math import ceil

#küsib andmed ülesande kohta
def küsi_ülesande_andmed():
    while True:
        ülesande_nimi=input('Sisestage ülesande nimi: ').strip()
        if ülesande_nimi:
            break
        print('Ülesande nimi ei sobi')
        
    while True:
        try:
            eeldatav_ajakulu=float(input('Sisestage eeldatav ajakulu selle ülesande jaoks tundides: '))
            if eeldatav_ajakulu <= 0:
                print('Ajakulu pole realistlik')
                continue
            break
        except ValueError:
            print('Palun sisestage arv')
    
    while True:
        try:
            tähtaeg=datetime.strptime(input('Sisestage ülesande tähtaeg (PP.KK.AAAA): '), '%d.%m.%Y')
            if tähtaeg.date()<=date.today():
                print('Tähtaeg on juba möödas, proovige uuesti.')
                continue
            break
        except ValueError:
            print('Vigane kuupäev, kasutage formaati PP.KK.AAAA')
    return [ülesande_nimi, eeldatav_ajakulu, tähtaeg]

#vaatab et ajavahemikud ei ületaks 23:30
def uni_on_ka_tähtis(ajavahemikud):
    uneaeg=time(23, 30)
    for ajavahemik in ajavahemikud:
        if ajavahemik[1] > uneaeg:
            ajavahemik[1] = uneaeg
            print('Uni on tähtis, ajavahemiku lõpuks määrati 23:30')
    return ajavahemikud

#kontrollib kas ajavahemikud on õigesti sisestatud ja et need ei kattuks üksteisega
def kontrolli_ajavahemikke(ajavahemikud):
    for algus, lõpp in ajavahemikud:
        if algus >= lõpp:
            return False
        
    for i in range(len(ajavahemikud)):
        for j in range(i+1, len(ajavahemikud)):
            algus1, lõpp1 = ajavahemikud[i]
            algus2, lõpp2 = ajavahemikud[j]
            if algus1 < lõpp2 and algus2 < lõpp1:
                return False
    return True


#küsib kasutajalt õppimiseks vaba aja            
def küsi_vaba_aeg():
    vaba_aeg=[]
    päevad=['esmaspäev', 'teisipäev', 'kolmapäev', 'neljapäev', 'reede', 'laupäev', 'pühapäev']
    for päev in päevad:
        while True:
            try:
                vaba=input(f'Sisestage aeg, millal saate õppida (nt 16:00-18:00)(kui on mitu ajavahemikku, eralda need komaga): {päev} ')
                ajavahemikud=[]
                if vaba:
                    for vahemik in vaba.split(','):
                        algus, lõpp = vahemik.strip().split('-')
                        algus = datetime.strptime(algus.strip(), '%H:%M').time()
                        lõpp = datetime.strptime(lõpp.strip(), '%H:%M').time()
                        ajavahemikud.append([algus, lõpp])
                ajavahemikud=uni_on_ka_tähtis(ajavahemikud)
                if kontrolli_ajavahemikke(ajavahemikud):
                    break
                print('Ajavahemikud kattuvad või on vales järjekorras')
            except ValueError:
                print('Vigane sisestus, kasutage formaati HH:MM-HH:MM')
        vaba_aeg.append([päevad.index(päev), ajavahemikud])
    return vaba_aeg


#rakendab väikese buffer aja ja tagastab ümardatult 0.5 tunni täpsusega
def aeg_parajaks(kuluv_aeg):
    a=ceil(kuluv_aeg * 1.1 *2)/2
    return a


#otsib päevad tänasest ülesande tähtajani
def aega_tähtajani(tähtaeg):
    tähtaeg=tähtaeg.date()
    täna=date.today()
    päevad_töötamiseks=[]
    while täna<tähtaeg:
        päevad_töötamiseks.append(täna)
        täna+=timedelta(days=1)
    return päevad_töötamiseks


#jagab kuupäevadele õppimise ajavahemikud
def päevas_õppida(vaba_aeg, päevad_töötamiseks):
    kuupäevad_õppimiseks=[]
    for päev in päevad_töötamiseks:
        nädalapäev=päev.weekday()
        kuupäevad_õppimiseks.append([päev, []])
        for vaba in vaba_aeg:
            if vaba[0]==nädalapäev:
                for ajavahemik in vaba[1]:
                    kuupäevad_õppimiseks[-1][1].append(ajavahemik)
    return kuupäevad_õppimiseks


#arvutab mitu tundi saab iga päev kokku õppida
def tunnid_päevas(kuupäevad_õppimiseks):
    päevade_tunnid=[]
    for päev in kuupäevad_õppimiseks:
        päeva_tunnid=0
        for ajavahemik in päev[1]:
            algus = datetime.combine(päev[0], ajavahemik[0])
            lõpp = datetime.combine(päev[0], ajavahemik[1])
            kestus = (lõpp - algus).total_seconds() / 3600
            päeva_tunnid += kestus
        päevade_tunnid.append([päev[0], päeva_tunnid])
    return päevade_tunnid


#kontrollib kas ülesande täitmiseks on piisavalt aega
def kas_on_aega(kuluv_aeg, päevade_tunnid):
    kokku_aega=0
    for päev in päevade_tunnid:
        kokku_aega+=min(päev[1], 4)
    return kokku_aega>=kuluv_aeg


#jaotab ülesandeks õppimise tunnid päevadele laiali
def aja_jaotus(kuluv_aeg, päevade_tunnid):
    jaotus=[]
    for päev in päevade_tunnid:
        if päev[1]>0:
            tunnid=päev[1]
            if tunnid>4:
                tunnid=4
            aega_järel = kuluv_aeg - tunnid
            if aega_järel <=0:
                jaotus.append([päev[0], kuluv_aeg])
                break
            else:
                jaotus.append([päev[0], tunnid])
            kuluv_aeg -= tunnid
    return jaotus


#määrab eelmise funktsiooni tundide järgi ajavahemikud õppimiseks
def määra_vahemikud(jaotus, kuupäevad_õppimiseks):
    graafik=[]
    for päev in jaotus:
        for kuupäev in kuupäevad_õppimiseks:
            if päev[0]==kuupäev[0]:
                ajavahemikud=kuupäev[1]
                jäänud_tunnid=päev[1]
                for ajavahemik in ajavahemikud:
                    algus = datetime.combine(päev[0], ajavahemik[0])
                    lõpp = datetime.combine(päev[0], ajavahemik[1])
                    kestus = (lõpp - algus).total_seconds() / 3600
                    if kestus <= jäänud_tunnid:
                        graafik.append([päev[0], algus.time(), lõpp.time()])
                        jäänud_tunnid -= kestus
                    else:
                        uus_lõpp = (algus + timedelta(hours=jäänud_tunnid)).time()
                        graafik.append([päev[0], algus.time(), uus_lõpp])
                        jäänud_tunnid = 0
                    if jäänud_tunnid <= 0:
                        break
    return graafik


def main():
    ülesande_andmed=küsi_ülesande_andmed()
    vaba_aeg=küsi_vaba_aeg()
    kuluv_aeg=aeg_parajaks(ülesande_andmed[1])
    päevad_töötamiseks=aega_tähtajani(ülesande_andmed[2])
    kuupäevad_õppimiseks=päevas_õppida(vaba_aeg, päevad_töötamiseks)
    päevade_tunnid=tunnid_päevas(kuupäevad_õppimiseks)
    if kas_on_aega(kuluv_aeg, päevade_tunnid):
        jaotus=aja_jaotus(kuluv_aeg, päevade_tunnid)
        graafik=määra_vahemikud(jaotus, kuupäevad_õppimiseks)
        print(f'Graafik ülesande "{ülesande_andmed[0]}" jaoks:')
        for päev in graafik:
            print(f'{päev[0].strftime("%d.%m.%Y")}: {päev[1].strftime("%H:%M")} - {päev[2].strftime("%H:%M")}')
    else:
        print('Kahjuks pole piisavalt aega selle ülesande jaoks.')


if __name__ == '__main__':
    main()