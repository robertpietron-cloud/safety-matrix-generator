# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/locales/da.py
# Author  : Robert Pietroń
# Revision: 1.1.0 (2026-10-21)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: danske tekster (samme nøgler
#                        som det engelske katalog).
#   1.1.0 (2026-10-21) - Texts of the new audit rules (SafetyTagMap target written,
#                        copied / computed channels, scan-order lag, EDM, ROUT
#                        extra logic, always-on / inverse outputs, AFI without
#                        outputs, timers outside device paths), constant bypass,
#                        ROUT/CROUT restart with a start / seal-in on its rung.
# =============================================================================
"""Danske tekster."""

TEXT = {
    # ------------------------------------------------------------------ dokument
    'doc.title': 'SAFETY MATRIX – {name} (SafetyTask)',
    'doc.block': 'Forfatter: {author}   •   Revision: {rev}   •   Dato: {date}',
    'doc.block_lang': '   •   Sprog: arket "Start"',
    'doc.source': 'Kilde: {src} • {proc} {ver} • SafetyTask {period} ms',
    'doc.subject': 'Årsags-virkningsmatrix – GuardLogix SafetyTask',
    # ------------------------------------------------------------------ arknavne
    'sheet.start': 'Start',
    'sheet.legend': 'Signaturforklaring',
    'sheet.sf': 'Sikkerhedsfunktioner',
    'sheet.test': 'Testprotokol',
    'sheet.dev': 'Komponenter',
    'sheet.out': 'Udgange',
    'sheet.path': 'C&E-stier',
    'sheet.rep': 'Rapport',
    'sheet.dict': 'Ordbog',
    # ------------------------------------------------------------------ arkoversigt
    'sl.start': 'Forside: sprogvalg, oversigt over ark, sammenfatning.',
    'sl.gi': 'Matrix efter skabelonen: rækker = udgange, kolonner = komponenter; Enable Group; metadatarækker for komponenterne; signaturforklaring.',
    'sl.motor': 'Matrix efter skabelonen: rækker = komponenter, kolonner = udgange; kommentarer med rung-stien; metadata for udgange (EDM, reset); signaturforklaring.',
    'sl.valve': 'Efter skabelonen: sikkerhedsventiler (udgange markeret som ventiler i konfigurationen).',
    'sl.legend': 'Komplet ordbog over betegnelser, metode, revisionshistorik, kilder.',
    'sl.sf': 'Sikkerhedsfunktion pr. komponent: udgange, indgangsstruktur, reaktionstid (værste tilfælde) ud fra CIP Safety-forbindelsernes parametre, felter for PLr / Kat. / PL.',
    'sl.test': 'Valideringsprotokol (ISO 13849-2) genereret fra matrixen: funktionstest, kanaluoverensstemmelse, OR-kombinationer, std-omgåelser, EDM, kommunikationstab; kolonner til resultat og underskrift.',
    'sl.dev': 'Kanaler, instruktion, rung, reset-type og -kilde, muting, status.',
    'sl.out': 'Adresse/IP, Enable Group og dens logik, EDM, reset, genstart, output-CRTL; udgange uden for matrixen.',
    'sl.path': 'Hvert krydsfelt med den fulde sti tag [rutine R rung] og omgåelsesbit / OR-partner.',
    'sl.rep': 'Kritiske alarmer, døde elementer, liste [SKAL VERIFICERES] – hver med rutine og rung.',
    'sl.dict': 'Tekster på alle sprog brugt af sprogvalget – oversættelser kan rettes her.',
    # ------------------------------------------------------------------ zoner / grupper / beskrivelser
    'zone.routine': 'ZONE {n} : rutine {routine}',
    'zone.other': 'ZONE {n} : øvrige komponenter',
    'group.routine': 'RUTINE {routine}',
    'group.info': 'SIGNALER TIL STANDARDSTYRINGEN (INFO)',
    'group.other': 'ØVRIGE UDGANGE',
    'effdesc.ROUT': 'Sikkerhedsudgang {instr} {tag} – I/O: {io}',
    'effdesc.OUT': 'Sikkerhedsudgang {tag} – I/O: {io}',
    'effdesc.DRIVE': '{name} – {catalog} {kind} {desc}',
    'effdesc.INFO': 'Signal til standardstyringen {tag} – {io}',
    # ------------------------------------------------------------------ ord
    'w.all': 'alle ({n})',
    'w.zone_n': 'ZONE {n}',
    'w.nocomment': 'ingen kommentar [SKAL VERIFICERES]',
    'w.bypass': 'Omgåelse (std-bit): {bits}',
    'w.conditions': 'Medmindre (intern betingelse / muting): {bits}',
    'w.partners': 'Udløser kun sammen med: {devs}',
    'w.delay': 'Frafaldsforsinkelse i stien: {ms} ms (stopkategori 1)',
    'w.constbypass': 'Kortsluttet af en konstant kontakt (startværdi 1, skrives aldrig): {bits}',
    'w.lag': 'Scanningsrækkefølge: +{n} SafetyTask-periode(r) = {ms} ms (værdi fra forrige scanning)',
    'src.const': '{op} = konstant {v}',
    'src.never': '{op} – skrives aldrig (ubrugt)',
    'src.literal': 'konstant {v}',
    # ------------------------------------------------------------------ koder
    'code.blank': '(tom)',
    'code.X.short': 'Slår udgangen fra direkte',
    'code.X.full': 'Udløsning af komponenten (O1 = 0) slår sikkerhedsudgangen direkte fra (STO på frekvensomformeren eller kontaktorfrafald). '
                   'Sti gennem rungs: cellekommentar (MOTOR) og arket "C&E-stier".',
    'code.X1.short': 'Slår fra, men komponenten er reelt enkeltkanals  [ALARM]',
    'code.X1.full': 'Som X, men begge instruktionens kanaler peger på samme indgang (eller direkte indgang uden sikkerhedsinstruktion) – '
                    'ingen redundans og ingen detektering af kanaluoverensstemmelse. [KRITISK ALARM]',
    'code.XB.short': 'Slår fra, men kan omgås / mutes fra standardstyringen  [ALARM]',
    'code.XB.full': 'Slår udgangen fra, MEN en bit fra standardstyringen (SafetyTagMap) kan kortslutte eller mute denne funktion. '
                    'Navn på omgåelsesbitten: cellekommentar / "C&E-stier". [KRITISK ALARM]',
    'code.XC.short': 'Slår kun fra sammen med en anden komponent (OR-gren)',
    'code.XC.full': 'Udgangen falder først, når partnerkomponenten OGSÅ er udløst (parallelle OR-grene). En enkelt udløsning stopper ikke. '
                    'Partner: cellekommentar / "C&E-stier". [SKAL VERIFICERES]',
    'code.XM.short': 'Slår fra, medmindre en intern betingelse er opfyldt (muting / tilstand / data)',
    'code.XM.full': 'Slår udgangen fra, men en intern betingelse i SafetyTask (muting-instruktion, sammenligning, tilstandsvælger, data eller låst bit) '
                    'kan holde den inde. Betingelse: cellekommentar / "C&E-stier". [SKAL VERIFICERES]',
    'code.N.short': 'I logikken, men ikke-funktionel – udløser aldrig  [ALARM]',
    'code.N.full': 'Komponenten er i den logiske sti, men kan aldrig slå udgangen fra: instruktionen har konstante '
                   'kanalindgange, eller komponenten er kortsluttet af en konstant kontakt (tag med startværdi 1, '
                   'som logikken aldrig skriver). [KRITISK ALARM]',
    'code.S.short': 'Info: signal til standardstyringen (ikke en sikkerhedsudgang)',
    'code.S.full': 'Informationskolonne: status, der videregives til STANDARDstyringen (f.eks. forrigling til en anden maskine). Ikke en sikkerhedsudgang.',
    'code.SB.short': 'Som S, med mulig omgåelse fra standardstyringen',
    'code.SB.full': 'Som S, med mulig omgåelse via en standardbit (se XB).',
    'code.SC.short': 'Som S, kun sammen med en anden komponent (OR)',
    'code.SC.full': 'Som S, kun sammen med partnerkomponenten (se XC).',
    'code.SM.short': 'Som S, medmindre en intern betingelse er opfyldt',
    'code.SM.full': 'Som S, med en intern betingelse, der kan holde signalet inde (se XM).',
    'code.none.short': 'Ingen forbindelse i SafetyTask-koden',
    'code.none.full': 'Ingen logisk sti i SafetyTask-koden mellem komponenten og udgangen.',
    # ------------------------------------------------------------------ komponenttyper
    'type.EMERGENCY STOP': 'Nødstop', 'type.SAFETY DOOR': 'Sikkerhedsdør', 'type.SAFETY GATE': 'Sikkerhedslåge',
    'type.SAFETY SWITCH': 'Sikkerhedsafbryder', 'type.LIGHT CURTAIN': 'Lysgardin', 'type.SAFETY SCANNER': 'Sikkerhedsscanner',
    'type.SAFETY MAT': 'Sikkerhedsmåtte', 'type.TWO-HAND CONTROL': 'Tohåndsbetjening', 'type.ENABLING DEVICE': 'Aktiveringsanordning',
    'type.ANALOG SAFETY INPUT': 'Analog sikkerhedsindgang', 'type.SAFETY INPUT': 'Sikkerhedsindgang',
    'type.DIRECT SAFETY INPUT': 'Direkte sikkerhedsindgang', 'type.EXTERNAL SAFETY SIGNAL': 'Eksternt sikkerhedssignal',
    'typedesc.EMERGENCY STOP': 'nødstopanordning (nødstop, svampeknap)',
    'typedesc.SAFETY DOOR': 'bevægelig afskærmning / dør (dørkontakt, dørlås)',
    'typedesc.SAFETY GATE': 'låge / adgangslåge',
    'typedesc.SAFETY SWITCH': 'sikkerhedsafbryder (positions- / forriglingsafbryder)',
    'typedesc.LIGHT CURTAIN': 'lysgardin / lysgitter',
    'typedesc.SAFETY SCANNER': 'sikkerhedslaserscanner',
    'typedesc.SAFETY MAT': 'trykfølsom sikkerhedsmåtte',
    'typedesc.TWO-HAND CONTROL': 'tohåndsbetjeningsanordning',
    'typedesc.ENABLING DEVICE': 'aktiveringsanordning / enable-håndterminal',
    'typedesc.ANALOG SAFETY INPUT': 'tokanals analog sikkerhedsindgang',
    'typedesc.SAFETY INPUT': 'tokanals sikkerhedsindgang (typen ikke genkendt i programmet – se beskrivelsen)',
    'typedesc.DIRECT SAFETY INPUT': 'sikkerhedsindgang brugt direkte i logikken uden sikkerhedsindgangsinstruktion',
    'typedesc.EXTERNAL SAFETY SIGNAL': 'sikkerhedssignal fra en anden controller (produced/consumed safety tag)',
    'fn.EMERGENCY STOP': 'Nødstop', 'fn.SAFETY DOOR': 'Forrigling af afskærmning – åbning af døren stopper',
    'fn.SAFETY GATE': 'Forrigling af låge – åbning stopper', 'fn.SAFETY SWITCH': 'Sikkerhedsafbryder',
    'fn.LIGHT CURTAIN': 'Stop ved afbrydelse af lysgardinet', 'fn.SAFETY SCANNER': 'Stop ved overtrædelse af scannerens beskyttelsesfelt',
    'fn.SAFETY MAT': 'Stop ved betrædelse af måtten', 'fn.TWO-HAND CONTROL': 'Tohåndsbetjening',
    'fn.ENABLING DEVICE': 'Aktiveringsfunktion', 'fn.ANALOG SAFETY INPUT': 'Analog sikkerhedsgrænse',
    'fn.SAFETY INPUT': 'Sikkerhedsindgangsfunktion', 'fn.DIRECT SAFETY INPUT': 'Direkte sikkerhedsindgang',
    'fn.EXTERNAL SAFETY SIGNAL': 'Forrigling fra en anden sikkerhedscontroller',
    'act.EMERGENCY STOP': 'Tryk på nødstoppet', 'act.SAFETY DOOR': 'Åbn døren', 'act.SAFETY GATE': 'Åbn lågen',
    'act.SAFETY SWITCH': 'Aktivér sikkerhedsafbryderen', 'act.LIGHT CURTAIN': 'Afbryd lysgardinet med teststangen',
    'act.SAFETY SCANNER': 'Før testobjektet ind i scannerens beskyttelsesfelt', 'act.SAFETY MAT': 'Træd på sikkerhedsmåtten',
    'act.TWO-HAND CONTROL': 'Slip den ene af tohåndsknapperne', 'act.ENABLING DEVICE': 'Slip aktiveringsanordningen',
    'act.ANALOG SAFETY INPUT': 'Bring det analoge signal ud over sikkerhedsgrænsen', 'act.SAFETY INPUT': 'Afbryd sikkerhedsindgangens kreds',
    'act.DIRECT SAFETY INPUT': 'Afbryd indgangskredsen', 'act.EXTERNAL SAFETY SIGNAL': 'Udløs sikkerhedsfunktionen i den producerende controller',
    # ------------------------------------------------------------------ udgangstyper
    'kindshort.ROUT': 'ROUT', 'kindshort.CROUT': 'CROUT', 'kindshort.OUT': 'Sikkerhedsudgang', 'kindshort.STO': 'STO CIP Safety',
    'kindshort.SS1': 'SS1 CIP Safety', 'kindshort.SBC': 'SBC CIP Safety', 'kindshort.SLS': 'SLS CIP Safety', 'kindshort.INFO': 'Std-bit (info)',
    'kind.ROUT': 'Redundant Output – par af sikkerhedsudgange, der styrer sikkerhedskontaktorer / -ventiler med EDM-tilbagemelding (NEGATIVE: udgang ON → '
                 'tilbagemelding OFF; POSITIVE: tilbagemeldingen følger udgangen). Udgangene følger Enable – ROUT-reset nulstiller kun fejlen.',
    'kind.CROUT': 'Configurable Redundant Output – som ROUT, med reaktionstid for tilbagemelding og overvågning af Input/Output Status.',
    'kind.OUT': 'Sikkerhedsudgangspunkt skrevet af en spole (OTE) uden udgangsinstruktion med EDM.',
    'kind.STO': 'Frekvensomformer via CIP Safety: :SO.SafeTorqueOff = 1 moment tilladt, 0 = STO. Reset af frekvensomformeren :SO.Reset; status :SI.TorqueDisabled, :SI.SafetyFault.',
    'kind.SS1': 'Anmodning om Safe Stop 1 til frekvensomformeren via CIP Safety (kontrolleret stop, derefter STO).',
    'kind.SBC': 'Safe Brake Control via CIP Safety.',
    'kind.SLS': 'Anmodning om Safely-Limited Speed via CIP Safety.',
    'kind.INFO': 'Informationsbit skrevet af SafetyTask og læst af standardstyringen (f.eks. forrigling til en anden maskine). Ikke en sikkerhedsudgang.',
    # ------------------------------------------------------------------ instruktioner
    'ins.ESTOP': 'Emergency Stop (legacy) – 2 kanaler; .O1 = 1 OK, 0 = aktiveret / fejl; reset MANUAL eller AUTOMATIC.',
    'ins.RIN': 'Redundant Input (legacy) – 2 kanaler (døre, låger, afbrydere).',
    'ins.LC': 'Light Curtain (legacy) – Mute-indgang = 1 ignorerer lysgardinet (muting); indgangsfilter i ms.',
    'ins.DIN': 'Diverse Input – 2 komplementære kanaler.',
    'ins.ENPEN': 'Enable Pendant – aktiveringsanordning.',
    'ins.THRS': 'Two-Hand Run Station – tohåndsbetjening.', 'ins.THRSE': 'Two-Hand Run Station Enhanced.',
    'ins.DCS': 'Dual Channel Input Stop – konfigurerbar sikkerhedsfunktion, uoverensstemmelsestid, genstart MANUAL/AUTOMATIC.',
    'ins.DCST': 'Dual Channel Input Stop with Test.', 'ins.DCSTM': 'Dual Channel Input Stop with Test and Mute.',
    'ins.DCSTL': 'Dual Channel Input Stop with Test and Lock.', 'ins.DCSRT': 'Dual Channel Input Start.',
    'ins.DCM': 'Dual Channel Input Monitor.', 'ins.DCA': 'Dual Channel Analog Input.', 'ins.DCAF': 'Dual Channel Analog Input (flydende komma).',
    'ins.SMAT': 'Safety Mat – sikkerhedsmåtte.',
    'ins.ROUT': 'Redundant Output – redundant udgang med EDM-overvågning (Feedback).',
    'ins.CROUT': 'Configurable Redundant Output – redundant udgang med EDM-overvågning og reaktionstid for tilbagemelding.',
    'ins.TSAM': 'Two Sensor Asymmetrical Muting – asymmetrisk muting med to sensorer.', 'ins.TSSM': 'Two Sensor Symmetrical Muting – symmetrisk muting med to sensorer.',
    'ins.FSBM': 'Four Sensor Bidirectional Muting – tovejs muting med fire sensorer.',
    'ins.FPMS': 'Five Position Mode Selector – tilstandsvælger.', 'ins.EPMS': 'Eight Position Mode Selector – tilstandsvælger.',
    'ins.TON': 'Timer On Delay – tiltrækningsforsinkelse.', 'ins.TOF': 'Timer Off Delay – frafaldsforsinkelse (stopkategori 1).',
    'ins.RTO': 'Retentive Timer On.', 'ins.TONR': 'Timer On Delay with Reset.',
    'ins.TOFR': 'Timer Off Delay with Reset – frafaldsforsinkelse (stopkategori 1).', 'ins.RTOR': 'Retentive Timer On with Reset.',
    'ins.TONS': 'Sikkerhedstimer – tiltrækningsforsinkelse.', 'ins.TOFS': 'Sikkerhedstimer – frafaldsforsinkelse (stopkategori 1).',
    'ins.OSF / OSR': 'One Shot Falling / Rising – flankeimpuls (typisk til reset).',
    'ins.XIC / XIO': 'Sluttekontakt (tester 1) / brydekontakt (tester 0).',
    'ins.OTE / OTL / OTU': 'Spole / låsning (Latch) / oplåsning (Unlatch).',
    'ins..O1': 'Udgang fra en sikkerhedsinstruktion: 1 = sikker / armeret (OK), 0 = overtrædelse / udløst.',
    'ins..FP': 'Fault Present – instruktionen er i fejl (f.eks. kanaluoverensstemmelse, EDM-fejl).',
    'ins.unknown': 'Instruktion brugt i SafetyTask (se Rockwell-dokumentationen).',
    # ------------------------------------------------------------------ signaturforklaring (hjørne / blok)
    'lg.title': 'SIGNATURFORKLARING',
    'lg.ids': 'Komponent-ID: ',
    'lg.id_suffix': '  (TYPE zone.nr)',
    'lg.abbr_head': 'Forkortelser: ',
    'lg.abbr_line': 'R = rung (fra 0) · M/A = manuel/automatisk reset · Kat. 0 = STO / frakobling, Kat. 1 = SS1 · · = OG, ∥ = ELLER · '
                    'std = standardstyring · std-bit = SafetyTagMap-tag (standard → sikkerhed)',
    'lg.full_note': 'Komplet signaturforklaring med farver: under matrixen og i arket "Signaturforklaring".',
    'lg.read': 'Aflæsning',
    'lg.codes': 'Koder i matrixens celler',
    'lg.ids_head': 'Komponentbetegnelser (ID)',
    'lg.format': 'Format',
    'lg.id_format': 'ID-format: TYPE zone.nummer – f.eks. "ES 3.1" = nødstop nr. 1 i zone 3. ID tildeles fortløbende, medmindre det er angivet '
                    'i konfigurationen; Logix-tagget vises altid ved siden af.',
    'lg.kinds': 'Udgangstyper',
    'lg.abbr_main': 'Vigtigste forkortelser (komplet liste: arket "Signaturforklaring")',
    'read.gi': 'Aflæsning: række = udgang (virkning), kolonne = komponent (årsag). Celle = hvad der sker med udgangen i rækken, når komponenten i kolonnen udløser.',
    'read.motor': 'Aflæsning: række = komponent (årsag), kolonne = udgang (virkning). Hold musen over en farvet celle – kommentaren viser stien gennem rungs.',
    'read.valve': 'Opbygning som MOTOR (rækker = komponenter), kolonner = udgange markeret som ventiler i konfigurationen.',
    'abbr': [
        ['Saw R22', 'Rutine "Saw", rung 22. Rungs nummereres fra 0 – som i Studio 5000.'],
        ['M / A', 'Reset MANUAL (kræver en knap / flanke) / AUTOMATIC (automatisk, når årsagen er fjernet).'],
        ['Kat. 0 / Kat. 1', 'Stopkategori iht. IEC 60204-1: 0 = øjeblikkelig fjernelse af energi (STO), 1 = kontrolleret bremsning, derefter frakobling (SS1, frafaldsforsinkelse).'],
        ['STO / SS1', 'Safe Torque Off / Safe Stop 1.'],
        ['EDM', 'External Device Monitoring – tilbagemeldingssløjfe for kontaktorers / ventilers kontakter (Feedback ROUT/CROUT). Metadata – ikke en årsag.'],
        ['Enable Group', 'Betingelse (zonetag eller sæt af .O1-bits), der skal være opfyldt, for at udgangen kan indkobles.'],
        ['·   ∥   NOT', 'I logikbeskrivelser: · = OG (serie), ∥ = ELLER (parallel gren), NOT = XIO-kontakt.'],
        ['std', 'Standardstyring (programmer i standardtasks – ikke sikkerhed).'],
        ['SafetyTagMap', 'Mapning af et standardtag til et sikkerhedstag (std → sikkerhed). Kun tilladt til reset / diagnose, aldrig som kilde til en sikkerhedsfunktion.'],
        ['Module:4:O.Pt00', 'I/O-adresse: adapter "Module", slot 4, udgang ("O") punkt 00; ":I.Pt02" = indgang punkt 02; ":SO." / ":SI." = CIP Safety-udgang / -indgang på en frekvensomformer.'],
        ['CRTL', 'Connection Reaction Time Limit for en CIP Safety-forbindelse = RPI × (TM + NDM) for indgange (Rockwell 1756-RM012).'],
        ['[KRITISK ALARM]', 'Omgåelse / ikke-funktionel komponent eller std-tag, der opretholder sikkerhedslogikken – kræver korrektion.'],
        ['[SKAL VERIFICERES]', 'Uklarhed i koden eller beskrivelsen – skal kontrolleres på stedet / i diagrammerne (valideringsrapport, med rutine og rung).'],
        ['DØD', 'Komponent / tag / kanal, der ikke påvirker nogen sikkerhedsudgang.'],
    ],
    'colors': [
        ['Zone / udgangsgruppe', 'Zoneoverskrift (kolonne i Group Interlocks) eller udgangsgruppe (kolonne i MOTOR).'],
        ['ID / tag', 'Celle med komponent-ID eller udgangstag; zonerække i MOTOR/VALVE.'],
        ['Udgangsgruppe', 'Overskriftsrække for en udgangsgruppe i Group Interlocks.'],
        ['Komponenttype', 'Overskrift for komponenttype / kolonneoverskrifter.'],
        ['Metadata', 'Metadatarækker (reset, stopkategori, EDM). Rød tekst = advarsel (reset A, 0 udgange slået fra).'],
    ],
    'dv.err_title': 'Kode uden for forklaringen',
    'dv.err': 'Brug en kode fra signaturforklaringen: {codes} (eller tom).',
    'dv.prompt_title': 'Kode',
    'dv.prompt': 'Vælg en kode – se arket "Signaturforklaring".',
    # ------------------------------------------------------------------ Group Interlocks / MOTOR / VALVE
    'gi.effect': 'Udgang (virkning) – beskrivelse',
    'gi.tag': 'Udgangstag',
    'gi.enable': 'Enable Group',
    'gi.reset_row': 'Reset af komponent (M = MANUAL / A = AUTOMATIC)',
    'gi.cat_row': 'Stopkategori',
    'gi.count_row': 'Antal sikkerhedsudgange, der slås fra',
    'gi.valve_head': 'SIKKERHEDSVENTILER (skabelonens VALVE-afsnit)',
    'gi.valve_none': 'Ingen markeret – SafetyTask-udgangene er ikke identificeret som ventiler. Belastninger på ROUT/CROUT-udgange skal verificeres i diagrammerne.',
    'm.type': 'Type',
    'm.desc': 'Komponentbeskrivelse (program / I/O-kommentarer)',
    'm.id': 'ID / Logix-tag',
    'm.meta_head': 'METADATA FOR UDGANGE (EDM / RESET – metadatakolonner, ikke årsager)',
    'm.kind': 'Udgangstype',
    'm.addr': 'Adresse / IP',
    'm.rung': 'Udgangsrung',
    'm.enable': 'Enable Group (betingelse)',
    'm.edm': 'EDM / tilbagemelding',
    'm.reset': 'Reset af udgang',
    'm.restart': 'Genstart',
    'm.cat': 'Stopkategori',
    'm.count': 'Antal komponenter, der slår udgangen fra (X, X1, XB, XM, S, SB, SM) – formel',
    'v.legend_ref': 'Signaturforklaring: arket "Signaturforklaring" (komponent-ID TYPE zone.nr)',
    'v.none_head': 'INGEN SIKKERHEDSVENTILER IDENTIFICERET I SafetyTask',
    'v.none_text': 'Ingen udgang er markeret som ventil (pneumatik / hydraulik). Hvis udgangene {outs} forsyner ventiler – markér dem i konfigurationen (effects: <tag>: valve: true).',
    # ------------------------------------------------------------------ metadatatekster
    'edm.cip': 'SI.TorqueDisabled / SI.SafetyFault (CIP Safety)',
    'rs.rout_fault': '(reset af ROUT-fejl)',
    'rs.none': 'ingen (ingen selvhold – følger logikken)',
    'rs.so_reset': '  + SO.Reset-rung ({rung})',
    'restart.rout': 'AUTO – ROUT/CROUT-udgangen følger Enable (reset af komponenter = genstart)',
    'restart.rout_seal': 'MANUEL – ROUT/CROUT-rungen har start / selvhold: genstart kun med {tags}',
    'restart.auto': 'AUTO – niveausignal i selvholdsgrenen: {tags}',
    'restart.manual': 'MANUEL – resetflanke + selvhold',
    'restart.follow': 'følger logikken',
    # ------------------------------------------------------------------ arket Komponenter
    'd.zone': 'Zone', 'd.id': 'ID', 'd.type': 'Type', 'd.tag': 'Logix-tag', 'd.desc': 'Beskrivelse', 'd.instr': 'Instruktion',
    'd.cha': 'Kanal A', 'd.chb': 'Kanal B', 'd.routine': 'Rutine', 'd.rung': 'Rung', 'd.reset_type': 'Reset (type)',
    'd.reset_tag': 'Reset-tag', 'd.reset_src': 'Reset-kilde (fysisk / logisk)', 'd.reset_rung': 'Reset-rung',
    'd.mute': 'Muting (Mute-indgang)', 'd.n_eff': 'Antal sikkerhedsudgange slået fra', 'd.cat': 'Stopkat.', 'd.status': 'Status',
    'st.dead': 'DØD – ingen virkning på sikkerhedsudgange', 'st.auto': 'AUTO-reset', 'st.equal': 'Kanaler A = B (enkeltkanals)',
    'st.const': 'Konstante indgange', 'st.std': 'Indgange fra standardstyringen (SafetyTagMap)', 'st.mute': 'Muting fra standardstyringen',
    'st.direct': 'Direkte indgang uden sikkerhedsinstruktion', 'st.external': 'Consumed sikkerhedstag', 'st.heuristic': 'Operander udledt – verificér',
    # ------------------------------------------------------------------ arket Udgange
    'o.group': 'Gruppe', 'o.tag': 'Tag', 'o.desc': 'Beskrivelse', 'o.kind': 'Type', 'o.addr': 'Adresse / IP', 'o.rung': 'Udgangsrung',
    'o.enable': 'Enable Group', 'o.enable_rung': 'Enable-rung', 'o.logic': 'Enable-logik (fra rungen; · = OG, ∥ = ELLER)',
    'o.edm': 'EDM / tilbagemelding', 'o.reset': 'Reset', 'o.restart': 'Genstart', 'o.cat': 'Stopkategori', 'o.crtl': 'Output CRTL [ms]',
    'o.aux_head': 'SIKKERHEDSUDGANGE UDEN FOR MATRIXEN (ingen indgangskomponent i deres logik eller ikke indkoblet i fejlfri tilstand) – se valideringsrapporten',
    'o.reason.no_device': 'Ingen sikkerhedsindgangskomponent i logikken (f.eks. oplåsning af dørlås, lampe, anmodning) – ikke en stopfunktion.',
    'o.reason.not_energized': 'Ikke indkoblet i fejlfri tilstand (kræver en anmodning / sekvens for at indkoble).',
    # ------------------------------------------------------------------ arket Stier
    'p.dev': 'Komponent (årsag)', 'p.eff': 'Udgang (virkning)', 'p.code': 'Kode',
    'p.path': 'Logisk sti (tag [rutine rung]) – fra indgangsinstruktionen til udgangen',
    'p.extra': 'Omgåelsesbit (std) / OR-partner / betingelse',
    # ------------------------------------------------------------------ Rapport
    'r.title': 'VALIDERINGSRAPPORT – AUDIT AF GuardLogix-KODEN (SafetyTask)',
    'r.note': 'Rungs nummereres fra 0 (som i Studio 5000). Udførelsesrækkefølge: {order}. Betegnelser: arket "Signaturforklaring". '
              'Rapporten er genereret automatisk – hvert punkt skal vurderes af en kompetent person.',
    'r.sec_alarm': '1. FUNDNE OMGÅELSER / IKKE-FUNKTIONELLE KOMPONENTER / AFI   [KRITISK ALARM]   ({n})',
    'r.sec_dead': '2. DØDE INDGANGE / UDGANGE / TAGS   ({n})',
    'r.sec_verify': '3. PUNKTER [SKAL VERIFICERES]   ({n})',
    'r.cols_alarm': [['Nr.', 'Rutine', 'Rung', 'Element', 'Konstatering', 'Anbefaling']],
    'r.cols_dead': [['Nr.', 'Rutine', 'Rung', 'Element', 'Konstatering', 'Klassifikation']],
    'r.cols_verify': [['Nr.', 'Rutine', 'Rung', 'Element', 'Konstatering', 'Handling']],
    'r.none': 'Ingen punkter fundet.',
    'r.priority': 'PRIORITET: ',
    # ------------------------------------------------------------------ konstateringer: ALARM
    'f.const_channels': 'Instruktionen {instr} {tag} har konstante kanalindgange ({cha}, {chb}) – den kan ALDRIG udløse, men dens udgang bruges i: {uses}. '
                        'Den giver en falsk følelse af beskyttelse.',
    'f.const_channels.rec': 'Tilslut de fysiske kanaler til instruktionen eller fjern komponenten fra sikkerhedsdokumentationen; kontrollér ledningsføringen.',
    'f.std_channels': 'Kanal A/B i {instr} {tag} kommer fra STANDARDtags mappet via SafetyTagMap ({cha}, {chb}). Kilde: {src}. '
                      'Funktionen har ingen sikkerhedsintegritet.',
    'f.std_channels.rec': 'Tilslut komponenten til et sikkerhedsindgangsmodul eller overfør signalet som produced/consumed safety tag mellem sikkerhedscontrollere.',
    'f.std_bypass': 'Standardbitten {bit} ligger i en parallel gren med sikkerhedsbetingelsen – med bit = 1 slår komponenterne {devices} ikke fra: {effects}. '
                    'Bittens kilde: {src}. Et SafetyTagMap-tag opretholder direkte sikkerhedslogikken.',
    'f.std_bypass.rec': 'Fjern omgåelsen fra standardstyringen; er en betingelse nødvendig, så byg den af sikkerhedsindgange / -instruktioner (f.eks. muting med TSAM/TSSM/FSBM).',
    'f.std_mute': 'Muting af {tag} ({instr}, operand {operand}) styres af standardbit(s) {bits}. Kilde: {src}.',
    'f.std_mute.rec': 'Udfør kun muting med TSAM/TSSM/FSBM og muting-sensorer på sikkerhedsindgange; mute ikke fra standardstyringen.',
    'f.mute_const': 'Mute-indgangen på {tag} er konstanten 1 – lysgardinet er permanent mutet.',
    'f.mute_const.rec': 'Tilslut Mute-indgangen til en sikker muting-funktion eller sæt den til 0.',
    'f.std_parallel': 'Standardbitten {bit} kan alene sætte {tag}, hvis logik ellers kræver betingelser fra sikkerhedsindgange: {expr}. Kilde: {src}.',
    'f.std_parallel.rec': 'Fjern standardgrenen eller erstat den med et sikkerhedssignal (f.eks. sikker stilstandsovervågning via CIP Safety).',
    'f.estop_auto': 'Nødstoppet/-ene {tags} har AUTOMATIC reset – når knappen frigives, er O1 = 1, og udgangene {effects} kan indkoble igen uden manuel reset '
                    '(ISO 13850: reset af et nødstop skal være en bevidst manuel handling og må ikke starte maskinen).',
    'f.estop_auto.rec': 'Sæt Reset Type til MANUAL med en resetknap uden for fareområdet; kontrollér, at ingen udgang genstarter automatisk.',
    'f.equal_channels': 'Begge kanaler i {instr} {tag} peger på samme indgang {ch} – ingen redundans og ingen detektering af uoverensstemmelse; funktionen er '
                        'reelt enkeltkanals ({n} sikkerhedsudgang(e) berørt).',
    'f.equal_channels.rec': 'Tilslut kanal B til en separat indgang og ret operanden; kontrollér sensorens ledningsføring.',
    'f.afi': 'AFI-instruktion (Always False) i {rung} – rungen er permanent deaktiveret; den slår permanent fra: '
             '{outputs}.',
    'f.afi.rec': 'Fjern AFI eller dokumentér årsagen; kontrollér, at ingen sikkerhedsfunktion afhænger af rungen.',
    'f.const_branch': 'En gren, der kun består af konstante kontakter ({consts}), er altid sand og kortslutter '
                      'logikken for {tag}. Kortsluttede komponenter: {devices}.',
    'f.const_branch.rec': 'Fjern den kortsluttende gren eller erstat konstanten med en reel sikkerhedsbetingelse.',
    'f.reset_std_auto': 'Resetbitten {bit} genereres automatisk (låst i standardsekvensen eller skrevet af selve SafetyTask) og nulstiller: {resets}. '
                        'Kilde: {src}. Reset uden bevidst handling fra operatøren.',
    'f.reset_std_auto.rec': 'Reset kun med trykknap (flanke) uden for fareområdet; fjern automatiske resetkilder fra standardstyringen.',
    # ------------------------------------------------------------------ konstateringer: DØDE
    'f.dead_device': 'Udgangen fra {tag} slår ingen sikkerhedsudgang fra; den bruges kun i: {uses}.',
    'f.dead_muting': 'Udgangen .O1 fra muting-instruktionen {tag} bruges ikke i nogen rung.',
    'f.const_tags': 'Tags, der aldrig skrives i SafetyTask (konstante startværdier), men læses i logikken: {tags}.',
    'f.unused_tags': 'Sikkerhedstags, der er defineret, men ikke bruges i den udførte SafetyTask-logik: {tags}.',
    'f.unused_inputs': 'Sikkerhedsindgange på modulet {module}, der ikke bruges i SafetyTask: {channels}.',
    'f.unused_outputs': 'Sikkerhedsudgange på modulet {module}, der ikke bruges i SafetyTask: {channels}.',
    'f.unused_module': 'Sikkerhedsindgangsmodul {module} – ingen af dets indgange bruges i SafetyTask.',
    'f.uncalled_routine': 'Rutinen {routine} ({n} rungs) kaldes aldrig (ingen JSR) – dens logik udføres ikke.',
    'f.drive_unused': 'Frekvensomformeren {module} har en CIP Safety-forbindelse, men ingen reference i SafetyTask.',
    'f.module_unused': 'Modulet {module} har en sikkerhedsforbindelse, men ingen reference i SafetyTask.',
    'f.drives_hardwired': 'Frekvensomformere uden CIP Safety-forbindelse (eventuel kablet STO er uden for koden): {modules}.',
    'cls.dead_input': 'Død indgang (for sikkerhedsudgange)', 'cls.dead_block': 'Død blok', 'cls.const_tag': 'Konstante tags',
    'cls.dead_tags': 'Døde tags', 'cls.dead_channel': 'Døde kanaler', 'cls.dead_routine': 'Død rutine',
    'cls.outside_code': 'Uden for koden', 'cls.dead': 'Død',
    # ------------------------------------------------------------------ konstateringer: SKAL VERIFICERES
    'f.aux_no_device': 'Sikkerhedsudgangen {tag} slås ikke fra af nogen sikkerhedsindgangskomponent (logik: {expr}) – f.eks. oplåsning af dørlås eller signallampe. '
                       'Kontrollér funktionen og dens betingelser.',
    'f.aux_not_energized': 'Sikkerhedsudgangen {tag} er ikke indkoblet i fejlfri tilstand (logik: {expr}) – ikke vist i matrixen; kontrollér funktionen.',
    'f.crtl_inputs': 'Sikkerhedsindgange på {adapter}: RPI {rpi} ms, Timeout Multiplier {tm}, Network Delay '
                     'Multiplier {ndm} % → Input CRTL {crtl} ms. Værste reaktionstid for logikken alene (Input CRTL '
                     '+ LC-filter + taskperiode {period} ms + watchdog {watchdog} ms + Output CRTL) op til {total} '
                     'ms – uden sensor- og stoptider. Komponenter: {devices}. Verificér mod risikovurderingen og '
                     'sikkerhedsafstandene (ISO 13855); detaljer: arket "Sikkerhedsfunktioner". Medregnet '
                     'forsinkelse fra scanningsrækkefølgen: {lags} × taskperiode.',
    'f.crtl_outputs': 'Sikkerhedsudgangsmoduler {modules}: RPI {rpi} ms, TM {tm}, NDM {ndm} % → Output CRTL {crtl} ms.',
    'f.crtl_drives': 'CIP Safety-udgangsforbindelser til frekvensomformere: RPI {rpi} ms, TM {tm}, NDM {ndm} % → CRTL {crtl} ms for: {modules}.',
    'f.osf_ote': 'OSF/OSR og OTE på samme tag {tag} i én rung – OTE overskriver flankeimpulsen med niveauet (niveaureset i stedet for flankereset).',
    'f.double_ote': 'Tagget {tag} skrives af {n} OTE-spoler – kun den sidste i scanningen bestemmer værdien.',
    'f.rout_reset_fp': 'Fejlreset {reset} for {tag} er betinget af {other} (fejl i en ANDEN udgangsinstruktion) – sandsynlig kopieringsfejl.',
    'f.or_devices': 'Komponenterne {a} og {b} er parallelforbundet (ELLER) – udløsning af den ene slår ikke {effects} fra (kode XC). Bekræft mod risikovurderingen.',
    'f.auto_restart': 'Selvholdsgrenen for {tag} indeholder et niveausignal ({levels}) – udgangen genstarter automatisk, når det vender tilbage (ingen uafhængig reset).',
    'f.auto_reset_guard': 'Afskærmningskomponenten {tag} har AUTOMATIC reset – efter lukning kan udgangene {effects} genstarte uden reset. Bekræft, at genstart '
                          'ikke kan ske, mens en person er i fareområdet (ISO 13849-1 §5.2.2, ISO 14119).',
    'f.reset_std': 'Reset fra standardstyringen: bit {bit} nulstiller {resets}. Kilde: {src}. Kontrollér placering og synlighed af resetknappen '
                   '(manuel reset uden for fareområdet, ISO 13849-1 §5.2.2).',
    'f.std_not_written': 'Den std-mappede bit {bit} læses i SafetyTask, men der er ikke fundet nogen skrivning til '
                         '{src} i standardkoden. Kun HMI/SCADA, en MSG-instruktion eller en online-ændring kan sætte '
                         'den.',
    'f.missing_comments': 'Ingen I/O-kanalkommentarer på {module} ({channels}) – tildeling af {who} kun ud fra tagnavne.',
    'f.free_cmp': 'Sammenligning {leaf} i logikken for {effects} – antaget {value} i fejlfri tilstand; resultatet afhænger af data.',
    'f.free_data': 'Dataafhængig bit {leaf} (skrevet af en datainstruktion) i logikken for {effects} – antaget {value} i fejlfri tilstand.',
    'f.free_latch': 'Låst bit {leaf} (OTL/OTU) i logikken for {effects} – antaget {value} i fejlfri tilstand; kontrollér låse- / oplåsningsbetingelserne.',
    'f.free_unk': 'Bit {leaf} med ukendt værdi i logikken for {effects} – antaget {value}.',
    'f.free_mute': 'Muting af {leaf} påvirker {effects} – mens muting er aktiv, udløser lysgardinet ikke (kode XM).',
    'f.free_ext': 'Consumed sikkerhedstag {leaf} i logikken for {effects} – kontrollér den producerende controller.',
    'f.direct_direct': 'Sikkerhedsindgangen {tag} bruges direkte i logikken for {effects} uden sikkerhedsindgangsinstruktion (ingen overvågning af uoverensstemmelse).',
    'f.direct_external': 'Consumed sikkerhedstag {tag} slår {effects} fra – funktionen er realiseret i en anden controller.',
    'f.heuristic': 'Operanderne i {instr} {tag} er tildelt heuristisk ({roles}) – bekræft kanaler og reset i Studio 5000.',
    'f.device_conditional': 'Sikkerhedsindgangsinstruktionen {tag} står i en betinget rung – når rungen er falsk, nulstilles udgangen .O1.',
    'f.routine_not_analysed': 'Rutinen {routine} ({kind}) kunne ikke analyseres (beskyttet eller ikke ladder) – dens logik afspejles ikke i matrixen.',
    'f.aoi_conditional': 'Add-On Instruction {aoi} kaldes i en betinget rung – analysen antager EnableIn = 1.',
    'f.flow': 'Programforløbsinstruktion {instr} i SafetyTask – matrixen forudsætter kontinuerlig udførelse af hver rung.',
    'f.unknown_instr': 'Instruktionen {instr} er ukendt for analysatoren – behandlet som gennemgående; kontrollér dens virkning manuelt.',
    'f.aoi_protected': 'Add-On Instruction {aoi} ({inst}) er kildebeskyttet – dens udgange behandles som ukendte.',
    'f.jsr_conditional': 'Rutinen {routine} kaldes betinget – udgange i den bevarer deres tilstand, mens den ikke udføres.',
    'f.pair_mismatch': 'Udgangene {a} og {b} på {tag} har forskellige årsager i logikken – kontrollér ledningsføringen af begge kanaler.',
    'f.loads': 'Koden definerer ikke, hvad der forsynes fra udgangene {outputs} (kontaktorer / kablet STO / ventiler) – bekræft i el-diagrammerne.',
    'f.stop_cat0': 'Ingen frafaldsforsinkelse ligger på en vej sikkerhedskomponent → udgang, så alle '
                   'sikkerhedsfunktioner er stopkategori 0 (STO / kontaktorfrafald). For maskiner med stor inerti '
                   'bør SS1 overvejes iht. risikovurderingen.',
    'f.stop_cat1': 'Frafaldsforsinkelser på veje sikkerhedskomponent → udgang: {timers} – udgangene {effects} '
                   'stopper i kategori 1 (SS1); kontrollér forsinkelsen mod stoptiden.',
    'f.forces': 'Forces gemmes ikke i eksporten – kontrollér fanen Forces for sikkerhedstags online i Studio 5000.',
    'f.completeness': 'Analyseret fil {src}; udførte rutiner og antal rungs: {routines}. Bekræft antallet af rungs i Studio 5000.',
    'f.afi_noop': 'AFI (Always False) i {rung} på en rung uden udgangsinstruktioner (f.eks. kun NOP) – ingen '
                  'virkning på logikken i dag, men det er en deaktiveret rung i sikkerhedsopgaven.',
    'f.afi_noop.rec': 'Fjern rungen eller dokumentér dens formål; kontrollér, at der ikke skulle have været en '
                      'sikkerhedsfunktion.',
    'f.map_written': 'Sikkerhedstagget {tag} er destination i SafetyTagMap (fra standardtagget {src}) og skrives '
                     'også af sikkerhedslogikken i {writers}. Standardværdien kopieres ved starten af hver scanning '
                     'af sikkerhedsopgaven og overskrives derefter – mappingen har ingen virkning og er vildledende.',
    'f.map_written.rec': 'Fjern mappingen eller brug et separat sikkerhedstag til logikkens resultat; dokumentér, '
                         'hvilken kilde der er tilsigtet.',
    'f.map_read_before_write': 'Sikkerhedstagget {tag} mappes fra standardtagget {src} (SafetyTagMap) og skrives af '
                               'sikkerhedslogikken i {writers}, men læses tidligere i scanningen i {readers} – dér '
                               'kommer værdien fra STANDARDstyringen.',
    'f.map_read_before_write.rec': 'Fjern mappingen eller flyt sikkerhedsskrivningen før enhver læsning; '
                                   'standardværdien må ikke påvirke sikkerhedsfunktionen.',
    'f.aux_always_on': 'Sikkerhedsudgangen {tag} er aktiveret ubetinget (logik: {expr}) – ingen sikkerhedskomponent '
                       'kan slå den fra (f.eks. forsyning til en sensor eller testkilde).',
    'f.aux_always_on.rec': 'Bekræft i diagrammerne, hvad der forsynes fra denne udgang; der må ikke være tilsluttet '
                           'en farlig belastning.',
    'f.aux_inverse': 'Sikkerhedsudgangen {tag} aktiveres kun, når {devices} udløser (logik: {expr}) – signallampe, '
                     'frigivelse af låsning eller lignende, ikke en udgang for en sikkerhedsfunktion; vises ikke i '
                     'matrixen.',
    'f.aux_inverse.rec': 'Kontrollér funktionen; hvis den frigiver en låsning, kontrollér betingelserne (stilstand, '
                         'forsinkelse).',
    'f.channel_copy': 'Kanalerne i disse instruktioner er mellemliggende tags kopieret fra fysiske indgange '
                      '(XIC(indgang) OTE(kopi)): {devices}. Kopierne skrives før instruktionen i scanningen; matrix, '
                      'CRTL og I/O-kommentarer bruger de fysiske indgange.',
    'f.channel_copy.rec': 'Kopi-rungs må ikke have ekstra betingelser; det er tydeligere at bruge de fysiske '
                          'indgange direkte i instruktionen.',
    'f.channel_copy_late': 'Kanalerne i disse instruktioner er mellemliggende tags kopieret fra fysiske indgange, og '
                           'kopi-rungs udføres EFTER instruktionen i scanningen: {devices}. Instruktionen vurderer '
                           'indgangstilstanden fra den forrige scanning – reaktionstiden øges med én '
                           'SafetyTask-periode ({period} ms).',
    'f.channel_copy_late.rec': 'Flyt kopi-rungs før instruktionerne (JSR-rækkefølge i MainRoutine) eller brug de '
                               'fysiske indgange direkte; medregn den ekstra periode i reaktionstiden.',
    'f.channel_logic': 'Kanal {ch} i {instr} {tag} er ikke en fysisk indgang, men et tag beregnet af logikken: '
                       '{expr}. Instruktionens redundans og uoverensstemmelsesovervågning gælder så denne logik, '
                       'ikke sensoren.',
    'f.channel_logic.rec': 'Forbind de fysiske kanaler direkte til instruktionen, eller begrund logikken i '
                           'sikkerhedskonceptet.',
    'f.scan_lag': 'Tagget {tag} skrives i {writer}, men læses tidligere i scanningen i {readers} – disse rungs '
                  'bruger værdien fra den forrige scanning: +1 SafetyTask-periode ({period} ms) i reaktionstiden '
                  'for: {effects}.',
    'f.scan_lag.rec': 'Ændr rækkefølgen af rutiner / rungs, så tagget skrives før det læses, eller medregn den '
                      'ekstra periode i reaktionstiden.',
    'f.edm_same_channel': 'Begge tilbagemeldingsindgange i {instr} {tag} bruger samme kanal {ch} – hjælpekontakterne '
                          'fra begge kontaktorer er seriekoblet til én indgang; en fejl i denne ene indgang eller '
                          'ledning opdages ikke af EDM.',
    'f.edm_same_channel.rec': 'Kontrollér, at dette opfylder den krævede kategori / PL; ellers skal hver '
                              'tilbagemelding forbindes til sin egen indgang.',
    'f.rout_extra_logic': 'Udgangene {outputs} fra {instr} {tag} slås også fra af {devices}, som ikke virker gennem '
                          '{instr}-frigivelsen. Når kun disse udløser, falder udgangene, mens {tag}.O1 forbliver '
                          'aktiv – tilbagemeldingen passer ikke længere, {tag} melder tilbagemeldingsfejl (reset '
                          'påkrævet), og EDM overvåger ikke denne frakoblingsvej.',
    'f.rout_extra_logic.rec': 'Inkludér disse betingelser i frigivelsen af {tag}, så enhver frakoblingsvej går '
                              'gennem den overvågede instruktion.',
    'f.timer_other': 'Frafaldsforsinkelsen {tag} ({instr}, preset {preset} ms) ligger ikke på en vej '
                     'sikkerhedskomponent → udgang: den forsinker betingelsen {cond}; bruges af: {users}. Det er '
                     'ikke stopkategori 1 for en sikkerhedsfunktion (f.eks. forsinkelse af låsning eller '
                     'frigivelse).',
    'f.timer_other.rec': 'Hvis den frigiver en låsning, kontrollér forsinkelsen mod maskinens udløbstid.',
    # ------------------------------------------------------------------ arket Signaturforklaring
    'l.title': 'SIGNATURFORKLARING OG METODE',
    'l.s1': '1. KODER I MATRIXENS CELLER', 'l.s2': '2. AFLÆSNING AF MATRIXEN', 'l.s3': '3. KOMPONENTBETEGNELSER (ID)', 'l.s4': '4. ZONER',
    'l.s5': '5. UDGANGSTYPER (VIRKNINGER)', 'l.s6': '6. ANVENDTE SIKKERHEDSINSTRUKTIONER', 'l.s7': '7. FORKORTELSER I METADATA / RAPPORT',
    'l.s8': '8. FARVER PÅ OVERSKRIFTER OG RÆKKER', 'l.s9': '9. METODE OG BEMÆRKNINGER', 'l.s10': '10. ARK I PROJEKTMAPPEN',
    'l.s11': '11. FELTER TIL UDFYLDNING OG TESTRESULTATER', 'l.s12': '12. REVISIONSHISTORIK', 'l.s13': '13. KILDER',
    'l.cols_codes': [['Kode', 'Betydning (kort)', 'Fuld beskrivelse', 'Antal – MOTOR', 'Antal – Group Interl.']],
    'l.sheet': 'Ark', 'l.axes': 'Akser', 'l.id_abbr': 'ID-forkortelse', 'l.type_hdr': 'Type (kolonneoverskrift)', 'l.meaning': 'Betydning',
    'l.instr': 'Instruktion', 'l.count': 'Antal', 'l.zone_no': 'Zone nr.', 'l.id_prefix': 'ID-præfiks', 'l.zone_name': 'Zonenavn',
    'l.kind': 'Type', 'l.mark': 'Betegnelse', 'l.sample': 'Eksempel', 'l.element': 'Element', 'l.contents': 'Indhold',
    'l.yellow': '(gul)', 'l.dropdown': 'Rulleliste',
    'l.dropdown_txt': 'Matrixcellerne (Group Interlocks, MOTOR) har en kodeliste og betinget formatering – en manuelt ændret kode får automatisk farven '
                      'fra signaturforklaringen. Bemærk: kommentaren med rung-stien beskriver tilstanden genereret fra programmet.',
    'l.rev': 'Revision', 'l.date': 'Dato', 'l.changes': 'Beskrivelse af ændringer', 'l.author': 'Forfatter', 'l.no': 'Nr.', 'l.doc': 'Dokument',
    'l.rev_auto': 'Genereret automatisk af safety-matrix-generator {version}.',
    'l.n.method': 'Metode: hvert krydsfelt er bestemt deterministisk ud fra SafetyTask-ladderlogikken (boolsk simulering af hver rung i scanningsrækkefølge): '
                  'komponent udløst (O1 = 0), øvrige komponenter fejlfri, standardbits = 0 → X; hvis en standardbit genopretter udgangen → XB; hvis en intern '
                  'betingelse genopretter den → XM; hvis udgangen kun falder sammen med en anden komponent → XC. Ingen forbindelse udledes af lighed i tagnavne.',
    'l.n.cat0': 'Stopkategori: der er ingen frafaldsforsinkelser i SafetyTask – alle funktioner er stopkategori 0 (STO via CIP Safety eller kontaktorfrafald via ROUT).',
    'l.n.cat1': 'Stopkategori: stier gennem frafaldsforsinkelser (TOF/TOFR/TOFS) er kategori 1 med timerens forindstilling vist i cellekommentaren og i metadata.',
    'l.n.edm': 'EDM / tilbagemelding og resetknapper vises kun i metadata (MOTOR – rækker under matrixen, arkene "Komponenter" og "Udgange"), aldrig som årsager.',
    'l.n.rout': 'ROUT/CROUT-udgange har to kanaler (f.eks. Pt00/Pt01) – matrixen har én kolonne pr. udgangsinstruktion (begge kanaler kontrolleres for identiske årsager).',
    'l.n.comment': 'Kommentarerne i MOTOR-cellerne indeholder stien tag [rutine R rung] fra indgangsinstruktionen til udgangen.',
    'l.n.ids': 'Komponent-ID (TYPE zone.nr) tildeles fortløbende, medmindre de er defineret i konfigurationen; Logix-tagget vises altid ved siden af.',
    'l.n.tool': 'Genereret med safety-matrix-generator {version} (forfatter: Robert Pietroń). Resultatet erstatter ikke validering iht. ISO 13849-2 / IEC 62061.',
    'input_note': 'Gule felter – skal udfyldes (data fra datablade, risikovurdering, SISTEMA eller testresultater). Alle øvrige felter er genereret fra programmet.',
    'result.OK': 'Testresultatet svarer til det forventede resultat.',
    'result.NOK': 'Testen fejlede – beskriv i bemærkningskolonnen og meld til korrektion.',
    'result.N/A': 'Ikke relevant / test ikke mulig (angiv årsagen).',
    # ------------------------------------------------------------------ Sikkerhedsfunktioner
    'sf.title': 'SIKKERHEDSFUNKTIONER – REAKTIONSTID OG PERFORMANCE LEVEL',
    'sf.method': 'Reaktionstid (værste tilfælde) = sensorforsinkelse + Input CRTL + LC-filter + (Safety Task-periode + watchdog) + Output CRTL + forsinkelse '
                 'i udgang / aktuator. Input CRTL = RPI × (TM + NDM); Output CRTL = Safety Task-periode × (TM + NDM − 1) – Rockwell 1756-RM012. CRTL-værdier '
                 'læst fra eksporten (ReactionTimeLimit); Safety Task: periode {period} ms, watchdog {watchdog} ms. Maskinens stoptid (ISO 13855) = '
                 'reaktionstid + bremse- / udløbstid – skal måles.',
    'sf.input_hint': 'Typiske kilder: reaktionstid for lysgardiner / scannere, kontaktorers frafaldstid – datablad; PLr – risikovurdering (ISO 13849-1, bilag A); PL/PFHd – SISTEMA.',
    'sf.cols': [['SF', 'ID', 'Komponenttag', 'Sikkerhedsfunktion', 'Udgange slået fra (X / X1 / XB / XM)', 'Stopkat.', 'Indgangsstruktur (fra koden)',
                 'Indgangsmodul (RPI / TM / NDM)', 'Input CRTL [ms]', 'LC-filter [ms]', 'Safety Task-periode + watchdog [ms]', 'Output CRTL maks. [ms]',
                 'Sensorforsinkelse [ms]', 'Forsinkelse udgang / aktuator [ms]', 'Reaktionstid – i alt [ms]', 'PLr (risikovurdering)', 'Kategori (B, 1–4)',
                 'Opnået PL / PFHd', 'Bemærkninger']],
    'sf.s.const': 'Konstante indgange – ingen funktion [ALARM]',
    'sf.s.direct': 'Direkte sikkerhedsindgang uden instruktion (enkeltkanals) [ALARM]',
    'sf.s.external': 'Consumed sikkerhedstag (funktion i en anden controller)',
    'sf.s.single': 'Enkeltkanals (kanal A = B) – {instr} [ALARM]',
    'sf.s.std': 'Kanaler fra standardstyringen (SafetyTagMap) – {instr} [ALARM]',
    'sf.s.two': 'Tokanals – {instr}',
    'sf.s.mute': '; muting fra standardstyringen [ALARM]',
    'sf.s.xb': '; std-omgåelse (XB)',
    'sf.s.xc': '; OR-gren (XC)',
    'sf.s.xm': '; intern betingelse (XM)',
    'sf.n.xc': 'Slår {effs} fra kun sammen med {partners} (OR-gren).',
    'sf.n.none': 'Ingen virkning på sikkerhedsudgange – funktionen er ikke realiseret i SafetyTask.',
    'sf.n.nonfunc': 'Ikke-funktionel komponent (konstante indgange) – funktionen virker ikke.',
    'sf.n.crtl': 'Input CRTL ≥ {ms} ms – se valideringsrapporten (PRIORITET).',
    'sf.n.std': 'Signal fra standardstyringen – reaktionstiden er ubestemt.',
    'sf.n.delay': 'Frafaldsforsinkelse i stien: {ms} ms (kategori 1) – lægges til reaktionstiden.',
    'sf.n.lag': 'Scanningsrækkefølgen tilføjer {n} SafetyTask-periode(r) ({ms} ms) – medregnet i taskkolonnen.',
    'sf.only_xc': 'kun med partner (XC): {effs}',
    'sf.cf_note': 'Rød sum: > 1000 ms; gul: 500–1000 ms (betinget formatering). Summen beregnes automatisk, når komponenternes forsinkelser er indtastet.',
    # ------------------------------------------------------------------ Testprotokol
    't.title': 'PROTOKOL FOR VALIDERINGSTEST AF SIKKERHEDSFUNKTIONERNE (ISO 13849-2)',
    't.pre': 'Forudsætninger: alle komponenter nulstillet, sikkerhedsudgange indkoblet (klar-tilstand), ingen personer i fareområderne, test uden materiale / '
             'i testtilstand. De forventede resultater er genereret fra SafetyTask-koden (MOTOR-matrixen) – afvigelse mellem virkelighed og forventning = NOK.',
    't.result_hint': 'Resultat: OK / NOK / N/A (liste). ',
    't.cols': [['Nr.', 'Testtype', 'ID / Tag', 'Beskrivelse af komponent / element', 'Testhandling', 'Forventet resultat (iht. SafetyTask-koden)',
                'Reset / genstart – forventet adfærd', 'Reference (rutine / rung)', 'Bemærkninger / alarm', 'Resultat', 'Dato', 'Udført af', 'Testbemærkninger']],
    't.k.func': 'Funktion', 't.k.or': 'OR-kombination', 't.k.byp': 'Std-omgåelse (dokumentation)', 't.k.edm': 'EDM', 't.k.comm': 'Kommunikationstab',
    't.act.xb': 'Omgåelsesbit(s) {bits} skal være inaktive.',
    't.act.mute': 'Muting inaktiv.',
    't.act.disc': '2) Uoverensstemmelsestest: med komponenten OK afbrydes kun kanal A ({a}), derefter kun kanal B ({b}).',
    't.exp.n': 'INGEN udløsning – instruktionen har konstante indgange i koden ({rung}); udgangene forbliver indkoblet. [KRITISK ALARM]',
    't.exp.nconst': 'INGEN udkobling for {outs} – komponenten er kortsluttet af den konstante kontakt {bits}; disse '
                    'udgange forbliver indkoblet. [KRITISK ALARM]',
    't.exp.off': '1) Slået fra: {outs}',
    't.exp.sto': ' (frekvensomformere: :SI.TorqueDisabled = 1)',
    't.exp.rest': '. Øvrige udgange uændrede.',
    't.exp.notoff': 'Slår IKKE fra: {effs} (OR-gren med {partners} – se OR-testen).',
    't.exp.disc': '2) {instr}.FP = 1 (uoverensstemmelsesfejl), O1 = 0 – frakobling som i 1); reset først muligt, når begge kanaler er genoprettet.',
    't.exp.disc_short': '2) {instr}.FP = 1 (uoverensstemmelsesfejl), O1 = 0.',
    't.exp.single': '2) Uoverensstemmelsestest IKKE MULIG – begge instruktionens kanaler på samme indgang. [KRITISK ALARM]',
    't.exp.xc_only': 'En enkelt udløsning slår INGEN sikkerhedsudgang fra; {effs} slår kun fra sammen med {partners} (OR-gren) – se OR-kombinationstesten.',
    't.exp.none': 'Ingen virkning på sikkerhedsudgange (komponenten styrer ingen udgang i SafetyTask) – bekræft designhensigten.',
    't.rst.manual': 'Komponent: MANUAL reset ({tag} [{rr}] ← {src}); uden reset er O1 = 0.',
    't.rst.auto': 'Komponent: AUTOMATIC reset – O1 vender selv tilbage, når årsagen er fjernet',
    't.rst.auto_estop': ' [ALARM: nødstop]',
    't.rst.follow': 'Komponent: reset iht. instruktionens konfiguration.',
    't.rs.rout': 'ROUT/CROUT-udgange ({outs}): indkobler af sig selv efter reset af komponenten (udgangen følger Enable).',
    't.rs.auto': 'Udgange {outs}: vender AUTOMATISK tilbage med {tags} [SKAL VERIFICERES].',
    't.rs.manual': 'Udgange ({n}: {outs}): reset påkrævet {resets}.',
    't.rs.follow': 'Udgange {outs}: følger logikken.',
    't.rs.where': 'Resetkilder for udgange: arket "Udgange".',
    't.note.xb': 'Omgåelse fra standardstyringen: {bits} – se OMGÅELSES-testen.',
    't.note.auto': 'AUTO-reset.',
    't.note.std': 'Kanaler fra standarddata – uoverensstemmelsestest på kildecontrollerens side.',
    't.or.act': '1) Udløs kun {a}. 2) Udløs kun {b}. 3) Udløs begge samtidig.',
    't.or.exp': '1), 2) {outs} forbliver INDKOBLET. 3) Slået fra: {outs}.',
    't.or.rst': 'Som i funktionstestene for begge komponenter.',
    't.or.note': 'Parallel OR-gren – bekræft mod risikovurderingen [SKAL VERIFICERES].',
    't.byp.act': 'Kontrolleret test, ingen personer i zonen: aktivér betingelsen, der sætter bit {bit} ({src}), og udløs derefter komponenten.',
    't.byp.exp': 'Iht. koden: {outs} forbliver INDKOBLET – funktionen er kortsluttet af standardstyringen. Efter rettelse af programmet: frakobling som i funktionstesten.',
    't.byp.note': '[KRITISK ALARM] – se valideringsrapporten.',
    't.edm.act_neg': 'Med udgangen frakoblet (zonen stoppet) afbrydes tilbagemeldingskredsen {fb} (simulering af svejset kontaktor – ingen brydekontakt); nulstil derefter komponenterne og forsøg at indkoble.',
    't.edm.act_pos': 'Med udgangen frakoblet kortsluttes tilbagemeldingen {fb} (tilbagemelding = 1 med udgangen frakoblet – simulering af svejset kontaktor); nulstil derefter komponenterne og forsøg at indkoble.',
    't.edm.exp': '{tag}.FP = 1 (EDM-fejl); udgangene {outs} indkobler IKKE.',
    't.edm.rst': 'Når årsagen er fjernet: fejlreset {reset} [{rr}] ← {src}.',
    't.comm.what': 'Adapter {name} ({cat}, {addr}) – Safety I/O-moduler',
    't.comm.act': 'Afbryd Ethernet-kablet til adapteren {name}, mens linjen kører.',
    't.comm.exp': 'Adapterens sikkerhedsindgange = 0 (forbindelsesstatus = fejl) → udløst: {ids}. Slået fra: {outs}.',
    't.comm.rst': 'Når forbindelsen er genoprettet: udgangene forbliver frakoblet, indtil komponenterne er nulstillet iht. funktionstestene.',
    't.comm.ref': 'I/O-konfiguration',
    't.comm.note': 'Detekteres senest efter modulernes Input CRTL ({crtl}).',
    't.drv.id': 'CIP Safety-frekvensomformere',
    't.drv.what': '{n} frekvensomformer(e) med CIP Safety',
    't.drv.act': 'For hver frekvensomformer: afbryd dens netværksforbindelse under drift.',
    't.drv.exp': 'Frekvensomformeren går i STO (tab af CIP Safety-forbindelsen); :SI.ConnectionFaulted = 1 blokerer :SO.SafeTorqueOff-rungen, hvor den bruges.',
    't.drv.rst': 'Efter genopretning: STO forbliver aktiv indtil reset (resetflanke + :SO.Reset).',
    't.drv.ref': 'STO-rungs ({routines})',
    't.summary': 'Sammenfatning',
    't.sum.count': 'Antal test',
    't.sum.open': 'Ikke udført',
    't.approve': 'Godkendelse af protokollen (navn, dato, underskrift):',
    't.done_by': 'Udført af', 't.checked_by': 'Kontrolleret af', 't.approved_by': 'Godkendt af',
    # ------------------------------------------------------------------ arket Start
    's.subtitle': 'Årsags-virkningsmatrix – GuardLogix {proc} {ver}, SafetyTask {period} ms, program {src}',
    's.author': 'Forfatter: {author}   •   Revision: {rev}   •   Dato: {date}',
    's.lang_label': 'Sprog',
    's.switch_hint': '◄ vælg et sprog på listen – alle ark skifter automatisk',
    's.dict_note': 'Teksterne hentes fra arket "{dict}" (oversættelserne kan rettes dér; en tom oversættelse viser den engelske tekst). '
                   'Matrixkoderne (X, X1, XB, XC, XM, N, S…) og programmets tags er ens på alle sprog.',
    's.sheet': 'Ark', 's.contents': 'Indhold', 's.summary': 'Sammenfatning', 's.value': 'Værdi',
    's.sum.devices': 'Indgangskomponenter (årsager)',
    's.sum.effects': 'Sikkerhedsudgange (virkninger) + informationssignaler',
    's.sum.cells': 'Krydsfelter X / X1 / XB / XC / XM / N i MOTOR-matrixen',
    's.sum.alarm': '[KRITISK ALARM] – punkter i rapporten',
    's.sum.dead': 'Døde elementer – punkter i rapporten',
    's.sum.verify': '[SKAL VERIFICERES] – punkter i rapporten',
    's.sum.tests': 'Test i valideringsprotokollen',
}
