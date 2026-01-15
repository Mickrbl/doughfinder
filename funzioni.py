from datetime import datetime
def data_ago(data, adesso):

    orario1 = datetime.strptime(data, "%Y-%m-%d %H:%M")
    orario2 = datetime.strptime(adesso, "%Y-%m-%d %H:%M")
    differenza = orario2 - orario1


    minuti = differenza.total_seconds() / 60
    ore = minuti / 60
    giorni = differenza.days

    if minuti < 10:
        return 'poco fa'
    elif minuti < 60:
        return f'{int(minuti)} minuti fa'
    elif ore < 2:
        return '1 ora fa'
    elif ore < 24:
        return f'{int(ore)} ore fa'
    elif giorni == 1:
        return 'un giorno fa'
    elif giorni < 30:
        return f'{giorni} giorni fa'
    elif giorni < 60:
        return 'un mese fa'
    elif giorni < 365:
        mesi = giorni // 30
        return f'{mesi} mesi fa'
    elif giorni == 365:
        return 'un anno fa'
    else:
        anni = giorni // 365
        return f'{anni} anni fa'

    return differenza


def età_minima():
    current_year = int(datetime.now().strftime("%Y"))
    età_minima_calcolo = current_year - 18
    current = datetime.now().strftime("-%m-%d")
    età_minima = str(età_minima_calcolo) + current

    return età_minima


def is_scaduto(scadenza_str,current):
    current_ = datetime.strptime(current, "%Y-%m-%d %H:%M")
    scadenza = datetime.strptime(scadenza_str, "%Y-%m-%d %H:%M")
    if current_ > scadenza:
        return True
    else:
        return False


def tempo_scadenza(scadenza,current):
    current_ = datetime.strptime(current, "%Y-%m-%d %H:%M")
    scadenza_datetime = datetime.strptime(scadenza, "%Y-%m-%d %H:%M")
    differenza = scadenza_datetime - current_

    if differenza.total_seconds() < 0:
        return ""

    giorni = differenza.days
    ore = differenza.seconds // 3600
    minuti = (differenza.seconds % 3600) // 60

    if giorni > 0:
        return f"{giorni} giorni alla fine"
    elif ore > 0:
        return f"{ore} ore alla fine"
    elif minuti > 0:
        return f"{minuti} minuti alla fine"
    else:
        return f"Pochi sec alla fine"

    return giorni, ore, minuti

def totale_donazioni(donazioni,id_rf):
    totale = 0
    for donazione in donazioni:
        if donazione["id_rf"] == id_rf:
            totale = totale + donazione['donazione']

    return totale
def num_donazioni(donazioni,id_post):
    num = 0
    for donazione in donazioni:
        if donazione["id_rf"] == id_post:
            num = num + 1

    return num

def valore_scadenza(scadenza,current):
    current_ = datetime.strptime(current, "%Y-%m-%d %H:%M")
    scadenza_datetime = datetime.strptime(scadenza, "%Y-%m-%d %H:%M")
    differenza = scadenza_datetime - current_

    if differenza.total_seconds() < 0:
        return "", ""

    giorni = differenza.days
    ore = differenza.seconds // 3600
    minuti = (differenza.seconds % 3600) // 60

    if giorni > 0:
        return giorni, "giorni"
    elif ore > 0:
        return ore, "ore"
    elif minuti > 0:
        return minuti, "minuti"
    else:
        return "Pochi sec alla fine", ""



def percentuale_rf(valore, obiettivo):
        percentuale_valore = (valore / obiettivo) * 100
        return int(percentuale_valore)


def migliori(archivio):
    lista=[]
    for elemento in archivio:
        if elemento['successo']==1:
            lista.append(elemento)

    lista.sort(key=lambda x: x['obiettivo'], reverse=True)
    migliori3=lista[0:3]

    return migliori3


def on_fire(rf_db,donazioni):
    lista=[]
    donazioni_totali = {}

    on_fire = {
        "id": 0,
        "tipo": 0,
        "descrizione": 0,
        "titolo": 0,
        "tipo": 0
    }


    if len(donazioni) < 10:
        return on_fire
    else:
        for elemento in rf_db:
            if elemento['stato']==0:
                lista.append(elemento)


        for donazione in donazioni:
            id_rf = donazione['id_rf']
            donazione_valore = donazione['donazione']
            donazioni_totali[id_rf] = donazioni_totali.get(id_rf, 0) + donazione_valore

        rf_max_donazioni = None
        max_donazioni = 0
        for rf in rf_db:
            id_rf = rf['id']
            if id_rf in donazioni_totali:
                if donazioni_totali[id_rf] > max_donazioni:
                    max_donazioni = donazioni_totali[id_rf]
                    rf_max_donazioni = rf
        print(rf_max_donazioni['titolo'])

        return rf_max_donazioni


def on_fire2(rf_db, donazioni):
        somme_donazioni = {}

        if len(donazioni) < 3:
            return ''
        else:
            for donazione in donazioni:
                id_rf = donazione['id_rf']
                donazione_valore = donazione['donazione']
                somme_donazioni[id_rf] = somme_donazioni.get(id_rf, 0) + donazione_valore

            top_donazioni = sorted(set(somme_donazioni.values()), reverse=True)[:3]

            top_rf = []
            for id_rf, valore_donazioni in somme_donazioni.items():
                if valore_donazioni in top_donazioni[1:]:
                    for rf in rf_db:
                        if rf['id'] == id_rf:
                            top_rf.append(rf)

            return top_rf




