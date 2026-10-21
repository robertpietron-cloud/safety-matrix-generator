# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/locales/pl.py
# Author  : Robert Pietroń
# Revision: 1.1.0 (2026-10-21)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: teksty polskie (te same klucze
#                        co katalog angielski).
#   1.1.0 (2026-10-21) - Texts of the new audit rules (SafetyTagMap target written,
#                        copied / computed channels, scan-order lag, EDM, ROUT
#                        extra logic, always-on / inverse outputs, AFI without
#                        outputs, timers outside device paths), constant bypass,
#                        ROUT/CROUT restart with a start / seal-in on its rung.
# =============================================================================
"""Teksty polskie."""

TEXT = {
    # ------------------------------------------------------------------ dokument
    'doc.title': 'SAFETY MATRIX – {name} (SafetyTask)',
    'doc.block': 'Autor: {author}   •   Rewizja: {rev}   •   Data: {date}',
    'doc.block_lang': '   •   Język: arkusz „Start”',
    'doc.source': 'Źródło: {src} • {proc} {ver} • SafetyTask {period} ms',
    'doc.subject': 'Macierz przyczynowo-skutkowa (Cause & Effect) – GuardLogix SafetyTask',
    # ------------------------------------------------------------------ nazwy arkuszy
    'sheet.start': 'Start',
    'sheet.legend': 'Legenda',
    'sheet.sf': 'Funkcje PL',
    'sheet.test': 'Protokół testów',
    'sheet.dev': 'Urządzenia',
    'sheet.out': 'Wyjścia',
    'sheet.path': 'Ścieżki C&E',
    'sheet.rep': 'Raport',
    'sheet.dict': 'Słownik',
    # ------------------------------------------------------------------ spis arkuszy
    'sl.start': 'Strona tytułowa: przełącznik języka, spis arkuszy, podsumowanie.',
    'sl.gi': 'Macierz wg wzorca: wiersze = wyjścia, kolumny = urządzenia; Enable Group; wiersze metadanych urządzeń; legenda.',
    'sl.motor': 'Macierz wg wzorca: wiersze = urządzenia, kolumny = wyjścia; komentarze ze ścieżką rungów; metadane wyjść (EDM, reset); legenda.',
    'sl.valve': 'Wg wzorca: zawory bezpieczeństwa (wyjścia oznaczone w konfiguracji jako zawory).',
    'sl.legend': 'Pełny słownik oznaczeń, metoda, historia rewizji, źródła.',
    'sl.sf': 'Funkcja bezpieczeństwa na urządzenie: wyjścia, struktura wejścia, czas reakcji (najgorszy przypadek) z parametrów połączeń CIP Safety, pola PLr / Kat. / PL do uzupełnienia.',
    'sl.test': 'Protokół walidacji (ISO 13849-2) wygenerowany z macierzy: test funkcji, rozbieżności kanałów, kombinacji OR, obejść std, EDM, utraty komunikacji; kolumny wyniku i podpisu.',
    'sl.dev': 'Kanały, instrukcja, rung, typ i źródło resetu, muting, status.',
    'sl.out': 'Adres/IP, Enable Group i jego logika, EDM, reset, restart, CRTL wyjścia; wyjścia poza macierzą.',
    'sl.path': 'Każde skrzyżowanie z pełną ścieżką tag [rutyna R rung] i bitem obejścia / partnerem OR.',
    'sl.rep': 'Alarmy krytyczne, martwe elementy, lista [DO WERYFIKACJI] – każda pozycja z rutyną i rungiem.',
    'sl.dict': 'Teksty wszystkich języków używane przez przełącznik języka – można tu poprawiać tłumaczenia.',
    # ------------------------------------------------------------------ strefy / grupy / opisy
    'zone.routine': 'STREFA {n} : rutyna {routine}',
    'zone.other': 'STREFA {n} : pozostałe urządzenia',
    'group.routine': 'RUTYNA {routine}',
    'group.info': 'SYGNAŁY DO STEROWANIA STANDARDOWEGO (INFO)',
    'group.other': 'POZOSTAŁE WYJŚCIA',
    'effdesc.ROUT': 'Wyjście bezpieczne {instr} {tag} – I/O: {io}',
    'effdesc.OUT': 'Wyjście bezpieczne {tag} – I/O: {io}',
    'effdesc.DRIVE': '{name} – {catalog} {kind} {desc}',
    'effdesc.INFO': 'Sygnał do sterowania standardowego {tag} – {io}',
    # ------------------------------------------------------------------ słowa
    'w.all': 'wszystkie ({n})',
    'w.zone_n': 'STREFA {n}',
    'w.nocomment': 'brak komentarza [DO WERYFIKACJI]',
    'w.bypass': 'Obejście (bit std): {bits}',
    'w.conditions': 'Chyba że (warunek wewnętrzny / muting): {bits}',
    'w.partners': 'Wyłącza dopiero razem z: {devs}',
    'w.delay': 'Timer opóźnionego wyłączenia w ścieżce: {ms} ms (kategoria zatrzymania 1)',
    'w.constbypass': 'Zmostkowane stałym stykiem (wartość początkowa 1, nigdy nie zapisywany): {bits}',
    'w.lag': 'Kolejność wykonania: +{n} okres(y) SafetyTask = {ms} ms (wartość z poprzedniego cyklu)',
    'src.const': '{op} = stała {v}',
    'src.never': '{op} – nigdy niezapisywany (nieużywany)',
    'src.literal': 'stała {v}',
    # ------------------------------------------------------------------ kody
    'code.blank': '(puste)',
    'code.X.short': 'Wyłącza wyjście bezpośrednio',
    'code.X.full': 'Wyzwolenie urządzenia (O1 = 0) bezpośrednio wyłącza wyjście bezpieczne (STO napędu lub odcięcie stycznika). '
                   'Ścieżka przez rungi: komentarz komórki (MOTOR) i arkusz „Ścieżki C&E”.',
    'code.X1.short': 'Wyłącza, ale urządzenie de facto 1-kanałowe  [ALARM]',
    'code.X1.full': 'Jak X, ale oba kanały instrukcji wskazują to samo wejście (lub wejście bezpośrednie bez instrukcji safety) – '
                    'brak redundancji i wykrywania rozbieżności kanałów. [ALARM KRYTYCZNY]',
    'code.XB.short': 'Wyłącza, ale może być obejście / muting ze sterowania std  [ALARM]',
    'code.XB.full': 'Wyłącza wyjście, ALE bit ze sterowania standardowego (SafetyTagMap) może tę funkcję zmostkować lub wyciszyć (muting). '
                    'Nazwa bitu obejścia: komentarz komórki / „Ścieżki C&E”. [ALARM KRYTYCZNY]',
    'code.XC.short': 'Wyłącza tylko razem z innym urządzeniem (gałąź OR)',
    'code.XC.full': 'Wyjście gaśnie dopiero, gdy wyzwolone jest TAKŻE urządzenie partnerskie (gałęzie równoległe OR). Pojedyncze wyzwolenie nie zatrzymuje. '
                    'Partner: komentarz komórki / „Ścieżki C&E”. [DO WERYFIKACJI]',
    'code.XM.short': 'Wyłącza, chyba że spełniony jest warunek wewnętrzny (muting / tryb / dane)',
    'code.XM.full': 'Wyłącza wyjście, ale warunek wewnętrzny SafetyTask (instrukcja mutingu, porównanie, przełącznik trybu, dane lub bit zatrzaskowy) '
                    'może je podtrzymać. Warunek: komentarz komórki / „Ścieżki C&E”. [DO WERYFIKACJI]',
    'code.N.short': 'W logice, ale niefunkcjonalne – nigdy nie zadziała  [ALARM]',
    'code.N.full': 'Urządzenie jest w ścieżce logicznej, ale nigdy nie wyłączy wyjścia: instrukcja ma stałe wejścia '
                   'kanałów albo urządzenie jest zmostkowane stałym stykiem (tag o wartości początkowej 1, którego '
                   'logika nigdy nie zapisuje). [ALARM KRYTYCZNY]',
    'code.S.short': 'Info: sygnał do sterowania std (nie wyjście bezpieczne)',
    'code.S.full': 'Kolumna informacyjna: stan przekazywany do sterowania STANDARDOWEGO (np. interlock do innej maszyny). Nie jest wyjściem bezpiecznym.',
    'code.SB.short': 'Jak S, z możliwym obejściem ze sterowania std',
    'code.SB.full': 'Jak S, z możliwym obejściem bitem standardowym (patrz XB).',
    'code.SC.short': 'Jak S, tylko razem z innym urządzeniem (OR)',
    'code.SC.full': 'Jak S, tylko łącznie z urządzeniem partnerskim (patrz XC).',
    'code.SM.short': 'Jak S, chyba że spełniony jest warunek wewnętrzny',
    'code.SM.full': 'Jak S, z warunkiem wewnętrznym, który może podtrzymać sygnał (patrz XM).',
    'code.none.short': 'Brak powiązania w kodzie SafetyTask',
    'code.none.full': 'Brak ścieżki logicznej w kodzie SafetyTask między urządzeniem a wyjściem.',
    # ------------------------------------------------------------------ typy urządzeń
    'type.EMERGENCY STOP': 'Wyłącznik awaryjny', 'type.SAFETY DOOR': 'Drzwi bezpieczeństwa', 'type.SAFETY GATE': 'Bramka bezpieczeństwa',
    'type.SAFETY SWITCH': 'Wyłącznik bezpieczeństwa', 'type.LIGHT CURTAIN': 'Kurtyna świetlna', 'type.SAFETY SCANNER': 'Skaner bezpieczeństwa',
    'type.SAFETY MAT': 'Mata bezpieczeństwa', 'type.TWO-HAND CONTROL': 'Sterowanie oburęczne', 'type.ENABLING DEVICE': 'Urządzenie zezwalające',
    'type.ANALOG SAFETY INPUT': 'Analogowe wejście bezpieczne', 'type.SAFETY INPUT': 'Wejście bezpieczne',
    'type.DIRECT SAFETY INPUT': 'Bezpośrednie wejście bezpieczne', 'type.EXTERNAL SAFETY SIGNAL': 'Zewnętrzny sygnał bezpieczeństwa',
    'typedesc.EMERGENCY STOP': 'wyłącznik bezpieczeństwa (E-stop, grzybek)',
    'typedesc.SAFETY DOOR': 'drzwi / osłona ruchoma (czujnik drzwi, rygiel)',
    'typedesc.SAFETY GATE': 'bramka / furtka dostępu',
    'typedesc.SAFETY SWITCH': 'wyłącznik bezpieczeństwa (pozycyjny / blokujący)',
    'typedesc.LIGHT CURTAIN': 'kurtyna / siatka świetlna',
    'typedesc.SAFETY SCANNER': 'laserowy skaner bezpieczeństwa',
    'typedesc.SAFETY MAT': 'mata naciskowa bezpieczeństwa',
    'typedesc.TWO-HAND CONTROL': 'urządzenie sterowania oburęcznego',
    'typedesc.ENABLING DEVICE': 'urządzenie zezwalające / panel z przyciskiem zezwolenia',
    'typedesc.ANALOG SAFETY INPUT': 'dwukanałowe analogowe wejście bezpieczne',
    'typedesc.SAFETY INPUT': 'dwukanałowe wejście bezpieczne (typ nierozpoznany z programu – patrz opis)',
    'typedesc.DIRECT SAFETY INPUT': 'wejście bezpieczne użyte w logice bezpośrednio, bez instrukcji wejściowej safety',
    'typedesc.EXTERNAL SAFETY SIGNAL': 'sygnał bezpieczeństwa z innego sterownika (tag produced/consumed safety)',
    'fn.EMERGENCY STOP': 'Zatrzymanie awaryjne', 'fn.SAFETY DOOR': 'Blokada osłony – otwarcie drzwi zatrzymuje',
    'fn.SAFETY GATE': 'Blokada bramki – otwarcie zatrzymuje', 'fn.SAFETY SWITCH': 'Wyłącznik bezpieczeństwa',
    'fn.LIGHT CURTAIN': 'Zatrzymanie po przerwaniu kurtyny', 'fn.SAFETY SCANNER': 'Zatrzymanie po naruszeniu pola skanera',
    'fn.SAFETY MAT': 'Zatrzymanie po wejściu na matę', 'fn.TWO-HAND CONTROL': 'Sterowanie oburęczne',
    'fn.ENABLING DEVICE': 'Funkcja zezwolenia', 'fn.ANALOG SAFETY INPUT': 'Analogowy próg bezpieczeństwa',
    'fn.SAFETY INPUT': 'Funkcja wejścia bezpiecznego', 'fn.DIRECT SAFETY INPUT': 'Bezpośrednie wejście bezpieczne',
    'fn.EXTERNAL SAFETY SIGNAL': 'Blokada z innego sterownika bezpieczeństwa',
    'act.EMERGENCY STOP': 'Wciśnij wyłącznik awaryjny', 'act.SAFETY DOOR': 'Otwórz drzwi', 'act.SAFETY GATE': 'Otwórz bramkę',
    'act.SAFETY SWITCH': 'Zadziałaj wyłącznikiem bezpieczeństwa', 'act.LIGHT CURTAIN': 'Przerwij pole kurtyny wałkiem testowym',
    'act.SAFETY SCANNER': 'Wprowadź obiekt testowy w pole ochronne skanera', 'act.SAFETY MAT': 'Wejdź na matę bezpieczeństwa',
    'act.TWO-HAND CONTROL': 'Zwolnij jeden z przycisków oburęcznych', 'act.ENABLING DEVICE': 'Zwolnij przycisk zezwolenia',
    'act.ANALOG SAFETY INPUT': 'Wyprowadź sygnał analogowy poza próg bezpieczeństwa', 'act.SAFETY INPUT': 'Rozewrzyj obwód wejścia bezpiecznego',
    'act.DIRECT SAFETY INPUT': 'Rozewrzyj obwód wejścia', 'act.EXTERNAL SAFETY SIGNAL': 'Wyzwól funkcję bezpieczeństwa w sterowniku produkującym sygnał',
    # ------------------------------------------------------------------ typy wyjść
    'kindshort.ROUT': 'ROUT', 'kindshort.CROUT': 'CROUT', 'kindshort.OUT': 'Wyjście safety', 'kindshort.STO': 'STO CIP Safety',
    'kindshort.SS1': 'SS1 CIP Safety', 'kindshort.SBC': 'SBC CIP Safety', 'kindshort.SLS': 'SLS CIP Safety', 'kindshort.INFO': 'Bit std (info)',
    'kind.ROUT': 'Redundant Output – para wyjść safety sterująca stycznikami / zaworami bezpieczeństwa ze sprzężeniem EDM (NEGATIVE: wyjście ON → feedback OFF; '
                 'POSITIVE: feedback zgodny z wyjściem). Wyjścia podążają za Enable – reset ROUT kasuje tylko błąd.',
    'kind.CROUT': 'Configurable Redundant Output – jak ROUT, z czasem reakcji sprzężenia zwrotnego i monitorowaniem Input/Output Status.',
    'kind.OUT': 'Punkt wyjścia safety zapisywany cewką (OTE) bez instrukcji wyjściowej z EDM.',
    'kind.STO': 'Napęd przez CIP Safety: :SO.SafeTorqueOff = 1 zezwolenie na moment, 0 = STO. Reset napędu :SO.Reset; status :SI.TorqueDisabled, :SI.SafetyFault.',
    'kind.SS1': 'Żądanie Safe Stop 1 do napędu przez CIP Safety (kontrolowane hamowanie, potem STO).',
    'kind.SBC': 'Safe Brake Control przez CIP Safety.',
    'kind.SLS': 'Żądanie Safely-Limited Speed przez CIP Safety.',
    'kind.INFO': 'Bit informacyjny zapisywany przez SafetyTask i czytany przez sterowanie standardowe (np. interlock do innej maszyny). Nie jest wyjściem bezpiecznym.',
    # ------------------------------------------------------------------ instrukcje
    'ins.ESTOP': 'Emergency Stop (legacy) – 2 kanały; .O1 = 1 OK, 0 = wciśnięty / błąd; reset MANUAL lub AUTOMATIC.',
    'ins.RIN': 'Redundant Input (legacy) – 2 kanały (drzwi, bramki, wyłączniki).',
    'ins.LC': 'Light Curtain (legacy) – wejście Mute = 1 pomija kurtynę (muting); filtr wejściowy w ms.',
    'ins.DIN': 'Diverse Input – 2 kanały komplementarne.',
    'ins.ENPEN': 'Enable Pendant – urządzenie zezwalające.',
    'ins.THRS': 'Two-Hand Run Station – sterowanie oburęczne.', 'ins.THRSE': 'Two-Hand Run Station Enhanced.',
    'ins.DCS': 'Dual Channel Input Stop – konfigurowalna funkcja bezpieczeństwa, czas rozbieżności, restart MANUAL/AUTOMATIC.',
    'ins.DCST': 'Dual Channel Input Stop with Test.', 'ins.DCSTM': 'Dual Channel Input Stop with Test and Mute.',
    'ins.DCSTL': 'Dual Channel Input Stop with Test and Lock.', 'ins.DCSRT': 'Dual Channel Input Start.',
    'ins.DCM': 'Dual Channel Input Monitor.', 'ins.DCA': 'Dual Channel Analog Input.', 'ins.DCAF': 'Dual Channel Analog Input (zmiennoprzecinkowe).',
    'ins.SMAT': 'Safety Mat – mata bezpieczeństwa.',
    'ins.ROUT': 'Redundant Output – wyjście redundantne z monitorowaniem EDM (Feedback).',
    'ins.CROUT': 'Configurable Redundant Output – wyjście redundantne z monitorowaniem EDM i czasem reakcji sprzężenia.',
    'ins.TSAM': 'Two Sensor Asymmetrical Muting – muting dwuczujnikowy asymetryczny.', 'ins.TSSM': 'Two Sensor Symmetrical Muting – muting dwuczujnikowy symetryczny.',
    'ins.FSBM': 'Four Sensor Bidirectional Muting – muting czteroczujnikowy dwukierunkowy.',
    'ins.FPMS': 'Five Position Mode Selector – przełącznik trybów.', 'ins.EPMS': 'Eight Position Mode Selector – przełącznik trybów.',
    'ins.TON': 'Timer On Delay – opóźnione załączenie.', 'ins.TOF': 'Timer Off Delay – opóźnione wyłączenie (kategoria zatrzymania 1).',
    'ins.RTO': 'Retentive Timer On.', 'ins.TONR': 'Timer On Delay with Reset.',
    'ins.TOFR': 'Timer Off Delay with Reset – opóźnione wyłączenie (kategoria zatrzymania 1).', 'ins.RTOR': 'Retentive Timer On with Reset.',
    'ins.TONS': 'Timer safety – opóźnione załączenie.', 'ins.TOFS': 'Timer safety – opóźnione wyłączenie (kategoria zatrzymania 1).',
    'ins.OSF / OSR': 'One Shot Falling / Rising – impuls na zboczu (zwykle do generowania resetu).',
    'ins.XIC / XIO': 'Styk normalnie otwarty (sprawdza 1) / normalnie zamknięty (sprawdza 0).',
    'ins.OTE / OTL / OTU': 'Cewka / zatrzask (Latch) / odblokowanie zatrzasku (Unlatch).',
    'ins..O1': 'Wyjście instrukcji safety: 1 = stan bezpieczny / uzbrojony (OK), 0 = naruszenie / wyzwolenie.',
    'ins..FP': 'Fault Present – instrukcja w stanie błędu (np. rozbieżność kanałów, błąd EDM).',
    'ins.unknown': 'Instrukcja użyta w SafetyTask (patrz dokumentacja Rockwell).',
    # ------------------------------------------------------------------ legenda (narożnik / blok)
    'lg.title': 'LEGENDA OZNACZEŃ',
    'lg.ids': 'ID urządzeń: ',
    'lg.id_suffix': '  (TYP strefa.nr)',
    'lg.abbr_head': 'Skróty: ',
    'lg.abbr_line': 'R = rung (od 0) · M/A = reset ręczny/auto · Kat. 0 = STO / odcięcie, Kat. 1 = SS1 · · = AND, ∥ = OR · '
                    'std = sterowanie standardowe · bit std = tag SafetyTagMap (standard → safety)',
    'lg.full_note': 'Pełna legenda z kolorami: pod macierzą i w arkuszu „Legenda”.',
    'lg.read': 'Odczyt',
    'lg.codes': 'Kody w komórkach macierzy',
    'lg.ids_head': 'Oznaczenia urządzeń (ID)',
    'lg.format': 'Format',
    'lg.id_format': 'Format ID: TYP strefa.numer – np. „ES 3.1” = E-stop nr 1 w strefie 3. ID nadawane porządkowo, chyba że zdefiniowano je '
                    'w konfiguracji; obok zawsze tag Logix.',
    'lg.kinds': 'Typy wyjść',
    'lg.abbr_main': 'Najważniejsze skróty (pełna lista: arkusz „Legenda”)',
    'read.gi': 'Odczyt: wiersz = wyjście (skutek / Effect), kolumna = urządzenie (przyczyna / Cause). Komórka = co się stanie z wyjściem w wierszu, gdy zadziała urządzenie z kolumny.',
    'read.motor': 'Odczyt: wiersz = urządzenie (przyczyna / Cause), kolumna = wyjście (skutek / Effect). Najedź na kolorową komórkę – komentarz pokazuje ścieżkę przez rungi.',
    'read.valve': 'Układ jak MOTOR (wiersze = urządzenia), kolumny = wyjścia oznaczone w konfiguracji jako zawory.',
    'abbr': [
        ['Saw R22', 'Rutyna „Saw”, rung 22. Numeracja rungów od 0 – jak w Studio 5000.'],
        ['M / A', 'Reset MANUAL (wymaga przycisku / zbocza) / AUTOMATIC (samoczynny po ustąpieniu przyczyny).'],
        ['Kat. 0 / Kat. 1', 'Kategoria zatrzymania wg IEC 60204-1: 0 = natychmiastowe odcięcie energii (STO), 1 = kontrolowane hamowanie, potem odcięcie (SS1, timer opóźnionego wyłączenia).'],
        ['STO / SS1', 'Safe Torque Off / Safe Stop 1.'],
        ['EDM', 'External Device Monitoring – pętla zwrotna styków styczników / zaworów (Feedback ROUT/CROUT). Metadane – nie jest przyczyną.'],
        ['Enable Group', 'Warunek (tag strefy lub zestaw bitów .O1), który musi być spełniony, aby wyjście mogło być załączone.'],
        ['·   ∥   NOT', 'W opisie logiki: · = AND (połączenie szeregowe), ∥ = OR (gałąź równoległa), NOT = styk XIO.'],
        ['std', 'Sterowanie standardowe (programy zadań standardowych – nie-safety).'],
        ['SafetyTagMap', 'Mapowanie tagu standardowego na tag safety (std → safety). Dozwolone tylko dla resetu / diagnostyki, nie jako źródło funkcji bezpieczeństwa.'],
        ['Module:4:O.Pt00', 'Adres I/O: adapter „Module”, slot 4, wyjście („O”) punkt 00; „:I.Pt02” = wejście punkt 02; „:SO.” / „:SI.” = wyjście / wejście CIP Safety napędu.'],
        ['CRTL', 'Connection Reaction Time Limit połączenia CIP Safety = RPI × (TM + NDM) dla wejść (Rockwell 1756-RM012).'],
        ['[ALARM KRYTYCZNY]', 'Obejście / bypass / niefunkcjonalne urządzenie lub tag std podtrzymujący logikę bezpieczeństwa – wymaga korekty.'],
        ['[DO WERYFIKACJI]', 'Niejasność w kodzie lub opisie – wymaga sprawdzenia na obiekcie / schematach (Raport walidacyjny, z rutyną i rungiem).'],
        ['MARTWE', 'Urządzenie / tag / kanał, który nie wpływa na żadne wyjście bezpieczne.'],
    ],
    'colors': [
        ['Strefa / grupa wyjść', 'Nagłówek strefy (kolumna w Group Interlocks) lub grupy wyjść (kolumna w MOTOR).'],
        ['ID / tag', 'Komórka z ID urządzenia lub tagiem wyjścia; wiersz strefy w MOTOR/VALVE.'],
        ['Grupa wyjść', 'Wiersz nagłówka grupy wyjść w Group Interlocks.'],
        ['Typ urządzenia', 'Nagłówek typu urządzenia / nagłówki kolumn.'],
        ['Metadane', 'Wiersze metadanych (reset, kat. zatrzymania, EDM). Czerwony tekst = ostrzeżenie (reset A, 0 wyłączanych wyjść).'],
    ],
    'dv.err_title': 'Kod spoza legendy',
    'dv.err': 'Użyj kodu z legendy: {codes} (lub puste).',
    'dv.prompt_title': 'Kod',
    'dv.prompt': 'Wybierz kod – patrz arkusz „Legenda”.',
    # ------------------------------------------------------------------ Group Interlocks / MOTOR / VALVE
    'gi.effect': 'Wyjście (Effect) – opis',
    'gi.tag': 'Tag wyjścia',
    'gi.enable': 'Enable Group',
    'gi.reset_row': 'Reset urządzenia (M = MANUAL / A = AUTOMATIC)',
    'gi.cat_row': 'Kategoria zatrzymania',
    'gi.count_row': 'Liczba wyłączanych wyjść bezpiecznych',
    'gi.valve_head': 'ZAWORY BEZPIECZEŃSTWA (sekcja VALVE wzorca)',
    'gi.valve_none': 'Brak oznaczonych – wyjścia SafetyTask nie są zidentyfikowane jako zawory. Odbiorniki wyjść ROUT/CROUT do weryfikacji na schematach.',
    'm.type': 'Typ',
    'm.desc': 'Opis urządzenia (z programu / komentarzy I/O)',
    'm.id': 'ID / Tag Logix',
    'm.meta_head': 'METADANE WYJŚĆ (EDM / RESET – kolumny metadanych, nie są przyczynami)',
    'm.kind': 'Typ wyjścia',
    'm.addr': 'Adres / IP',
    'm.rung': 'Rung wyjścia',
    'm.enable': 'Enable Group (warunek)',
    'm.edm': 'EDM / Feedback',
    'm.reset': 'Reset wyjścia',
    'm.restart': 'Restart',
    'm.cat': 'Kategoria zatrzymania',
    'm.count': 'Liczba urządzeń wyłączających wyjście (X, X1, XB, XM, S, SB, SM) – formuła',
    'v.legend_ref': 'Legenda oznaczeń: arkusz „Legenda” (ID urządzeń TYP strefa.nr)',
    'v.none_head': 'BRAK ZIDENTYFIKOWANYCH ZAWORÓW BEZPIECZEŃSTWA W SafetyTask',
    'v.none_text': 'Żadne wyjście nie jest oznaczone jako zawór (pneumatyka / hydraulika). Jeżeli wyjścia {outs} zasilają zawory – oznacz je w konfiguracji (effects: <tag>: valve: true).',
    # ------------------------------------------------------------------ teksty metadanych
    'edm.cip': 'SI.TorqueDisabled / SI.SafetyFault (CIP Safety)',
    'rs.rout_fault': '(reset błędu ROUT)',
    'rs.none': 'brak (bez podtrzymania – podąża za logiką)',
    'rs.so_reset': '  + rung SO.Reset ({rung})',
    'restart.rout': 'AUTO – wyjście ROUT/CROUT podąża za Enable (reset urządzeń = restart)',
    'restart.rout_seal': 'RĘCZNY – rung ROUT/CROUT ma start / podtrzymanie: ponowne załączenie tylko przez {tags}',
    'restart.auto': 'AUTO – sygnał poziomowy w gałęzi podtrzymania: {tags}',
    'restart.manual': 'MANUAL – zbocze resetu + podtrzymanie',
    'restart.follow': 'podąża za logiką',
    # ------------------------------------------------------------------ arkusz Urządzenia
    'd.zone': 'Strefa', 'd.id': 'ID', 'd.type': 'Typ', 'd.tag': 'Tag Logix', 'd.desc': 'Opis', 'd.instr': 'Instrukcja',
    'd.cha': 'Kanał A', 'd.chb': 'Kanał B', 'd.routine': 'Rutyna', 'd.rung': 'Rung', 'd.reset_type': 'Reset (typ)',
    'd.reset_tag': 'Tag resetu', 'd.reset_src': 'Źródło resetu (fizyczne / logiczne)', 'd.reset_rung': 'Rung resetu',
    'd.mute': 'Muting (wejście Mute)', 'd.n_eff': 'Liczba wył. wyjść bezp.', 'd.cat': 'Kat. zatrz.', 'd.status': 'Status',
    'st.dead': 'MARTWE – brak wpływu na wyjścia bezp.', 'st.auto': 'Reset AUTO', 'st.equal': 'Kanały A = B (1-kanałowo)',
    'st.const': 'Wejścia stałe', 'st.std': 'Wejścia ze std (SafetyTagMap)', 'st.mute': 'Muting ze std',
    'st.direct': 'Wejście bezpośrednie bez instrukcji safety', 'st.external': 'Tag safety consumed', 'st.heuristic': 'Operandy wyznaczone heurystycznie – sprawdzić',
    # ------------------------------------------------------------------ arkusz Wyjścia
    'o.group': 'Grupa', 'o.tag': 'Tag', 'o.desc': 'Opis', 'o.kind': 'Typ', 'o.addr': 'Adres / IP', 'o.rung': 'Rung wyjścia',
    'o.enable': 'Enable Group', 'o.enable_rung': 'Rung Enable', 'o.logic': 'Logika Enable (z rungu; · = AND, ∥ = OR)',
    'o.edm': 'EDM / Feedback', 'o.reset': 'Reset', 'o.restart': 'Restart', 'o.cat': 'Kat. zatrzymania', 'o.crtl': 'Output CRTL [ms]',
    'o.aux_head': 'WYJŚCIA BEZPIECZNE POZA MACIERZĄ (brak urządzenia wejściowego w logice lub niezałączone w stanie gotowości) – patrz Raport walidacyjny',
    'o.reason.no_device': 'Brak urządzenia wejściowego safety w logice (np. odblokowanie rygla, lampka, żądanie) – nie jest funkcją zatrzymania.',
    'o.reason.not_energized': 'Niezałączone w stanie gotowości (wymaga żądania / sekwencji, aby się załączyć).',
    # ------------------------------------------------------------------ arkusz Ścieżki
    'p.dev': 'Urządzenie (Cause)', 'p.eff': 'Wyjście (Effect)', 'p.code': 'Kod',
    'p.path': 'Ścieżka logiczna (tag [rutyna rung]) – od instrukcji wejściowej do wyjścia',
    'p.extra': 'Bit obejścia (std) / partner OR / warunek',
    # ------------------------------------------------------------------ Raport
    'r.title': 'RAPORT WALIDACYJNY – AUDYT KODU GuardLogix (SafetyTask)',
    'r.note': 'Numeracja rungów od 0 (jak w Studio 5000). Kolejność wykonywania: {order}. Oznaczenia: arkusz „Legenda”. '
              'Raport wygenerowano automatycznie – każdą pozycję musi ocenić kompetentna osoba.',
    'r.sec_alarm': '1. WYKRYTE OBEJŚCIA / NIEFUNKCJONALNE URZĄDZENIA / AFI   [ALARM KRYTYCZNY]   ({n})',
    'r.sec_dead': '2. MARTWE WEJŚCIA / WYJŚCIA / TAGI   ({n})',
    'r.sec_verify': '3. ELEMENTY [DO WERYFIKACJI]   ({n})',
    'r.cols_alarm': [['Nr', 'Rutyna', 'Rung', 'Element', 'Opis', 'Zalecenie']],
    'r.cols_dead': [['Nr', 'Rutyna', 'Rung', 'Element', 'Opis', 'Klasyfikacja']],
    'r.cols_verify': [['Nr', 'Rutyna', 'Rung', 'Element', 'Opis', 'Działanie']],
    'r.none': 'Nie znaleziono pozycji.',
    'r.priority': 'PRIORYTET: ',
    # ------------------------------------------------------------------ ustalenia: ALARM
    'f.const_channels': 'Instrukcja {instr} {tag} ma stałe wejścia kanałów ({cha}, {chb}) – NIGDY nie zadziała, a jej wyjście jest użyte w: {uses}. '
                        'Daje fałszywe poczucie ochrony.',
    'f.const_channels.rec': 'Podłączyć fizyczne kanały do instrukcji lub usunąć urządzenie z dokumentacji bezpieczeństwa; sprawdzić okablowanie.',
    'f.std_channels': 'Kanały A/B instrukcji {instr} {tag} pochodzą z tagów STANDARDOWYCH mapowanych przez SafetyTagMap ({cha}, {chb}). Źródło: {src}. '
                      'Funkcja nie ma integralności bezpieczeństwa.',
    'f.std_channels.rec': 'Podłączyć urządzenie do modułu wejść safety lub przekazać sygnał jako Produced/Consumed Safety Tag między sterownikami safety.',
    'f.std_bypass': 'Bit standardowy {bit} jest w gałęzi równoległej z warunkiem bezpieczeństwa – przy bicie = 1 urządzenia {devices} nie wyłączają: {effects}. '
                    'Źródło bitu: {src}. Tag z SafetyTagMap bezpośrednio podtrzymuje logikę bezpieczeństwa.',
    'f.std_bypass.rec': 'Usunąć obejście ze sterowania standardowego; jeśli warunek jest potrzebny – zbudować go z wejść / instrukcji safety (np. muting TSAM/TSSM/FSBM).',
    'f.std_mute': 'Muting {tag} ({instr}, operand {operand}) jest sterowany bitem / bitami standardowymi {bits}. Źródło: {src}.',
    'f.std_mute.rec': 'Realizować muting wyłącznie instrukcjami TSAM/TSSM/FSBM z czujnikami mutingu na wejściach safety; nie wyciszać ze sterowania std.',
    'f.mute_const': 'Wejście Mute {tag} jest stałą 1 – kurtyna jest trwale wyciszona.',
    'f.mute_const.rec': 'Podłączyć wejście Mute do bezpiecznej funkcji mutingu lub ustawić 0.',
    'f.std_parallel': 'Sam bit standardowy {bit} może ustawić {tag}, którego logika w przeciwnym razie wymaga warunków z wejść safety: {expr}. Źródło: {src}.',
    'f.std_parallel.rec': 'Usunąć gałąź standardową lub zastąpić ją sygnałem safety (np. bezpieczne monitorowanie postoju przez CIP Safety).',
    'f.estop_auto': 'Wyłącznik(i) awaryjny(e) {tags} mają reset AUTOMATIC – po zwolnieniu grzybka O1 = 1 i wyjścia {effects} mogą się ponownie załączyć bez resetu ręcznego '
                    '(ISO 13850: reset E-stop musi być świadomym działaniem ręcznym i nie może inicjować ponownego uruchomienia).',
    'f.estop_auto.rec': 'Zmienić Reset Type na MANUAL z przyciskiem resetu poza strefą zagrożenia; sprawdzić, czy żadne wyjście nie startuje samoczynnie.',
    'f.equal_channels': 'Oba kanały instrukcji {instr} {tag} wskazują to samo wejście {ch} – brak redundancji i wykrywania rozbieżności; funkcja de facto '
                        '1-kanałowa (dotyczy {n} wyjść bezpiecznych).',
    'f.equal_channels.rec': 'Podłączyć kanał B do osobnego wejścia i poprawić operand; zweryfikować okablowanie czujnika.',
    'f.afi': 'Instrukcja AFI (Always False) w {rung} – rung trwale wyłączony; na stałe wyłącza: {outputs}.',
    'f.afi.rec': 'Usunąć AFI lub udokumentować powód wyłączenia rungu; sprawdzić, czy żadna funkcja bezpieczeństwa od niego nie zależy.',
    'f.const_branch': 'Gałąź złożona wyłącznie ze stałych styków ({consts}) jest zawsze prawdziwa i mostkuje logikę '
                      '{tag}. Zmostkowane urządzenia: {devices}.',
    'f.const_branch.rec': 'Usunąć mostkującą gałąź lub zastąpić stałą rzeczywistym warunkiem bezpieczeństwa.',
    'f.reset_std_auto': 'Bit resetu {bit} jest generowany automatycznie (zatrzaskiwany w sekwencji standardowej lub zapisywany przez sam SafetyTask) i resetuje: {resets}. '
                        'Źródło: {src}. Reset bez świadomego działania operatora.',
    'f.reset_std_auto.rec': 'Resetować wyłącznie przyciskiem (zbocze) poza strefą zagrożenia; usunąć automatyczne źródła resetu ze sterowania standardowego.',
    # ------------------------------------------------------------------ ustalenia: MARTWE
    'f.dead_device': 'Wyjście {tag} nie wyłącza żadnego wyjścia bezpiecznego; użyte tylko w: {uses}.',
    'f.dead_muting': 'Wyjście .O1 instrukcji mutingu {tag} nie jest użyte w żadnym rungu.',
    'f.const_tags': 'Tagi nigdy niezapisywane w SafetyTask (stałe wartości początkowe), a czytane w logice: {tags}.',
    'f.unused_tags': 'Tagi safety zdefiniowane, ale nieużywane w wykonywanej logice SafetyTask: {tags}.',
    'f.unused_inputs': 'Wejścia safety modułu {module} nieużywane w SafetyTask: {channels}.',
    'f.unused_outputs': 'Wyjścia safety modułu {module} nieużywane w SafetyTask: {channels}.',
    'f.unused_module': 'Moduł wejść safety {module} – żadne z jego wejść nie jest użyte w SafetyTask.',
    'f.uncalled_routine': 'Rutyna {routine} ({n} rungów) nie jest wywoływana (brak JSR) – jej logika się nie wykonuje.',
    'f.drive_unused': 'Napęd {module} ma połączenie CIP Safety, ale brak odwołań w SafetyTask.',
    'f.module_unused': 'Moduł {module} ma połączenie safety, ale brak odwołań w SafetyTask.',
    'f.drives_hardwired': 'Napędy bez połączenia CIP Safety (ewentualne STO sprzętowe jest poza kodem): {modules}.',
    'cls.dead_input': 'Martwe wejście (dla wyjść bezp.)', 'cls.dead_block': 'Martwy blok', 'cls.const_tag': 'Tagi stałe',
    'cls.dead_tags': 'Martwe tagi', 'cls.dead_channel': 'Martwe kanały', 'cls.dead_routine': 'Martwa rutyna',
    'cls.outside_code': 'Poza kodem', 'cls.dead': 'Martwe',
    # ------------------------------------------------------------------ ustalenia: DO WERYFIKACJI
    'f.aux_no_device': 'Wyjście bezpieczne {tag} nie jest wyłączane przez żadne urządzenie wejściowe safety (logika: {expr}) – np. odblokowanie rygla lub lampka. '
                       'Sprawdzić funkcję i jej warunki.',
    'f.aux_not_energized': 'Wyjście bezpieczne {tag} nie jest załączone w stanie gotowości (logika: {expr}) – pominięte w macierzy; sprawdzić funkcję.',
    'f.crtl_inputs': 'Wejścia safety {adapter}: RPI {rpi} ms, Timeout Multiplier {tm}, Network Delay Multiplier '
                     '{ndm} % → Input CRTL {crtl} ms. Najgorszy czas reakcji samej logiki (Input CRTL + filtr LC + '
                     'okres zadania {period} ms + watchdog {watchdog} ms + Output CRTL) do {total} ms – bez czasu '
                     'czujnika i zatrzymania. Urządzenia: {devices}. Zweryfikować z oceną ryzyka i odległościami '
                     'bezpieczeństwa (ISO 13855); szczegóły: arkusz „Funkcje PL”. Uwzględnione opóźnienie z '
                     'kolejności wykonania: {lags} × okres zadania.',
    'f.crtl_outputs': 'Moduły wyjść safety {modules}: RPI {rpi} ms, TM {tm}, NDM {ndm} % → Output CRTL {crtl} ms.',
    'f.crtl_drives': 'Połączenia wyjściowe CIP Safety napędów: RPI {rpi} ms, TM {tm}, NDM {ndm} % → CRTL {crtl} ms dla: {modules}.',
    'f.osf_ote': 'OSF/OSR i OTE na tym samym tagu {tag} w jednym rungu – OTE nadpisuje impuls zbocza poziomem (reset poziomem zamiast zboczem).',
    'f.double_ote': 'Tag {tag} jest zapisywany przez {n} cewki OTE – wartość określa tylko ostatnia w cyklu.',
    'f.rout_reset_fp': 'Reset błędu {reset} instrukcji {tag} jest warunkowany przez {other} (błąd INNEJ instrukcji wyjściowej) – prawdopodobny błąd kopiowania.',
    'f.or_devices': 'Urządzenia {a} i {b} są połączone równolegle (OR) – wyzwolenie jednego z nich nie wyłącza {effects} (kod XC). Potwierdzić z oceną ryzyka.',
    'f.auto_restart': 'Gałąź podtrzymania {tag} zawiera sygnał poziomowy ({levels}) – wyjście wraca samoczynnie, gdy sygnał powróci (brak niezależnego resetu).',
    'f.auto_reset_guard': 'Urządzenie osłony {tag} ma reset AUTOMATIC – po zamknięciu wyjścia {effects} mogą wystartować bez resetu. Potwierdzić, że restart '
                          'nie jest możliwy, gdy osoba przebywa w strefie zagrożenia (ISO 13849-1 §5.2.2, ISO 14119).',
    'f.reset_std': 'Reset ze sterowania standardowego: bit {bit} resetuje {resets}. Źródło: {src}. Sprawdzić lokalizację i widoczność przycisku resetu '
                   '(reset ręczny poza strefą zagrożenia, ISO 13849-1 §5.2.2).',
    'f.std_not_written': 'Bit mapowany ze std {bit} jest czytany w SafetyTask, ale w kodzie standardowym nie '
                         'znaleziono zapisu do {src}. Mógłby go ustawić tylko panel HMI/SCADA, instrukcja MSG lub '
                         'zmiana online.',
    'f.missing_comments': 'Brak komentarzy kanałów I/O w {module} ({channels}) – przypisanie {who} wyłącznie na podstawie nazw tagów.',
    'f.free_cmp': 'Porównanie {leaf} w logice {effects} – przyjęto {value} w stanie gotowości; wynik zależy od danych.',
    'f.free_data': 'Bit zależny od danych {leaf} (zapisywany instrukcją danych) w logice {effects} – przyjęto {value} w stanie gotowości.',
    'f.free_latch': 'Bit zatrzaskowy {leaf} (OTL/OTU) w logice {effects} – przyjęto {value} w stanie gotowości; sprawdzić warunki zatrzaśnięcia / zwolnienia.',
    'f.free_unk': 'Bit {leaf} o nieznanej wartości w logice {effects} – przyjęto {value}.',
    'f.free_mute': 'Muting {leaf} wpływa na {effects} – przy aktywnym mutingu kurtyna nie wyłącza (kod XM).',
    'f.free_ext': 'Tag safety consumed {leaf} w logice {effects} – sprawdzić sterownik produkujący.',
    'f.direct_direct': 'Wejście safety {tag} jest użyte bezpośrednio w logice {effects} bez instrukcji wejściowej safety (brak monitorowania rozbieżności).',
    'f.direct_external': 'Tag safety consumed {tag} wyłącza {effects} – funkcja jest realizowana w innym sterowniku.',
    'f.heuristic': 'Operandy {instr} {tag} przypisano heurystycznie ({roles}) – potwierdzić kanały i reset w Studio 5000.',
    'f.device_conditional': 'Instrukcja wejściowa safety {tag} jest w rungu warunkowym – przy fałszywym warunku wyjście .O1 jest kasowane.',
    'f.routine_not_analysed': 'Rutyny {routine} ({kind}) nie można przeanalizować (chroniona lub nie-drabinkowa) – jej logika nie jest odzwierciedlona w macierzy.',
    'f.aoi_conditional': 'Add-On Instruction {aoi} jest wywoływana w rungu warunkowym – analiza przyjmuje EnableIn = 1.',
    'f.flow': 'Instrukcja sterowania przebiegiem {instr} w SafetyTask – macierz zakłada ciągłe wykonywanie każdego rungu.',
    'f.unknown_instr': 'Instrukcja {instr} nie jest znana analizatorowi – potraktowano ją jako przezroczystą; sprawdzić jej działanie ręcznie.',
    'f.aoi_protected': 'Add-On Instruction {aoi} ({inst}) jest chroniona (source protection) – jej wyjścia potraktowano jako nieznane.',
    'f.jsr_conditional': 'Rutyna {routine} jest wywoływana warunkowo – wyjścia w niej zachowują stan, gdy nie jest wykonywana.',
    'f.pair_mismatch': 'Wyjścia {a} i {b} instrukcji {tag} mają w logice różne przyczyny – sprawdzić okablowanie obu kanałów.',
    'f.loads': 'Kod nie definiuje, co jest zasilane z wyjść {outputs} (styczniki / sprzętowe STO / zawory) – potwierdzić na schematach elektrycznych.',
    'f.stop_cat0': 'Żaden timer opóźnionego wyłączenia nie leży na ścieżce urządzenie safety → wyjście, więc wszystkie '
                   'funkcje bezpieczeństwa realizują zatrzymanie kategorii 0 (STO / odpadnięcie stycznika). Dla '
                   'maszyn o dużej bezwładności rozważyć SS1 zgodnie z oceną ryzyka.',
    'f.stop_cat1': 'Timery opóźnionego wyłączenia na ścieżkach urządzenie safety → wyjście: {timers} – wyjścia '
                   '{effects} zatrzymują się w kategorii 1 (SS1); sprawdzić opóźnienie względem czasu zatrzymania.',
    'f.forces': 'Stan Force nie jest zapisywany w eksporcie – sprawdzić zakładkę Forces dla tagów safety online w Studio 5000.',
    'f.completeness': 'Analizowany plik {src}; wykonywane rutyny i liczby rungów: {routines}. Potwierdzić liczby rungów w Studio 5000.',
    'f.afi_noop': 'AFI (Always False) w {rung} na rungu bez instrukcji wyjściowych (np. tylko NOP) – obecnie bez '
                  'wpływu na logikę, ale to wyłączony rung w zadaniu bezpieczeństwa.',
    'f.afi_noop.rec': 'Usunąć rung lub udokumentować jego cel; upewnić się, że nie miała tu być funkcja '
                      'bezpieczeństwa.',
    'f.map_written': 'Tag safety {tag} jest celem SafetyTagMap (ze standardowego {src}) i jednocześnie jest '
                     'zapisywany przez logikę safety w {writers}. Wartość ze sterowania standardowego jest kopiowana '
                     'na początku każdego cyklu zadania bezpieczeństwa, a potem nadpisywana – mapowanie nic nie daje '
                     'i wprowadza w błąd.',
    'f.map_written.rec': 'Usunąć mapowanie lub użyć osobnego tagu safety dla wyniku logiki; udokumentować, które '
                         'źródło jest zamierzone.',
    'f.map_read_before_write': 'Tag safety {tag} jest mapowany ze standardowego {src} (SafetyTagMap) i zapisywany '
                               'przez logikę safety w {writers}, ale jest czytany wcześniej w cyklu w {readers} – '
                               'tam jego wartość pochodzi ze sterowania STANDARDOWEGO.',
    'f.map_read_before_write.rec': 'Usunąć mapowanie lub przenieść zapis safety przed każdy odczyt; wartość ze '
                                   'sterowania standardowego nie może wpływać na funkcję bezpieczeństwa.',
    'f.aux_always_on': 'Wyjście bezpieczne {tag} jest załączone bezwarunkowo (logika: {expr}) – żadne urządzenie '
                       'safety go nie wyłącza (np. zasilanie czujnika lub źródło testowe).',
    'f.aux_always_on.rec': 'Potwierdzić na schematach, co jest zasilane z tego wyjścia; nie może być do niego '
                           'podłączony niebezpieczny odbiornik.',
    'f.aux_inverse': 'Wyjście bezpieczne {tag} załącza się dopiero po wyzwoleniu {devices} (logika: {expr}) – '
                     'lampka, zwolnienie rygla itp., nie wyjście funkcji bezpieczeństwa; nie jest pokazane w '
                     'macierzy.',
    'f.aux_inverse.rec': 'Sprawdzić funkcję; jeśli zwalnia rygiel osłony, zweryfikować warunki (postój, opóźnienie).',
    'f.channel_copy': 'Kanały tych instrukcji to tagi pośrednie kopiowane z wejść fizycznych (XIC(wejście) '
                      'OTE(kopia)): {devices}. Kopie są zapisywane przed instrukcją w cyklu; macierz, CRTL i '
                      'komentarze I/O używają wejść fizycznych.',
    'f.channel_copy.rec': 'Rungi kopiujące nie mogą mieć dodatkowych warunków; czytelniej jest użyć wejść fizycznych '
                          'bezpośrednio w instrukcji.',
    'f.channel_copy_late': 'Kanały tych instrukcji to tagi pośrednie kopiowane z wejść fizycznych, a rungi kopiujące '
                           'wykonują się PO instrukcji w cyklu: {devices}. Instrukcja ocenia stan wejść z '
                           'poprzedniego cyklu – czas reakcji rośnie o jeden okres SafetyTask ({period} ms).',
    'f.channel_copy_late.rec': 'Przenieść rungi kopiujące przed instrukcje (kolejność JSR w MainRoutine) lub użyć '
                               'wejść fizycznych bezpośrednio; uwzględnić dodatkowy okres w czasie reakcji.',
    'f.channel_logic': 'Kanał {ch} instrukcji {instr} {tag} nie jest wejściem fizycznym, lecz tagiem wyliczanym '
                       'przez logikę: {expr}. Redundancja i kontrola rozbieżności instrukcji dotyczą wtedy tej '
                       'logiki, a nie czujnika.',
    'f.channel_logic.rec': 'Podłączyć kanały fizyczne bezpośrednio do instrukcji lub uzasadnić logikę w koncepcji '
                           'bezpieczeństwa.',
    'f.scan_lag': 'Tag {tag} jest zapisywany w {writer}, ale czytany wcześniej w cyklu w {readers} – te rungi '
                  'używają wartości z poprzedniego cyklu: +1 okres SafetyTask ({period} ms) w czasie reakcji dla: '
                  '{effects}.',
    'f.scan_lag.rec': 'Zmienić kolejność rutyn / rungów tak, aby tag był zapisywany przed odczytem, lub uwzględnić '
                      'dodatkowy okres w czasie reakcji.',
    'f.edm_same_channel': 'Oba wejścia sprzężenia zwrotnego {instr} {tag} używają tego samego kanału {ch} – styki '
                          'pomocnicze obu styczników są połączone szeregowo do jednego wejścia; uszkodzenie tego '
                          'jednego wejścia lub przewodu nie jest wykrywane przez EDM.',
    'f.edm_same_channel.rec': 'Sprawdzić, czy spełnia to wymaganą kategorię / PL; w przeciwnym razie podłączyć każde '
                              'sprzężenie do osobnego wejścia.',
    'f.rout_extra_logic': 'Wyjścia {outputs} instrukcji {instr} {tag} są wyłączane także przez {devices}, które nie '
                          'działają przez zezwolenie {instr}. Gdy zadziała tylko któreś z nich, wyjścia gasną, a '
                          '{tag}.O1 pozostaje załączone – sprzężenie zwrotne przestaje się zgadzać, {tag} zgłasza '
                          'błąd sprzężenia (wymagany reset), a EDM nie nadzoruje tej ścieżki wyłączenia.',
    'f.rout_extra_logic.rec': 'Włączyć te warunki do zezwolenia {tag}, aby każda ścieżka wyłączenia przechodziła '
                              'przez nadzorowaną instrukcję.',
    'f.timer_other': 'Timer opóźnionego wyłączenia {tag} ({instr}, preset {preset} ms) nie leży na ścieżce '
                     'urządzenie safety → wyjście: opóźnia warunek {cond}; używany przez: {users}. To nie jest '
                     'kategoria zatrzymania 1 funkcji bezpieczeństwa (np. opóźnienie rygla lub zwolnienia).',
    'f.timer_other.rec': 'Jeśli zwalnia rygiel osłony, zweryfikować opóźnienie względem czasu wybiegu maszyny.',
    # ------------------------------------------------------------------ arkusz Legenda
    'l.title': 'LEGENDA OZNACZEŃ I METODA',
    'l.s1': '1. KODY W KOMÓRKACH MACIERZY', 'l.s2': '2. ODCZYT MACIERZY', 'l.s3': '3. OZNACZENIA URZĄDZEŃ (ID)', 'l.s4': '4. STREFY',
    'l.s5': '5. TYPY WYJŚĆ (SKUTKI)', 'l.s6': '6. UŻYTE INSTRUKCJE SAFETY', 'l.s7': '7. SKRÓTY I OZNACZENIA W METADANYCH / RAPORCIE',
    'l.s8': '8. KOLORY NAGŁÓWKÓW I WIERSZY', 'l.s9': '9. METODA I UWAGI', 'l.s10': '10. ARKUSZE SKOROSZYTU',
    'l.s11': '11. POLA DO UZUPEŁNIENIA I WYNIKI TESTÓW', 'l.s12': '12. HISTORIA REWIZJI', 'l.s13': '13. ŹRÓDŁA',
    'l.cols_codes': [['Kod', 'Znaczenie (skrót)', 'Opis pełny', 'Liczba – MOTOR', 'Liczba – Group Interl.']],
    'l.sheet': 'Arkusz', 'l.axes': 'Układ osi', 'l.id_abbr': 'Skrót ID', 'l.type_hdr': 'Typ (nagłówek kolumny)', 'l.meaning': 'Znaczenie',
    'l.instr': 'Instrukcja', 'l.count': 'Liczba', 'l.zone_no': 'Nr strefy', 'l.id_prefix': 'Prefiks ID', 'l.zone_name': 'Nazwa strefy',
    'l.kind': 'Typ', 'l.mark': 'Oznaczenie', 'l.sample': 'Próbka', 'l.element': 'Element', 'l.contents': 'Zawartość',
    'l.yellow': '(żółte)', 'l.dropdown': 'Lista rozwijana',
    'l.dropdown_txt': 'Komórki macierzy (Group Interlocks, MOTOR) mają listę kodów i formatowanie warunkowe – ręczna zmiana kodu automatycznie nadaje '
                      'kolor z legendy. Uwaga: komentarz ze ścieżką rungów opisuje stan wygenerowany z programu.',
    'l.rev': 'Rewizja', 'l.date': 'Data', 'l.changes': 'Opis zmian', 'l.author': 'Autor', 'l.no': 'Nr', 'l.doc': 'Dokument',
    'l.rev_auto': 'Wygenerowano automatycznie programem safety-matrix-generator {version}.',
    'l.n.method': 'Metoda: każde skrzyżowanie wyznaczono deterministycznie z logiki drabinkowej SafetyTask (symulacja boolowska każdego rungu w kolejności '
                  'skanowania): urządzenie wyzwolone (O1 = 0), pozostałe zdrowe, bity standardowe = 0 → X; jeśli ustawienie bitu std przywraca wyjście → XB; '
                  'jeśli przywraca je warunek wewnętrzny → XM; jeśli wyjście gaśnie tylko przy wyzwoleniu drugiego urządzenia → XC. '
                  'Żadne powiązanie nie wynika z podobieństwa nazw tagów.',
    'l.n.cat0': 'Kategoria zatrzymania: w SafetyTask brak timerów opóźnionego wyłączenia – wszystkie funkcje realizują zatrzymanie kategorii 0 (STO przez CIP Safety lub odcięcie stycznika przez ROUT).',
    'l.n.cat1': 'Kategoria zatrzymania: ścieżki przez timery opóźnionego wyłączenia (TOF/TOFR/TOFS) to kategoria 1 z nastawą timera podaną w komentarzu komórki i w metadanych.',
    'l.n.edm': 'EDM / Feedback oraz przyciski Reset są ujęte wyłącznie w metadanych (MOTOR – wiersze pod macierzą, arkusze „Urządzenia” i „Wyjścia”), nie jako przyczyny.',
    'l.n.rout': 'Wyjścia ROUT/CROUT mają po dwa kanały (np. Pt00/Pt01) – w macierzy jedna kolumna na instrukcję wyjściową (sprawdzono, że oba kanały mają identyczne przyczyny).',
    'l.n.comment': 'Komentarze w komórkach arkusza MOTOR zawierają ścieżkę tag [rutyna R rung] od instrukcji wejściowej do wyjścia.',
    'l.n.ids': 'ID urządzeń (TYP strefa.nr) nadawane są porządkowo, chyba że zdefiniowano je w konfiguracji; obok zawsze tag Logix.',
    'l.n.tool': 'Wygenerowano programem safety-matrix-generator {version} (autor: Robert Pietroń). Wynik nie zastępuje walidacji wg ISO 13849-2 / IEC 62061.',
    'input_note': 'Pola żółte – do uzupełnienia (dane z kart katalogowych, oceny ryzyka, SISTEMA lub wyniki testów). Pozostałe pola wygenerowano z programu.',
    'result.OK': 'Test zgodny z oczekiwanym wynikiem.',
    'result.NOK': 'Test niezgodny – opisać w kolumnie uwag, zgłosić do korekty.',
    'result.N/A': 'Nie dotyczy / test niewykonalny (podać powód).',
    # ------------------------------------------------------------------ Funkcje bezpieczeństwa
    'sf.title': 'FUNKCJE BEZPIECZEŃSTWA – CZAS REAKCJI I POZIOM PL',
    'sf.method': 'Czas reakcji (najgorszy przypadek) = opóźnienie czujnika + Input CRTL + filtr LC + (okres Safety Task + watchdog) + Output CRTL + opóźnienie '
                 'wyjścia / aktuatora. Input CRTL = RPI × (TM + NDM); Output CRTL = okres Safety Task × (TM + NDM − 1) – Rockwell 1756-RM012. Wartości CRTL '
                 'odczytane z eksportu (ReactionTimeLimit); Safety Task: okres {period} ms, watchdog {watchdog} ms. Czas zatrzymania maszyny (ISO 13855) = '
                 'czas reakcji + czas hamowania / wybiegu – do pomiaru.',
    'sf.input_hint': 'Przykładowe źródła: czas reakcji kurtyny / skanera, czas zadziałania stycznika – karta katalogowa; PLr – ocena ryzyka (ISO 13849-1, zał. A); PL/PFHd – SISTEMA.',
    'sf.cols': [['SF', 'ID', 'Tag urządzenia', 'Funkcja bezpieczeństwa', 'Wyłączane wyjścia (X / X1 / XB / XM)', 'Kat. zatrz.', 'Struktura wejścia (z kodu)',
                 'Moduł wejściowy (RPI / TM / NDM)', 'Input CRTL [ms]', 'Filtr LC [ms]', 'Okres Safety Task + watchdog [ms]', 'Output CRTL max [ms]',
                 'Opóźnienie czujnika [ms]', 'Opóźnienie wyjścia / aktuatora [ms]', 'Czas reakcji – suma [ms]', 'PLr (ocena ryzyka)', 'Kategoria (B, 1–4)',
                 'PL osiągnięty / PFHd', 'Uwagi']],
    'sf.s.const': 'Wejścia stałe – brak funkcji [ALARM]',
    'sf.s.direct': 'Bezpośrednie wejście safety bez instrukcji (1 kanał) [ALARM]',
    'sf.s.external': 'Tag safety consumed (funkcja w innym sterowniku)',
    'sf.s.single': '1-kanałowa (kanał A = B) – {instr} [ALARM]',
    'sf.s.std': 'Kanały ze sterowania std (SafetyTagMap) – {instr} [ALARM]',
    'sf.s.two': '2-kanałowa – {instr}',
    'sf.s.mute': '; muting ze std [ALARM]',
    'sf.s.xb': '; obejście std (XB)',
    'sf.s.xc': '; gałąź OR (XC)',
    'sf.s.xm': '; warunek wewnętrzny (XM)',
    'sf.n.xc': 'Wyłącza {effs} tylko łącznie z {partners} (gałąź OR).',
    'sf.n.none': 'Brak wpływu na wyjścia bezpieczne – funkcja niezrealizowana w SafetyTask.',
    'sf.n.nonfunc': 'Urządzenie niefunkcjonalne (stałe wejścia) – funkcja nie działa.',
    'sf.n.crtl': 'Input CRTL ≥ {ms} ms – patrz Raport walidacyjny (PRIORYTET).',
    'sf.n.std': 'Sygnał ze sterowania standardowego – czas reakcji nieokreślony.',
    'sf.n.delay': 'Opóźnione wyłączenie w ścieżce: {ms} ms (kategoria 1) – doliczyć do czasu reakcji.',
    'sf.n.lag': 'Kolejność wykonania dodaje {n} okres(y) SafetyTask ({ms} ms) – uwzględnione w kolumnie zadania.',
    'sf.only_xc': 'tylko z partnerem (XC): {effs}',
    'sf.cf_note': 'Czerwone tło sumy: > 1000 ms; żółte: 500–1000 ms (formatowanie warunkowe). Suma liczy się automatycznie po wpisaniu opóźnień urządzeń.',
    # ------------------------------------------------------------------ Protokół testów
    't.title': 'PROTOKÓŁ TESTÓW WALIDACYJNYCH FUNKCJI BEZPIECZEŃSTWA (ISO 13849-2)',
    't.pre': 'Warunki wstępne: wszystkie urządzenia zresetowane, wyjścia bezpieczne załączone (stan gotowości), brak osób w strefach zagrożenia, test wykonywany '
             'bez materiału / w trybie testowym. Oczekiwane wyniki wygenerowano z kodu SafetyTask (macierz MOTOR) – rozbieżność rzeczywistości z oczekiwaniem = NOK.',
    't.result_hint': 'Wynik: OK / NOK / N/A (lista). ',
    't.cols': [['Nr', 'Typ testu', 'ID / Tag', 'Opis urządzenia / elementu', 'Akcja testowa', 'Oczekiwany wynik (wg kodu SafetyTask)',
                'Reset / restart – oczekiwane zachowanie', 'Odniesienie (rutyna / rung)', 'Uwagi / alarm', 'Wynik', 'Data', 'Wykonał', 'Uwagi z testu']],
    't.k.func': 'Funkcja', 't.k.or': 'Kombinacja OR', 't.k.byp': 'Obejście std (dokumentacyjny)', 't.k.edm': 'EDM', 't.k.comm': 'Utrata komunikacji',
    't.act.xb': 'Bit(y) obejścia {bits} muszą być nieaktywne.',
    't.act.mute': 'Muting nieaktywny.',
    't.act.disc': '2) Test rozbieżności: przy urządzeniu w stanie OK rozewrzyj tylko kanał A ({a}), potem tylko kanał B ({b}).',
    't.exp.n': 'BRAK zadziałania – instrukcja ma w kodzie stałe wejścia ({rung}); wyjścia pozostają załączone. [ALARM KRYTYCZNY]',
    't.exp.nconst': 'BRAK wyłączenia dla {outs} – urządzenie jest zmostkowane stałym stykiem {bits}; te wyjścia '
                    'pozostają załączone. [ALARM KRYTYCZNY]',
    't.exp.off': '1) Wyłączone: {outs}',
    't.exp.sto': ' (napędy: :SI.TorqueDisabled = 1)',
    't.exp.rest': '. Pozostałe wyjścia bez zmian.',
    't.exp.notoff': 'NIE wyłączą się: {effs} (gałąź OR z {partners} – patrz test OR).',
    't.exp.disc': '2) {instr}.FP = 1 (błąd rozbieżności), O1 = 0 – wyłączenia jak w 1); reset możliwy dopiero po przywróceniu obu kanałów.',
    't.exp.disc_short': '2) {instr}.FP = 1 (błąd rozbieżności), O1 = 0.',
    't.exp.single': '2) Test rozbieżności NIEWYKONALNY – oba kanały instrukcji na tym samym wejściu. [ALARM KRYTYCZNY]',
    't.exp.xc_only': 'Pojedyncze wyzwolenie NIE wyłącza żadnego wyjścia bezpiecznego; {effs} wyłączy się tylko łącznie z {partners} (gałąź OR) – patrz test kombinacji OR.',
    't.exp.none': 'Brak wpływu na wyjścia bezpieczne (urządzenie nie steruje żadnym wyjściem w SafetyTask) – potwierdzić zamierzenie projektowe.',
    't.rst.manual': 'Urządzenie: reset MANUAL ({tag} [{rr}] ← {src}); bez resetu O1 = 0.',
    't.rst.auto': 'Urządzenie: reset AUTOMATIC – O1 wraca samo po ustąpieniu przyczyny',
    't.rst.auto_estop': ' [ALARM: E-stop]',
    't.rst.follow': 'Urządzenie: reset zgodnie z konfiguracją instrukcji.',
    't.rs.rout': 'Wyjścia ROUT/CROUT ({outs}): załączą się same po resecie urządzenia (wyjście podąża za Enable).',
    't.rs.auto': 'Wyjścia {outs}: wracają AUTOMATYCZNIE z {tags} [DO WERYFIKACJI].',
    't.rs.manual': 'Wyjścia ({n}: {outs}): wymagany reset {resets}.',
    't.rs.follow': 'Wyjścia {outs}: podążają za logiką.',
    't.rs.where': 'Źródła resetów wyjść: arkusz „Wyjścia”.',
    't.note.xb': 'Obejście ze std: {bits} – patrz test OBEJŚCIE.',
    't.note.auto': 'Reset AUTO.',
    't.note.std': 'Kanały z danych standardowych – test rozbieżności po stronie sterownika źródłowego.',
    't.or.act': '1) Wyzwól tylko {a}. 2) Wyzwól tylko {b}. 3) Wyzwól oba jednocześnie.',
    't.or.exp': '1), 2) {outs} pozostają ZAŁĄCZONE. 3) Wyłączone: {outs}.',
    't.or.rst': 'Jak w testach funkcji obu urządzeń.',
    't.or.note': 'Gałąź równoległa OR – potwierdzić z oceną ryzyka [DO WERYFIKACJI].',
    't.byp.act': 'Test kontrolowany, bez osób w strefie: ustaw warunek aktywujący bit {bit} ({src}), następnie wyzwól urządzenie.',
    't.byp.exp': 'Wg kodu: {outs} pozostają ZAŁĄCZONE – funkcja zmostkowana przez sterowanie standardowe. Po korekcie programu oczekiwane: wyłączenie jak w teście funkcji.',
    't.byp.note': '[ALARM KRYTYCZNY] – patrz Raport walidacyjny.',
    't.edm.act_neg': 'Przy wyłączonym wyjściu (strefa zatrzymana) rozewrzyj obwód sprzężenia zwrotnego {fb} (symulacja sklejonego stycznika – brak styku NC), następnie zresetuj urządzenia i spróbuj załączyć.',
    't.edm.act_pos': 'Przy wyłączonym wyjściu zmostkuj sprzężenie zwrotne {fb} (feedback = 1 przy wyłączonym wyjściu – symulacja sklejonego stycznika), następnie zresetuj urządzenia i spróbuj załączyć.',
    't.edm.exp': '{tag}.FP = 1 (błąd EDM); wyjścia {outs} NIE załączają się.',
    't.edm.rst': 'Po usunięciu przyczyny: reset błędu {reset} [{rr}] ← {src}.',
    't.comm.what': 'Adapter {name} ({cat}, {addr}) – moduły Safety I/O',
    't.comm.act': 'Odłącz kabel Ethernet adaptera {name} przy pracującej linii.',
    't.comm.exp': 'Wejścia safety adaptera = 0 (status połączenia = błąd) → wyzwolone: {ids}. Wyłączone: {outs}.',
    't.comm.rst': 'Po przywróceniu połączenia: wyjścia pozostają wyłączone do resetu urządzeń wg testów funkcji.',
    't.comm.ref': 'Konfiguracja I/O',
    't.comm.note': 'Wykrycie najpóźniej po Input CRTL modułów ({crtl}).',
    't.drv.id': 'Napędy CIP Safety',
    't.drv.what': '{n} napęd(ów) z CIP Safety',
    't.drv.act': 'Dla każdego napędu: odłącz jego połączenie sieciowe podczas pracy.',
    't.drv.exp': 'Napęd przechodzi w STO (utrata połączenia CIP Safety); :SI.ConnectionFaulted = 1 blokuje rung :SO.SafeTorqueOff tam, gdzie jest użyty.',
    't.drv.rst': 'Po przywróceniu: STO pozostaje aktywne do resetu (zbocze resetu + :SO.Reset).',
    't.drv.ref': 'Rungi STO ({routines})',
    't.summary': 'Podsumowanie',
    't.sum.count': 'Liczba testów',
    't.sum.open': 'Niewykonane',
    't.approve': 'Zatwierdzenie protokołu (imię, nazwisko, data, podpis):',
    't.done_by': 'Wykonał', 't.checked_by': 'Sprawdził', 't.approved_by': 'Zatwierdził',
    # ------------------------------------------------------------------ arkusz Start
    's.subtitle': 'Macierz przyczynowo-skutkowa (Cause & Effect) – GuardLogix {proc} {ver}, SafetyTask {period} ms, program {src}',
    's.author': 'Autor: {author}   •   Rewizja: {rev}   •   Data: {date}',
    's.lang_label': 'Język',
    's.switch_hint': '◄ wybierz język z listy – wszystkie arkusze przełączą się automatycznie',
    's.dict_note': 'Teksty pobierane są z arkusza „{dict}” (tam można poprawiać tłumaczenia; puste tłumaczenie = tekst angielski). '
                   'Kody w macierzy (X, X1, XB, XC, XM, N, S…) i tagi programu są wspólne dla wszystkich języków.',
    's.sheet': 'Arkusz', 's.contents': 'Zawartość', 's.summary': 'Podsumowanie', 's.value': 'Wartość',
    's.sum.devices': 'Urządzenia wejściowe (przyczyny)',
    's.sum.effects': 'Wyjścia bezpieczne (skutki) + sygnały informacyjne',
    's.sum.cells': 'Skrzyżowania X / X1 / XB / XC / XM / N w macierzy MOTOR',
    's.sum.alarm': '[ALARM KRYTYCZNY] – pozycje w raporcie',
    's.sum.dead': 'Martwe elementy – pozycje w raporcie',
    's.sum.verify': '[DO WERYFIKACJI] – pozycje w raporcie',
    's.sum.tests': 'Testy w protokole walidacji',
}
