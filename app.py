import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=dotenv_path, override=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import utenti_dao
import doughfinder_dao
import donazioni_dao
import funzioni
from models import User
import cloudinary
import cloudinary.uploader
from urllib.parse import urlparse
from flask import url_for



# Debug (puoi toglierlo dopo)
print("DEBUG CLOUDINARY_URL =", os.getenv("CLOUDINARY_URL"))
print("DEBUG CLOUDINARY_API_KEY =", os.getenv("CLOUDINARY_API_KEY"))
print("DEBUG CLOUDINARY_CLOUD_NAME =", os.getenv("CLOUDINARY_CLOUD_NAME"))


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret") #Secret_key impostata su railway

login_manager = LoginManager()
login_manager.init_app(app)

cloudinary_url = os.getenv("CLOUDINARY_URL")

if cloudinary_url:
    cloudinary.config(
        cloudinary_url=cloudinary_url,
        secure=True
    )
else:
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )


@app.route('/')
def index():
    utenti_db = utenti_dao.get_utenti()
    rf_db = doughfinder_dao.get_raccolta()
    donazioni = donazioni_dao.get_donazioni()
    all_rf = doughfinder_dao.get_raccolta_all()

    # datetime veri
    now_dt = datetime.now()
    current = now_dt.strftime("%Y-%m-%d %H:%M")

    # max selezionabile per la creazione: entro 14 giorni DA ADESSO
    scadenza_massima = (now_dt + timedelta(days=14)).strftime("%Y-%m-%d %H:%M")

    progetti_totali = len(all_rf)
    donazioni_globali_totali = len(donazioni)
    totale_globale_donazioni = 0

    rb_archivio = doughfinder_dao.get_archivio()
    migliori_successi = funzioni.migliori(rb_archivio)

    len_rf_db = len(rf_db)
    len_donazioni = len(donazioni)

    if len_rf_db > 2:
        rf_db = doughfinder_dao.get_raccolta()
        onfire = funzioni.on_fire(rf_db, donazioni)
        onfire23 = funzioni.on_fire2(rf_db, donazioni)
    else:
        onfire = 0
        onfire23 = 0

    for donazione in donazioni:
        totale_globale_donazioni += donazione['donazione']

    for raccolta in rf_db:
        if funzioni.is_scaduto(raccolta['scadenza'], current):
            doughfinder_dao.change_stato(raccolta['id'])

    for raccolta in rf_db:
        if funzioni.is_scaduto(raccolta['scadenza'], current):
            totale_donazioni_rf = 0
            for donazione in donazioni:
                if donazione['id_rf'] == raccolta['id']:
                    totale_donazioni_rf += donazione['donazione']

            if totale_donazioni_rf >= raccolta['obiettivo']:
                utenti_dao.success(raccolta['id_utente'], totale_donazioni_rf)
                doughfinder_dao.success_rf(raccolta['id'])

    rf_db_aggiornato = doughfinder_dao.get_raccolta()

    return render_template(
        'index.html',
        rf=rf_db_aggiornato,
        utenti=utenti_db,
        scadenza_massima=scadenza_massima,
        delete=doughfinder_dao.delete_rf,
        tempo_scadenza=funzioni.tempo_scadenza,
        current=current,
        tot_donazioni=funzioni.totale_donazioni,
        percentuale=funzioni.percentuale_rf,
        donazioni=donazioni,
        progetti_totali=progetti_totali,
        totale_globale_donazioni=totale_globale_donazioni,
        donazioni_globali_totali=donazioni_globali_totali,
        migliori=migliori_successi,
        onfire=onfire,
        onfire23=onfire23,
        len=len_rf_db,
        len_donazioni=len_donazioni
    )

def upload_image_to_cloudinary(file_storage, folder="doughfinder"):
    result = cloudinary.uploader.upload(
        file_storage,
        folder=folder,
        resource_type="image"
    )
    return result["secure_url"]




