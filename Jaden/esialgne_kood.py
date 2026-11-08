def kellaaeg_minutiteks(kellaaeg):
    """Teeb kellaajast "19:30" minutid alates keskööst (1170)."""
    tunnid = int(kellaaeg[:2])
    minutid = int(kellaaeg[3:])
    return tunnid * 60 + minutid


def leia_yhe_paeva_ajad(seaded):
    """Tagastab ühe päeva vabad ajad: kõik õppimise ajad miinus ajad, mis ei sobi."""
    algus = kellaaeg_minutiteks(seaded["algus"])
    lopp = kellaaeg_minutiteks(seaded["lopp"])
    yhe_paeva_ajad = set(range(algus, lopp, 30))

    for vahemik in seaded["ei_sobi"]:
        algus = kellaaeg_minutiteks(vahemik[:5])
        lopp = kellaaeg_minutiteks(vahemik[6:])
        yhe_paeva_ajad = yhe_paeva_ajad - set(range(algus, lopp, 30))

    return yhe_paeva_ajad


def lisa_pausid(yhe_paeva_ajad):
    """Esimene paus tuleb 90 min pärast õppimise algust, siis iga 2 tunni järel uuesti."""
    if len(yhe_paeva_ajad) > 0:
        algus = min(yhe_paeva_ajad)
        lopp = max(yhe_paeva_ajad)
        for paus in range(algus + 90, lopp + 30, 120):
            if paus in yhe_paeva_ajad:
                yhe_paeva_ajad.remove(paus)
    return yhe_paeva_ajad


def leia_vabad_ajad(paevade_seaded, kell_praegu):
    """Tagastab iga päeva vabad ajad koos pausidega. [0] on täna, [1] on homme jne."""
    vabad_ajad = []
    for seaded in paevade_seaded:
        yhe_paeva_ajad = leia_yhe_paeva_ajad(seaded)
        vabad_ajad.append(yhe_paeva_ajad)

    tanased_moodunud_ajad = set(range(0, kellaaeg_minutiteks(kell_praegu), 30))
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
