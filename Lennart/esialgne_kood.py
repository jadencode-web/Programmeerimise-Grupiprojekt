from datetime import datetime, time, date, timedelta
from math import ceil


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
            if tähtaeg.date()<=datetime.today():
                print('Tähtaeg on juba möödas, proovige uuesti.')
                continue
            break
        except ValueError:
            print('Vigane kuupäev, kasutage formaati PP.KK.AAAA')
    return [ülesande_nimi, eeldatav_ajakulu, tähtaeg]


def uni_on_ka_tähtis(ajavahemikud):
    uneaeg=time(23, 30)
    for ajavahemik in ajavahemikud:
        if ajavahemik[1] > uneaeg:
            ajavahemik[1] = uneaeg
            print('Uni on tähtis, ajavahemiku lõpuks määrati 23:30')
    return ajavahemikud

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


def aeg_parajaks(kuluv_aeg):
    a=ceil(kuluv_aeg * 1.1 *2)/2
    return a


def aega_tähtajani(tähtaeg):
    täna=date.today()
    päevad_töötamiseks=[]
    while täna<tähtaeg:
        päevad_töötamiseks.append(täna)
        täna+=timedelta(days=1)
    return päevad_töötamiseks