@app.route('/lampo')
def lampo():
    rf_db = doughfinder_dao.get_raccolta()
    donazioni = donazioni_dao.get_donazioni()
    current = datetime.now().strftime("%Y-%m-%d %H:%M")

    for raccolta in rf_db:

        if funzioni.is_scaduto(raccolta['scadenza'], current):
            doughfinder_dao.change_stato(raccolta['id'])

    rf_db_aggiornato = doughfinder_dao.get_raccolta()

    return render_template('lampo.html', rf=rf_db_aggiornato, donazioni=donazioni,
                           tot_donazioni=funzioni.totale_donazioni,
                           percentuale=funzioni.percentuale_rf, tempo_scadenza=funzioni.tempo_scadenza, current=current)

@app.route('/normale')
def normale():
    rf_db = doughfinder_dao.get_raccolta()
    donazioni = donazioni_dao.get_donazioni()
    current = datetime.now().strftime("%Y-%m-%d %H:%M")

    for raccolta in rf_db:

        if funzioni.is_scaduto(raccolta['scadenza'], current):
            doughfinder_dao.change_stato(raccolta['id'])

    rf_db_aggiornato = doughfinder_dao.get_raccolta()

    return render_template('normale.html',rf = rf_db_aggiornato, donazioni=donazioni,tot_donazioni=funzioni.totale_donazioni,
                           percentuale=funzioni.percentuale_rf,tempo_scadenza=funzioni.tempo_scadenza, current=current)

@app.route('/halloffame')
def halloffame():
    rf_db_aperti = doughfinder_dao.get_raccolta()
    current = datetime.now().strftime("%Y-%m-%d %H:%M")
    for raccolta in rf_db_aperti:

        if funzioni.is_scaduto(raccolta['scadenza'], current):
            doughfinder_dao.change_stato(raccolta['id'])

    rf_db = doughfinder_dao.get_archivio()
    donazioni = donazioni_dao.get_donazioni()

    return render_template('halloffame.html',rf=rf_db, donazioni=donazioni,tot_donazioni=funzioni.totale_donazioni,
                           percentuale =funzioni.percentuale_rf)

@app.route('/iscriviti')
def iscriviti():
    e = funzioni.età_minima()
    return render_template('signup.html', età_minima=e)

@app.route('/raccolta/modifica/<int:id_rf>', methods=['GET', 'POST'])
@login_required
def edit_rf(id_rf):
    rf_db = doughfinder_dao.get_raccolta_singolo(id_rf)
    current = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_datetime = datetime.strptime(current, "%Y-%m-%d %H:%M")
    rf = dict(rf_db)
    rf_data = datetime.strptime(rf_db['data'], "%Y-%m-%d %H:%M")
    scadenza_massima = (rf_data + timedelta(days=14)).strftime("%Y-%m-%d %H:%M")
    data_creazione = datetime.strptime(rf['data'], "%Y-%m-%d %H:%M")
    scadenza_lampo = data_creazione + timedelta(minutes=5)
    n_donazioni = donazioni_dao.count_donazioni_per_rf(id_rf)

    if rf['id_utente'] == current_user.id:
        n_donazioni = donazioni_dao.count_donazioni_per_rf(id_rf)

        return render_template(
            'edit_rf.html',
            rf=rf_db,
            current=current,
            current_dt=current_datetime,
            scadenza_massima=scadenza_massima,
            scadenza_lampo=scadenza_lampo,
            n_donazioni=n_donazioni
        )
    else:
        return redirect(url_for('index'))

@app.route('/archivio')
def archivio():
    rf_db = doughfinder_dao.get_archivio()
    donazioni = donazioni_dao.get_donazioni()
    current = datetime.now().strftime("%Y-%m-%d %H:%M")

    return render_template('archivio.html',rf=rf_db, donazioni=donazioni,tot_donazioni=funzioni.totale_donazioni,
                           percentuale =funzioni.percentuale_rf)

