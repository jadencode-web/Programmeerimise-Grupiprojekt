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
            if tähtaeg.date()<=date.today():
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
    tähtaeg=tähtaeg.date()
    täna=date.today()
    päevad_töötamiseks=[]
    while täna<tähtaeg:
        päevad_töötamiseks.append(täna)
        täna+=timedelta(days=1)
    return päevad_töötamiseks


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


def lisa_pausid(yhe_paeva_ajad):
    """Esimene paus tuleb 90 min pärast õppimise algust, siis iga 2 tunni järel uuesti."""
    if len(yhe_paeva_ajad) > 0:
        algus = min(yhe_paeva_ajad)
        lopp = max(yhe_paeva_ajad)
        for paus in range(algus + 90, lopp + 30, 120):
            if paus in yhe_paeva_ajad:
                yhe_paeva_ajad.remove(paus)
    return yhe_paeva_ajad


def leia_vabad_ajad(kuupäevad_õppimiseks, kell_praegu):
    """Tagastab iga päeva vabad pooltunnid koos pausidega. [0] on täna, [1] on homme jne."""
    vabad_ajad = []
    for päev in kuupäevad_õppimiseks:
        yhe_paeva_ajad = set()
        for ajavahemik in päev[1]:
            algus = ajavahemik[0].hour * 60 + ajavahemik[0].minute
            lopp = ajavahemik[1].hour * 60 + ajavahemik[1].minute
            yhe_paeva_ajad = yhe_paeva_ajad | set(range(algus, lopp, 30))
        vabad_ajad.append(yhe_paeva_ajad)

    kell_praegu_minutites = kell_praegu.hour * 60 + kell_praegu.minute
    tanased_moodunud_ajad = set(range(0, kell_praegu_minutites, 30))
    vabad_ajad[0] = vabad_ajad[0] - tanased_moodunud_ajad

    for paev in range(len(vabad_ajad)):
        yhe_paeva_ajad = vabad_ajad[paev]
        vabad_ajad[paev] = lisa_pausid(yhe_paeva_ajad)

    return vabad_ajad


def vaba_aeg_kokku_minutites(vabad_ajad, paevi_tahtajani):
    """Tagastab, mitu minutit on enne tähtaega kokku vaba."""
    kokku = 0
    for paev in range(paevi_tahtajani):
        kokku = kokku + len(vabad_ajad[paev]) * 30
    return kokku


def paiguta_ylesanne(vabad_ajad, ylesande_nimi, kulub_minuteid, paevi_tahtajani):
    """Jagab ülesande päevade peale: igale päevale kuni 90 min, vajadusel rohkem."""
    ylesande_ajad = []
    paigutamata_minuteid = kulub_minuteid

    while paigutamata_minuteid > 0 and vaba_aeg_kokku_minutites(vabad_ajad, paevi_tahtajani) > 0:
        for paev in range(paevi_tahtajani):
            yhe_paeva_ajad = sorted(vabad_ajad[paev])
            mitu_pooltundi = min(3, paigutamata_minuteid // 30, len(yhe_paeva_ajad))

            for pooltund in yhe_paeva_ajad[:mitu_pooltundi]:
                vabad_ajad[paev].remove(pooltund)
                ylesande_ajad.append({"nimi": ylesande_nimi, "paev": paev, "kellaaeg": pooltund})

            paigutamata_minuteid = paigutamata_minuteid - mitu_pooltundi * 30

    return ylesande_ajad


def main():
    ülesande_andmed=küsi_ülesande_andmed()
    vaba_aeg=küsi_vaba_aeg()
    kuluv_aeg=aeg_parajaks(ülesande_andmed[1])
    päevad_töötamiseks=aega_tähtajani(ülesande_andmed[2])
    kuupäevad_õppimiseks=päevas_õppida(vaba_aeg, päevad_töötamiseks)

    vabad_ajad = leia_vabad_ajad(kuupäevad_õppimiseks, datetime.now().time())
    kulub_minuteid = int(kuluv_aeg * 60)
    paevi_tahtajani = len(päevad_töötamiseks)

    if vaba_aeg_kokku_minutites(vabad_ajad, paevi_tahtajani) >= kulub_minuteid:
        ylesande_ajad = paiguta_ylesanne(vabad_ajad, ülesande_andmed[0], kulub_minuteid, paevi_tahtajani)
        print(f'Graafik ülesande "{ülesande_andmed[0]}" jaoks:')
        for paev in range(paevi_tahtajani):
            for kirje in ylesande_ajad:
                if kirje["paev"] == paev:
                    kuupäev = päevad_töötamiseks[paev]
                    algus = time(kirje["kellaaeg"] // 60, kirje["kellaaeg"] % 60)
                    lõpp = time((kirje["kellaaeg"] + 30) // 60, (kirje["kellaaeg"] + 30) % 60)
                    print(f'{kuupäev.strftime("%d.%m.%Y")}: {algus.strftime("%H:%M")} - {lõpp.strftime("%H:%M")}')
    else:
        print('Kahjuks pole piisavalt aega selle ülesande jaoks.')


if __name__ == '__main__':
    main()
