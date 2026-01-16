--
-- PostgreSQL database dump
--

\restrict 5ySZdgKUHLQarUK8ICE2qMLlxLzMlFgGNLgyH5bzdiWcyNqHT61PNeTS4IdxpYw

-- Dumped from database version 14.20 (Homebrew)
-- Dumped by pg_dump version 14.20 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: donazioni; Type: TABLE; Schema: public; Owner: mickolroebaronialasquety
--

CREATE TABLE public.donazioni (
    id integer NOT NULL,
    nome text DEFAULT 'Anonimo'::text NOT NULL,
    cognome text DEFAULT 'Anonimo'::text NOT NULL,
    donazione integer NOT NULL,
    id_rf integer NOT NULL,
    anonimo integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.donazioni OWNER TO mickolroebaronialasquety;

--
-- Name: donazioni_id_seq; Type: SEQUENCE; Schema: public; Owner: mickolroebaronialasquety
--

CREATE SEQUENCE public.donazioni_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.donazioni_id_seq OWNER TO mickolroebaronialasquety;

--
-- Name: donazioni_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mickolroebaronialasquety
--

ALTER SEQUENCE public.donazioni_id_seq OWNED BY public.donazioni.id;


--
-- Name: raccolta_fondi; Type: TABLE; Schema: public; Owner: mickolroebaronialasquety
--

CREATE TABLE public.raccolta_fondi (
    id integer NOT NULL,
    id_utente integer NOT NULL,
    titolo text NOT NULL,
    descrizione text NOT NULL,
    img text,
    obiettivo integer NOT NULL,
    tipo integer NOT NULL,
    max_donazione integer NOT NULL,
    min_donazione integer NOT NULL,
    data text NOT NULL,
    "like" integer DEFAULT 0 NOT NULL,
    stato integer DEFAULT 0 NOT NULL,
    donazioni integer DEFAULT 0 NOT NULL,
    scadenza text,
    successo integer DEFAULT 0 NOT NULL,
    CONSTRAINT chk_max_donazione CHECK ((max_donazione >= 1)),
    CONSTRAINT chk_min_donazione CHECK ((min_donazione >= 1)),
    CONSTRAINT chk_obiettivo CHECK ((obiettivo >= 1))
);


ALTER TABLE public.raccolta_fondi OWNER TO mickolroebaronialasquety;

--
-- Name: raccolta_fondi_id_seq; Type: SEQUENCE; Schema: public; Owner: mickolroebaronialasquety
--

CREATE SEQUENCE public.raccolta_fondi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.raccolta_fondi_id_seq OWNER TO mickolroebaronialasquety;

--
-- Name: raccolta_fondi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mickolroebaronialasquety
--

ALTER SEQUENCE public.raccolta_fondi_id_seq OWNED BY public.raccolta_fondi.id;


--
-- Name: utenti; Type: TABLE; Schema: public; Owner: mickolroebaronialasquety
--

CREATE TABLE public.utenti (
    id integer NOT NULL,
    nome text NOT NULL,
    cognome text NOT NULL,
    username text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    data_nascita text NOT NULL,
    portafoglio integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.utenti OWNER TO mickolroebaronialasquety;

--
-- Name: utenti_id_seq; Type: SEQUENCE; Schema: public; Owner: mickolroebaronialasquety
--

CREATE SEQUENCE public.utenti_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.utenti_id_seq OWNER TO mickolroebaronialasquety;

--
-- Name: utenti_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mickolroebaronialasquety
--

ALTER SEQUENCE public.utenti_id_seq OWNED BY public.utenti.id;


--
-- Name: donazioni id; Type: DEFAULT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.donazioni ALTER COLUMN id SET DEFAULT nextval('public.donazioni_id_seq'::regclass);


--
-- Name: raccolta_fondi id; Type: DEFAULT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.raccolta_fondi ALTER COLUMN id SET DEFAULT nextval('public.raccolta_fondi_id_seq'::regclass);


--
-- Name: utenti id; Type: DEFAULT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.utenti ALTER COLUMN id SET DEFAULT nextval('public.utenti_id_seq'::regclass);


--
-- Data for Name: donazioni; Type: TABLE DATA; Schema: public; Owner: mickolroebaronialasquety
--

COPY public.donazioni (id, nome, cognome, donazione, id_rf, anonimo) FROM stdin;
1	Mickol Roe Baronia	Lasquety	5	1	1
2	Lava 	Stoviglie	2000	1	0
3	Lesto	Fante	500	1	0
4	Mickol Roe Baronia	Lasquety	568	2	0
5	Mickol Roe Baronia	Lasquety	500	6	1
6	Fiamma	Cartina	257	6	0
7	Germana	Astonsi	157	6	0
8	Jose	Phina	480	6	0
9	Ciccio	Gamer	200	8	0
10	Sentinels	company	400	8	0
11	Mickol Roe Baronia	Lasquety	500	11	0
12	Mickol Roe Baronia	Lasquety	487	11	1
13	Mickol Roe Baronia	Lasquety	500	3	0
14	Mickol Roe Baronia	Lasquety	19000	4	0
15	Mickol Roe Baronia	Lasquety	14222	4	0
16	Mickol Roe Baronia	Lasquety	10000	5	1
17	Arcone	Fegatelli	5	12	0
18	Mercoledì	Martedì	800	7	0
19	Mickol Roe Baronia	Lasquety	342	7	1
\.


--
-- Data for Name: raccolta_fondi; Type: TABLE DATA; Schema: public; Owner: mickolroebaronialasquety
--

COPY public.raccolta_fondi (id, id_utente, titolo, descrizione, img, obiettivo, tipo, max_donazione, min_donazione, data, "like", stato, donazioni, scadenza, successo) FROM stdin;
1	5	Spashless 	Lavandino Splashless: rivoluzionario design anti-spruzzi. Esperienza di lavaggio senza inconvenienti. Mantieni la pulizia senza stress e gocce fastidiose. Supportateci per il futuro del mondo	imgprofilo258685CCcompany.jpg	10000	0	2000	5	2024-02-21 23:04	0	1	0	2024-02-29 23:04	0
2	5	Salotto dei sogni express	Supportaci per la creazione del nostro salotto dei sogni!  Per ogni persona che donerà nei prossimi 5 minuti doneremo un sorriso!	imgprofilo409128CCcompany.jpg	2000	1	1000	1	2024-02-21 23:07	0	1	0	2024-02-21 23:12	0
3	5	Ricreiamo la stanza di Friends	Ricreiamo la stanza di Friends, per tutti coloro che voglio collaborare a questo sogno! Coraggio aiutateci!	imgprofilo004324CCcompany.jpg	600	0	500	1	2024-02-21 23:11	0	1	0	2024-03-02 23:11	0
4	1	Poor Things	Aiutaci a portare vita a un'avventura epica! Sostieni il regista nel suo sogno di creare un film coinvolgente. "Una giovane donna riportata in vita da uno scienziato si unisce a un avvocato losco in avventure globali, scoprendo la sua passione per la giustizia sociale	imgprofilo265812lmsky98.jpg	100000	0	20000	20	2024-02-21 23:13	0	1	0	2024-03-05 23:13	0
5	1	Dogtooth	"Dogtooth": Un film controverso e sconcertante che esplora l'isolamento e il controllo familiare estremo attraverso una trama oscura e surreale. Con i vostri soldi riusciremo ad accedere al mondo degli dei del cinema!	imgprofilo956315lmsky98.jpg	10000	0	10000	20	2024-02-21 23:16	0	1	0	2024-02-27 23:16	1
6	1	Nimic	\r\nInvesti in "Nimic": un cortometraggio che sfida i confini dell'arte cinematografica. Offre un'esperienza coinvolgente e innovativa che promette di lasciare un'impronta duratura nel mondo del cinema.	imgprofilo189560lmsky98.jpg	1000	1	500	5	2024-02-21 23:18	0	1	0	2024-02-21 23:23	1
7	2	Stormgate	Dai creatori di StarCraft II e Warcraft III, arriva un nuovo RTS. Gioca con reattività estrema, potente editor, co-op, campagna, 1v1 e altro ancora! Sostienici nella raccolta fondi per realizzare questo progetto straordinario!	imgprofilo190483dungeonmaster.jpg	50000	0	5000	5	2024-02-21 23:22	0	1	0	2024-02-28 23:22	0
8	2	Legionari - The game	\r\nInvesti in "Legionari": un coinvolgente gioco da tavolo ambientato nell'antica Roma. Strategia, storia e divertimento si fondono per creare un'esperienza ludica senza tempo.	imgprofilo418089dungeonmaster.jpg	400	1	400	1	2024-02-21 23:24	0	1	0	2024-02-21 23:29	1
9	3	Hitball alle olimpiadi	Contribuisci alla ricerca della pecora perduta! Ogni aiuto conta per trovare il nostro prezioso amico smarrito. Dona oggi per riportare a casa la pecora sana e salva!	imgprofilo444668sentinels.jpg	100	1	200	5	2024-02-21 23:29	0	1	0	2024-02-21 23:34	0
10	3	Pasta immersiva	Pasta Immersiva" è un progetto culinario che unisce tradizione e tecnologia. Utilizzando realtà aumentata e storytelling, trasforma la preparazione della pasta in un'esperienza coinvolgente e multisensoriale, esplorando la sua storia e cultura.	imgprofilo861038sentinels.jpg	5000	0	5000	1	2024-02-21 23:31	0	1	0	2024-02-28 23:31	0
11	3	Serie tv - Beau is afraid	Beau ha Paura" è una serie TV innovativa che affronta il tema del coraggio e della resilienza attraverso una storia avvincente e personaggi coinvolgenti. 	imgprofilo320221sentinels.jpg	500	1	500	1	2024-02-21 23:34	0	1	0	2024-02-21 23:39	1
12	3	Hitball alle olimpiadi	Aiutaci a portare hitball alle olimpiadi!	imgprofilo540224sentinels.jpg	200	0	5	1	2024-02-21 23:38	0	1	0	2024-02-23 01:41	0
\.


--
-- Data for Name: utenti; Type: TABLE DATA; Schema: public; Owner: mickolroebaronialasquety
--

COPY public.utenti (id, nome, cognome, username, email, password, data_nascita, portafoglio) FROM stdin;
1	Mickol Roe Baronia	Lasquety	Yorgos Lanthimos	lmsky98@gmail.com	scrypt:32768:8:1$TvdYmWCd3HD0GiiH$728647920e9175b7003dba0dfa72d627346c56a215590a8cc25b8c0ad73fd341af51a8ecad186669e5a493f06f1fe7c12c2dad38e7df2a3b0f2e36c5d488b04b	1998-02-14	10000
2	Carletto	Ferdinelli	dungeonmaster	dungeonmaster@gmail.com	scrypt:32768:8:1$z32hj4BQp5EalgpA$ae56d55134e17d8283e5829c091cf4449c992bbbaaf5db2982ca2bf41bc58c561bed7cbfddf39165dcfe7ed803ad753de4f4cc0bc40a36ab3140c5aac56f44aa	1967-02-16	600
3	Ferdinelli 	Asparago	sentinels_company	sentinels@gmail.com	scrypt:32768:8:1$gGNTFh1w4FLLl25D$10ccf11c9eff292e42281dae453dc23a125b444b12f2f02a89431138b6b3fbfd8236263a457e396a27311451c57b82e49e926cec6f6d858eac74bc5a7597f70d	1997-07-09	987
4	Miranda	Malintenzionata	Malinda	malinda@gmail.com	scrypt:32768:8:1$DJhzFJ7IZQPH52Jl$a8f571e1fec421014d39b1f84c231c7ba446d9100a6cc8c72d52658958f3a7679b257a666861ad1b9561cc77f9a7ee0e14ac6db411f9eac14408a64020917216	1976-06-21	0
5	Merletto	Ancestrillo	Carmela corporatio	CCcompany@gmail.com	scrypt:32768:8:1$z3gDb09g9vtiVppA$dec99dadc51faa4796827acb56c2826029156a2408b545f4ff27932923ad7a3c80674da6807731c579ac705edfe23f4b064b1c0904a7c0fdc324150550bc44f8	1978-06-09	0
6	Martino	Campanaro	Martins	martins@gmail.com	scrypt:32768:8:1$CTVJR4grc7V7hpSQ$70271e8eea9f3217bd1f94047f10a0c95f7f8680429170122f679bc6963c77966cc352a50047fd81702ebeb52a7295026959cf77552256843d0b95f29f88a29b	2004-02-17	0
7	Federica	La Cara	Fedez	federica.lacara98@gmail.com	scrypt:32768:8:1$2ahKcUGUKckFMj7i$369ba8e704915592392b371797d6a92096d0af60141366594155ec8502d6a221e3eea7492b44da08d7889eef5bd90968f706d5b779a2ce9cbea85573f395db3e	1998-07-09	0
8	Mick	Roe	Micks	mick@gmail.com	scrypt:32768:8:1$72QngWgNdOMxIsOF$8c4dbd1f3ac86111b913d8544ea24a64637632cbf3f2a5d1d1876a46ae019beca35bcd69879312e9296b0c46d484167e73906fa0225b669ad074095f6968f4fe	2000-02-09	0
9	Goga	Goga	Goga	Goga@gmail.com	scrypt:32768:8:1$Jm3YuqIfdguV8YVP$3083af7abcecdac33b2f354fa3e2ce0a13282c918f9cc55b70a4735039e76d7e2feb5f855ec88ef379e8e40825385a06c9ab854f6979f20c39d5435018f07452	2000-02-14	0
\.


--
-- Name: donazioni_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mickolroebaronialasquety
--

SELECT pg_catalog.setval('public.donazioni_id_seq', 21, true);


--
-- Name: raccolta_fondi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mickolroebaronialasquety
--

SELECT pg_catalog.setval('public.raccolta_fondi_id_seq', 29, true);


--
-- Name: utenti_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mickolroebaronialasquety
--

SELECT pg_catalog.setval('public.utenti_id_seq', 9, true);


--
-- Name: donazioni donazioni_pkey; Type: CONSTRAINT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.donazioni
    ADD CONSTRAINT donazioni_pkey PRIMARY KEY (id);


--
-- Name: raccolta_fondi raccolta_fondi_pkey; Type: CONSTRAINT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.raccolta_fondi
    ADD CONSTRAINT raccolta_fondi_pkey PRIMARY KEY (id);


--
-- Name: utenti utenti_email_key; Type: CONSTRAINT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.utenti
    ADD CONSTRAINT utenti_email_key UNIQUE (email);


--
-- Name: utenti utenti_pkey; Type: CONSTRAINT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.utenti
    ADD CONSTRAINT utenti_pkey PRIMARY KEY (id);


--
-- Name: utenti utenti_username_key; Type: CONSTRAINT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.utenti
    ADD CONSTRAINT utenti_username_key UNIQUE (username);


--
-- Name: donazioni donazioni_id_rf_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.donazioni
    ADD CONSTRAINT donazioni_id_rf_fkey FOREIGN KEY (id_rf) REFERENCES public.raccolta_fondi(id);


--
-- Name: raccolta_fondi raccolta_fondi_id_utente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mickolroebaronialasquety
--

ALTER TABLE ONLY public.raccolta_fondi
    ADD CONSTRAINT raccolta_fondi_id_utente_fkey FOREIGN KEY (id_utente) REFERENCES public.utenti(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 5ySZdgKUHLQarUK8ICE2qMLlxLzMlFgGNLgyH5bzdiWcyNqHT61PNeTS4IdxpYw