@app.route('/raccolta/<int:id>', methods=['GET', 'POST'])
def rf_singolo(id):
    rf = doughfinder_dao.get_raccolta_singolo(id)
    utenti = utenti_dao.get_utenti()
    donazioni = donazioni_dao.get_donazioni()
    current = datetime.now().strftime("%Y-%m-%d %H:%M")
    totale_donazioni = funzioni.totale_donazioni(donazioni,id)
    numero_donazioni= funzioni.num_donazioni(donazioni,id)

    percentuale_rf = funzioni.percentuale_rf(totale_donazioni,rf['obiettivo'])

    valore, tipo_tempo = funzioni.valore_scadenza(rf["scadenza"], current)

    if rf:
        return render_template('paginarf.html', rf=rf, current=current, utenti=utenti, donazioni=donazioni, totale=totale_donazioni, numero_donazioni=numero_donazioni, valore=valore, tipo_tempo=tipo_tempo, percentuale_rf=percentuale_rf)
    else:
        return render_template('error.html'), 404


@login_manager.user_loader #funzione che viene richiesta dal login manager
def load_user(user_id):
    db_user = utenti_dao.get_user_by_id(user_id)
    user = User(id=db_user['id'] ,
                email=db_user['email'],
                username=db_user['username'],
                password=db_user['password'],
                nome=db_user['nome'],
                cognome=db_user['cognome'],
                portafoglio=db_user['portafoglio'],
                data_nascita=db_user['data_nascita'] )

    return user

@app.route('/login', methods=['POST'])
def login():
    utente_form = request.form.to_dict()
    utente_db = utenti_dao.get_user_by_email(utente_form['email'])
    if not utente_db or not check_password_hash(utente_db['password'], utente_form['password']):
        flash('Credenziali errate', 'danger')
        return redirect(url_for('index'))
    else :
        new = User( id = utente_db['id'],
                    email = utente_db['email'],
                    username = utente_db['username'],
                    password = utente_db['password'],
                    nome=utente_db['nome'],
                    cognome=utente_db['cognome'],
                    portafoglio=utente_db['portafoglio'],
                    data_nascita=utente_db['data_nascita'] )
        login_user(new, True) # ci gestisce i cookie e tutte le sbatte del login
        flash('Login effettuato!', 'success' )
        return redirect(url_for('index'))


@app.route('/signup', methods=['POST'])
def signup():
    new_user_from_form = request.form.to_dict()

    if new_user_from_form['nome'] == '':
        app.logger.error('Il nome non può essere vuoto')
        return redirect(url_for('iscriviti'))
    if new_user_from_form['cognome'] == '':
        app.logger.error('Il cognome non può essere vuoto')
        return redirect(url_for('iscriviti'))
    if new_user_from_form['username'] == '':
        app.logger.error('Il username non può essere vuoto')
        return redirect(url_for('iscriviti'))
    if new_user_from_form['email'] == '':
        app.logger.error('la mail non può essere vuota')
        return redirect(url_for('iscriviti'))
    if new_user_from_form['password'] == '':
        app.logger.error('la password non può essere vuota')
        return redirect(url_for('iscriviti'))
    if new_user_from_form['data_nascita'] >= funzioni.età_minima():
        flash("Non è possibile iscriversi se si è minorenni", 'danger')
        app.logger.error('I minori di 18 anni non possono registrarsi sul sito')
        return redirect(url_for('iscriviti'))
    if new_user_from_form['data_nascita'] == '':
        app.logger.error('La data non può essere vuota')
        return redirect(url_for('iscriviti'))

    esiste_mail = utenti_dao.esiste_email(new_user_from_form['email'])

    if esiste_mail:
        flash('Mail esistente!', 'danger')
        return redirect(url_for('iscriviti'))

    else:
        new_user_from_form['password'] = generate_password_hash(
            new_user_from_form['password'])  # criptiamo la password hash

        success = utenti_dao.create_user(new_user_from_form)
        if success:
            utente_db = utenti_dao.get_user_by_email(new_user_from_form['email'])
            new = User(id=utente_db['id'],
                       email=utente_db['email'],
                       username=utente_db['username'],
                       password=utente_db['password'],
                       nome=utente_db['nome'],
                       cognome=utente_db['cognome'],
                       portafoglio=utente_db['portafoglio'],
                       data_nascita=utente_db['data_nascita'])
            login_user(new, True)  # ci gestisce i cookie e tutte le sbatte del login
            flash('Registrazione effettuata!', 'success')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('iscriviti'))




