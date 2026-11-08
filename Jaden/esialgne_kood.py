def kellaaeg_minutiteks(kellaaeg):
    tunnid_ja_minutid = kellaaeg.split(":")
    tunnid = int(tunnid_ja_minutid[0])
    minutid = int(tunnid_ja_minutid[1])
    return tunnid * 60 + minutid


def minutid_kellaajaks(minutid_keskoost):
    tunnid = minutid_keskoost // 60
    minutid = minutid_keskoost % 60
    tunnid_tekstina = str(tunnid)
    minutid_tekstina = str(minutid)
    if tunnid < 10:
        tunnid_tekstina = "0" + tunnid_tekstina
    if minutid < 10:
        minutid_tekstina = "0" + minutid_tekstina
    return tunnid_tekstina + ":" + minutid_tekstina


def paeva_vabad_pooltunnid(oppimise_algus, oppimise_lopp, ei_sobi_ajad):
    algus_minutites = kellaaeg_minutiteks(oppimise_algus)
    lopp_minutites = kellaaeg_minutiteks(oppimise_lopp)
    vabad_pooltunnid = set(range(algus_minutites, lopp_minutites, 30))

    for aeg in ei_sobi_ajad:
        ajavahemik = aeg.split("-")
        sobimatu_algus = kellaaeg_minutiteks(ajavahemik[0])
        sobimatu_lopp = kellaaeg_minutiteks(ajavahemik[1])
        sobimatud_pooltunnid = set(range(sobimatu_algus, sobimatu_lopp, 30))
        vabad_pooltunnid = vabad_pooltunnid - sobimatud_pooltunnid

    return vabad_pooltunnid


def lisa_pausid(paeva_vabad_ajad):
    if len(paeva_vabad_ajad) > 0:
        oppimise_algus = min(paeva_vabad_ajad)
        paeva_lopp = max(paeva_vabad_ajad)
        for paus in range(oppimise_algus + 90, paeva_lopp + 30, 120):
            if paus in paeva_vabad_ajad:
                paeva_vabad_ajad.remove(paus)
    return paeva_vabad_ajad


def leia_vabad_ajad(paevade_seaded, kell_praegu):
    vabad_ajad = []

    for seaded in paevade_seaded:
        oppimise_algus = seaded["algus"]
        oppimise_lopp = seaded["lopp"]
        ei_sobi_ajad = seaded["ei_sobi"]
        vabad = paeva_vabad_pooltunnid(oppimise_algus, oppimise_lopp, ei_sobi_ajad)
        vabad_ajad.append(vabad)

    kell_praegu_minutites = kellaaeg_minutiteks(kell_praegu)
    tanased_moodunud_pooltunnid = set(range(0, kell_praegu_minutites, 30))
    vabad_ajad[0] = vabad_ajad[0] - tanased_moodunud_pooltunnid

    for paev in range(len(vabad_ajad)):
        paeva_vabad_ajad = vabad_ajad[paev]
        vabad_ajad[paev] = lisa_pausid(paeva_vabad_ajad)

    return vabad_ajad


def vaba_aeg_enne_tahtaega(vabad_ajad, paevi_tahtajani):
    vaba_aeg_minutites = 0
    for paev in range(paevi_tahtajani):
        vabu_pooltunde = len(vabad_ajad[paev])
        vaba_aeg_minutites = vaba_aeg_minutites + vabu_pooltunde * 30
    return vaba_aeg_minutites


def paiguta_ylesanne(vabad_ajad, ylesande_nimi, kulub_minuteid, paevi_tahtajani):
    ylesande_ajad = []
    paigutamata_minuteid = kulub_minuteid

    while paigutamata_minuteid > 0 and vaba_aeg_enne_tahtaega(vabad_ajad, paevi_tahtajani) > 0:
        for paev in range(paevi_tahtajani):
            vabad_kellaajad = sorted(vabad_ajad[paev])
            paigutamata_pooltunde = paigutamata_minuteid // 30
            vabu_pooltunde = len(vabad_kellaajad)
            mitu_pooltundi = min(3, paigutamata_pooltunde, vabu_pooltunde)
            valitud_kellaajad = vabad_kellaajad[:mitu_pooltundi]

            for kellaaeg in valitud_kellaajad:
                vabad_ajad[paev].remove(kellaaeg)
                ylesande_ajad.append({"nimi": ylesande_nimi, "paev": paev, "kellaaeg": kellaaeg})

            paigutamata_minuteid = paigutamata_minuteid - mitu_pooltundi * 30

    return ylesande_ajad