@app.route('/raccolta/new', methods=['POST'])
@login_required
def new_rf():
    new_rf = request.form.to_dict()
    new_foto = request.files['foto']
    current = datetime.now().strftime("%Y-%m-%d %H:%M")
    tipo = request.form.get('tipo', '0')
    imgp = 'logo1.png'

    scadenza_lampo= datetime.now() + timedelta(minutes=5)
    scadenza_str = scadenza_lampo.strftime("%Y-%m-%d %H:%M")

    scadenza_form = request.form.get('scadenza', scadenza_str)
    scadenza = scadenza_form.replace('T', ' ')

    current_ = datetime.strptime(current, "%Y-%m-%d %H:%M")
    scadenza_dt = datetime.strptime(scadenza, "%Y-%m-%d %H:%M")
    scadenza_massima = current_ + timedelta(days=14)



    if new_rf['titolo']=='':
        app.logger.error('Il titolo non può essere vuoto')
        return redirect(url_for('index'))
    if new_rf['descrizione']=='':
        app.logger.error('la descrizione non può essere vuota')
        return redirect(url_for('index'))

    if new_foto and new_foto.filename:
        imgp = upload_image_to_cloudinary(new_foto, folder="doughfinder/raccolte")
    else:
        imgp = 'default_img_rf.png'

    if new_rf['obiettivo']=='':
        app.logger.error("l'obiettivo non può essere vuoto")
        return redirect(url_for('index'))

    if new_rf['min_donazione']=='':
        app.logger.error("La donazione minima non può essere vuota")
        return redirect(url_for('index'))

    if new_rf['max_donazione']=='':
        app.logger.error("la donazione massima non può essere vuota")
        return redirect(url_for('index'))

    obiettivo = int(new_rf['obiettivo'])
    min = int(new_rf['min_donazione'])
    max = int(new_rf['max_donazione'])

    if obiettivo <= 0 or min <= 0 or max <= 0:
        flash("L'obiettivo e le donazioni minime o massime devono essere superiori a 0, riprovare", 'danger')
        app.logger.error("L'obiettivo e le donazioni minime o massime devono essere superiori a 0, riprovare")
        return redirect(url_for('index'))
    elif min >= max:
        flash("La donazione minima deve essere inferiore alla donazione massima, riprovare", 'danger')
        app.logger.error("La donazione minima deve essere inferiore alla donazione massima, riprovare")
        return redirect(url_for('index'))
    elif min >= obiettivo:
        flash("La donazione minima non può essere maggiore dell'obiettivo", 'danger')
        app.logger.error("La donazione minima non può essere maggiore dell'obiettivo, riprovare")
        return redirect(url_for('index'))

    # se raccolta NORMALE (tipo=0) controllo scadenza scelta dall'utente
    if str(tipo) == "0":
        if scadenza_dt < current_:
            flash("La data di scadenza non può essere antecedente alla creazione.", "danger")
            return redirect(url_for('index'))

        scadenza_massima = current_ + timedelta(days=15)  # <-- qui metti 14 o 15 come vuoi
        if scadenza_dt > scadenza_massima:
            flash("Puoi scegliere una scadenza entro massimo 15 giorni.", "danger")
            return redirect(url_for('index'))

    # se raccolta LAMPO (tipo=1) forzo scadenza a +5 min
    else:
        scadenza = scadenza_str

    user = current_user.id

    post = doughfinder_dao.add_rf(new_rf, current, user,tipo,imgp, scadenza)

    return redirect(url_for('index'))


@app.route('/delete/<int:id_rf>', methods=['POST'])
@login_required
def delete_rf(id_rf):
    post = doughfinder_dao.get_raccolta_singolo(id_rf)

    if not post:
        flash("Raccolta non trovata", "danger")
        return redirect(url_for('index'))

    if current_user.id != post['id_utente']:
        flash('Non si hanno le credenziali', 'danger')
        return redirect(url_for('index'))

    # BLOCCO: se ci sono donazioni non puoi cancellare
    n = donazioni_dao.count_donazioni_per_rf(id_rf)
    if n > 0:
        flash("Impossibile cancellare: la raccolta ha già ricevuto donazioni.", "warning")
        return redirect(url_for('index'))

    success = doughfinder_dao.delete_rf(id_rf)

    if success:
        flash(f'Raccolta con ID {id_rf} cancellata con successo.', 'success')
    else:
        flash('Errore: cancellazione non riuscita.', 'danger')

    return redirect(url_for('index'))




@app.route('/<username>')
@login_required
def myprofile(username):
    utenti_db = utenti_dao.get_utenti()
    rf_db = doughfinder_dao.get_raccolta_all()  # oppure get_raccolta() se già le prende tutte
    donazioni = donazioni_dao.get_donazioni()
    current = datetime.now().strftime("%Y-%m-%d %H:%M")

    # solo quelle dell’utente
    mie = [r for r in rf_db if r['id_utente'] == current_user.id]

    # separo attive / chiuse
    rf_attive = [r for r in mie if int(r.get('stato', 0)) == 0]
    rf_chiuse = [r for r in mie if int(r.get('stato', 0)) == 1]

    return render_template(
        "myprofile.html",
        rf=rf_attive,
        rf_chiuse=rf_chiuse,
        donazioni=donazioni,
        current=current,
        tempo_scadenza=funzioni.tempo_scadenza,
        tot_donazioni=funzioni.totale_donazioni,
        percentuale=funzioni.percentuale_rf
    )


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/logout')
@login_required #per poter invocare questa funzione bisogna che ci sia il login
def logout():
    logout_user()
    flash('Logout effettuato!', 'success')
    return redirect(url_for('index'))

@app.route('/new_password', methods=['POST'])
@login_required #per poter invocare questa funzione bisogna che ci sia il login
def new_password():
    utente_form = request.form.to_dict()
    utente_db = utenti_dao.get_user_by_email(current_user.email)

    if check_password_hash(utente_db['password'], utente_form['vecchia_password']):
        new_password = generate_password_hash(utente_form['nuova_password'])
        utenti_dao.change_password(current_user.email, new_password)
        flash('Password cambiata con successo', 'success')
        return redirect(url_for('settings'))

    else:
        flash('La vecchia password non è corretta', 'danger')
        return redirect(url_for('settings'))


@app.route('/edit_title/<int:id_rf>', methods=['POST'])
@login_required
def edit_title(id_rf):
    new_titolo = request.form.get('titolo')
    rf = doughfinder_dao.get_raccolta_singolo(id_rf)

    if rf:
        doughfinder_dao.change_title(id_rf, new_titolo )
        flash('Modifica avvenuta con successo', 'success')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    else:
        flash('Modifica non avvenuta', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))



@app.route('/edit_description/<int:id_rf>', methods=['POST'])
@login_required
def edit_description(id_rf):
    new_descrizione= request.form.get('descrizione')
    rf = doughfinder_dao.get_raccolta_singolo(id_rf)

    if rf:
        doughfinder_dao.change_description(id_rf, new_descrizione )
        flash('Modifica avvenuta con successo', 'success')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    else:
        flash('Modifica non avvenuta', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))


@app.route('/edit_scadenza/<int:id_rf>', methods=['POST'])
@login_required
def edit_scadenza(id_rf):
    rf = doughfinder_dao.get_raccolta_singolo(id_rf)
    if not rf:
        flash('Raccolta non trovata', 'danger')
        return redirect(url_for('index'))

    # Solo proprietario
    if rf['id_utente'] != current_user.id:
        flash('Non autorizzato', 'danger')
        return redirect(url_for('index'))

    new_scadenza = request.form.get('scadenza')
    if not new_scadenza:
        flash('Scadenza non valida', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    scadenza_str = new_scadenza.replace('T', ' ')

    try:
        scadenza_dt = datetime.strptime(scadenza_str, "%Y-%m-%d %H:%M")
    except ValueError:
        flash('Formato data non valido', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    now_dt = datetime.now()

    # limite: non nel passato
    if scadenza_dt < now_dt:
        flash('La scadenza non può essere nel passato.', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    # limite: massimo 14 giorni dalla DATA DI CREAZIONE della raccolta
    try:
        data_creazione_dt = datetime.strptime(rf['data'], "%Y-%m-%d %H:%M")
    except ValueError:
        flash('Errore: data creazione non valida nel database.', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    scadenza_massima_dt = data_creazione_dt + timedelta(days=14)

    if scadenza_dt > scadenza_massima_dt:
        flash('Non puoi scegliere una scadenza oltre 14 giorni dalla creazione della raccolta.', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    doughfinder_dao.change_scadenza(id_rf, scadenza_str)
    flash('Modifica avvenuta con successo', 'success')
    return redirect(url_for('edit_rf', id_rf=id_rf))



@app.route('/edit_tipo/<int:id_rf>', methods=['POST'])
@login_required
def edit_tipo(id_rf):
    rf = doughfinder_dao.get_raccolta_singolo(id_rf)
    new_tipo = 0
    data_creazione = datetime.strptime(rf['data'], "%Y-%m-%d %H:%M")
    new_scadenza = ''



    if rf['tipo'] == 0:
        new_tipo = 1
        new_scadenza = data_creazione + timedelta(minutes=5)
        scadenza = new_scadenza.strftime("%Y-%m-%d %H:%M")
        doughfinder_dao.change_tipo(id_rf, new_tipo, scadenza)
        flash('Modifica avvenuta con successo', 'success')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    else:
        new_scadenza = request.form.get('scadenza')
        new_tipo = 0
        scadenza = new_scadenza.replace('T', ' ')
        doughfinder_dao.change_tipo(id_rf, new_tipo, scadenza)
        flash('Modifica avvenuta con successo', 'success')
        return redirect(url_for('edit_rf', id_rf=id_rf))

@app.route('/edit_goal/<int:id_rf>', methods=['POST'])
@login_required
def edit_goal(id_rf):
    new_goal_raw = request.form.get('obiettivo')
    rf = doughfinder_dao.get_raccolta_singolo(id_rf)

    if not rf:
        flash('Modifica non avvenuta', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    # solo il proprietario può modificare
    if rf['id_utente'] != current_user.id:
        flash('Non autorizzato', 'danger')
        return redirect(url_for('index'))

    # BLOCCO: se esiste almeno una donazione, non si può modificare l'obiettivo
    n = donazioni_dao.count_donazioni_per_rf(id_rf)
    if n > 0:
        flash("Obiettivo bloccato: la raccolta ha già ricevuto donazioni.", 'warning')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    # VALIDAZIONE: deve essere un intero >= 1
    try:
        new_goal = int(new_goal_raw)
    except (TypeError, ValueError):
        flash("Obiettivo non valido.", "danger")
        return redirect(url_for('edit_rf', id_rf=id_rf))

    if new_goal < 1:
        flash("Obiettivo deve essere almeno 1€.", "danger")
        return redirect(url_for('edit_rf', id_rf=id_rf))

    doughfinder_dao.change_goal(id_rf, new_goal)
    flash('Modifica avvenuta con successo', 'success')
    return redirect(url_for('edit_rf', id_rf=id_rf))



@app.route('/edit_minmax/<int:id_rf>', methods=['POST'])
@login_required
def edit_minmax(id_rf):
    rf = doughfinder_dao.get_raccolta_singolo(id_rf)
    if not rf:
        flash('Raccolta non trovata', 'danger')
        return redirect(url_for('index'))

    # solo proprietario
    if rf['id_utente'] != current_user.id:
        flash('Non autorizzato', 'danger')
        return redirect(url_for('index'))

    new_min = request.form.get('min_donazione')
    new_max = request.form.get('max_donazione')

    # controlli base form
    if not new_min or not new_max:
        flash('Valori non validi', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    try:
        new_min = int(new_min)
        new_max = int(new_max)
    except ValueError:
        flash('Inserisci solo numeri', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    # vincoli: >= 1 e min < max
    if new_min < 1 or new_max < 1:
        flash('Min e Max devono essere almeno 1', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    if new_min >= new_max:
        flash('La donazione minima deve essere inferiore alla donazione massima', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    # (opzionale ma consigliato) controlla anche che min < obiettivo
    try:
        obiettivo = int(rf['obiettivo'])
        if new_min >= obiettivo:
            flash("La donazione minima non può essere maggiore o uguale all'obiettivo", 'danger')
            return redirect(url_for('edit_rf', id_rf=id_rf))
    except Exception:
        pass

    ok = doughfinder_dao.change_minmax(id_rf, new_min, new_max)
    if ok:
        flash('Modifica avvenuta con successo', 'success')
    else:
        flash('Errore durante la modifica', 'danger')

    return redirect(url_for('edit_rf', id_rf=id_rf))



@app.route('/new_img/<int:id_rf>', methods=['POST'])
@login_required
def new_img(id_rf):
    new_foto_profilo = request.files.get('img')

    # niente file caricato
    if not new_foto_profilo or not new_foto_profilo.filename:
        flash('Non siamo riusciti a cambiare la foto del profilo', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    try:
        # carico su Cloudinary (usa la tua funzione già definita)
        imgp = upload_image_to_cloudinary(new_foto_profilo, folder="doughfinder/raccolte")

        # salvo nel DB (imgp ora è un URL https://...)
        doughfinder_dao.change_img(id_rf, imgp)

        flash('Foto profilo cambiata con successo', 'success')
        return redirect(url_for('edit_rf', id_rf=id_rf))

    except Exception as e:
        app.logger.exception("Errore upload Cloudinary in new_img: %s", e)
        flash('Errore durante il caricamento immagine', 'danger')
        return redirect(url_for('edit_rf', id_rf=id_rf))




@app.route('/donazione/new/<int:id_rf>', methods=['POST'])
@login_required
def new_donazione(id_rf):
    new_donazione = request.form.to_dict()
    anonimo = request.form.get('anonimo', 0)
    rf = doughfinder_dao.get_raccolta_singolo(id_rf)
    current = datetime.now().strftime("%Y-%m-%d %H:%M")

    if new_donazione['nome']=='':
        app.logger.error('Il nome non può essere vuoto')
        return redirect(url_for('index'))
    if new_donazione['cognome']=='':
        app.logger.error('Il cognome non può essere vuoto')
        return redirect(url_for('index'))
    if new_donazione['donazione']=='':
        app.logger.error('la donazione non può essere vuota')
        return redirect(url_for('index'))




    if funzioni.is_scaduto(rf['scadenza'], current):
        flash('Impossibile donare, la raccolta fondi è ormai chiusa', 'danger')
        return redirect(url_for('rf_singolo', id=id_rf))
    else:
        donazioni_dao.add_donazione(new_donazione, id_rf, anonimo)
        flash('Donazione avvenuta', 'success')
        return redirect(url_for('rf_singolo', id=id_rf))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


def is_url(s: str) -> bool:
    try:
        u = urlparse(s)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False

@app.template_filter("img_url")
def img_url_filter(img_value):
    """
    - URL Cloudinary → usato direttamente
    - None / vuoto → default_img_rf.png
    - filename locale → static/<filename>
    """
    if not img_value:
        return url_for("static", filename="default_img_rf.png")

    img_value = str(img_value).strip()

    if is_url(img_value):
        return img_value

    if img_value.startswith("static/"):
        img_value = img_value.replace("static/", "", 1)

    return url_for("static", filename=img_value)




if __name__ == '__main__':
    app.run()
