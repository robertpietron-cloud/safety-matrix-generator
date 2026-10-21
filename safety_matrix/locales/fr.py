# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/locales/fr.py
# Author  : Robert Pietroń
# Revision: 1.1.0 (2026-10-21)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: textes français (mêmes clés
#                        que le catalogue anglais).
#   1.1.0 (2026-10-21) - Texts of the new audit rules (SafetyTagMap target written,
#                        copied / computed channels, scan-order lag, EDM, ROUT
#                        extra logic, always-on / inverse outputs, AFI without
#                        outputs, timers outside device paths), constant bypass,
#                        ROUT/CROUT restart with a start / seal-in on its rung.
# =============================================================================
"""Textes français."""

TEXT = {
    # ------------------------------------------------------------------ document
    'doc.title': 'SAFETY MATRIX – {name} (SafetyTask)',
    'doc.block': 'Auteur : {author}   •   Révision : {rev}   •   Date : {date}',
    'doc.block_lang': '   •   Langue : feuille « Start »',
    'doc.source': 'Source : {src} • {proc} {ver} • SafetyTask {period} ms',
    'doc.subject': 'Matrice de causes et effets – GuardLogix SafetyTask',
    # ------------------------------------------------------------------ noms des feuilles
    'sheet.start': 'Start',
    'sheet.legend': 'Légende',
    'sheet.sf': 'Fonctions de sécurité',
    'sheet.test': 'Procès-verbal d’essais',
    'sheet.dev': 'Appareils',
    'sheet.out': 'Sorties',
    'sheet.path': 'Chemins C&E',
    'sheet.rep': 'Rapport',
    'sheet.dict': 'Dictionnaire',
    # ------------------------------------------------------------------ liste des feuilles
    'sl.start': 'Page de garde : choix de la langue, liste des feuilles, synthèse.',
    'sl.gi': 'Matrice selon le modèle : lignes = sorties, colonnes = appareils ; Enable Group ; lignes de métadonnées des appareils ; légende.',
    'sl.motor': 'Matrice selon le modèle : lignes = appareils, colonnes = sorties ; commentaires avec le chemin des rungs ; métadonnées des sorties (EDM, réarmement) ; légende.',
    'sl.valve': 'Selon le modèle : vannes de sécurité (sorties marquées comme vannes dans la configuration).',
    'sl.legend': 'Dictionnaire complet des désignations, méthode, historique des révisions, sources.',
    'sl.sf': 'Fonction de sécurité par appareil : sorties, structure d’entrée, temps de réponse (pire cas) à partir des paramètres des connexions CIP Safety, champs PLr / Cat. / PL à remplir.',
    'sl.test': 'Procès-verbal de validation (ISO 13849-2) généré à partir de la matrice : essai de fonction, discordance des voies, combinaisons OU, contournements std, EDM, perte de communication ; colonnes résultat et signature.',
    'sl.dev': 'Voies, instruction, rung, type et source du réarmement, muting, état.',
    'sl.out': 'Adresse/IP, Enable Group et sa logique, EDM, réarmement, redémarrage, CRTL de sortie ; sorties hors matrice.',
    'sl.path': 'Chaque croisement avec son chemin complet tag [routine R rung] et bit de contournement / partenaire OU.',
    'sl.rep': 'Alarmes critiques, éléments morts, liste [À VÉRIFIER] – chacun avec routine et rung.',
    'sl.dict': 'Textes de toutes les langues utilisés par le choix de la langue – les traductions peuvent être corrigées ici.',
    # ------------------------------------------------------------------ zones / groupes / descriptions
    'zone.routine': 'ZONE {n} : routine {routine}',
    'zone.other': 'ZONE {n} : autres appareils',
    'group.routine': 'ROUTINE {routine}',
    'group.info': 'SIGNAUX VERS LA COMMANDE STANDARD (INFO)',
    'group.other': 'AUTRES SORTIES',
    'effdesc.ROUT': 'Sortie de sécurité {instr} {tag} – E/S : {io}',
    'effdesc.OUT': 'Sortie de sécurité {tag} – E/S : {io}',
    'effdesc.DRIVE': '{name} – {catalog} {kind} {desc}',
    'effdesc.INFO': 'Signal vers la commande standard {tag} – {io}',
    # ------------------------------------------------------------------ mots
    'w.all': 'toutes ({n})',
    'w.zone_n': 'ZONE {n}',
    'w.nocomment': 'sans commentaire [À VÉRIFIER]',
    'w.bypass': 'Contournement (bit std) : {bits}',
    'w.conditions': 'Sauf si (condition interne / muting) : {bits}',
    'w.partners': 'Déclenche seulement avec : {devs}',
    'w.delay': 'Temporisation au repos dans le chemin : {ms} ms (catégorie d’arrêt 1)',
    'w.constbypass': 'Ponté par un contact constant (valeur initiale 1, jamais écrit) : {bits}',
    'w.lag': 'Ordre d’exécution : +{n} période(s) de SafetyTask = {ms} ms (valeur du cycle précédent)',
    'src.const': '{op} = constante {v}',
    'src.never': '{op} – jamais écrit (inutilisé)',
    'src.literal': 'constante {v}',
    # ------------------------------------------------------------------ codes
    'code.blank': '(vide)',
    'code.X.short': 'Coupe la sortie directement',
    'code.X.full': 'Le déclenchement de l’appareil (O1 = 0) coupe directement la sortie de sécurité (STO du variateur ou retombée du contacteur). '
                   'Chemin à travers les rungs : commentaire de la cellule (MOTOR) et feuille « Chemins C&E ».',
    'code.X1.short': 'Coupe, mais l’appareil est de fait monovoie  [ALARME]',
    'code.X1.full': 'Comme X, mais les deux voies de l’instruction pointent vers la même entrée (ou entrée directe sans instruction de sécurité) – '
                    'pas de redondance ni de détection de discordance. [ALARME CRITIQUE]',
    'code.XB.short': 'Coupe, mais peut être contourné / inhibé par la commande std  [ALARME]',
    'code.XB.full': 'Coupe la sortie, MAIS un bit de la commande standard (SafetyTagMap) peut ponter ou inhiber (muting) cette fonction. '
                    'Nom du bit de contournement : commentaire de la cellule / « Chemins C&E ». [ALARME CRITIQUE]',
    'code.XC.short': 'Coupe seulement avec un autre appareil (branche OU)',
    'code.XC.full': 'La sortie ne tombe que si l’appareil partenaire est AUSSI déclenché (branches parallèles OU). Un seul déclenchement n’arrête pas. '
                    'Partenaire : commentaire de la cellule / « Chemins C&E ». [À VÉRIFIER]',
    'code.XM.short': 'Coupe, sauf si une condition interne est remplie (muting / mode / données)',
    'code.XM.full': 'Coupe la sortie, mais une condition interne de la SafetyTask (instruction de muting, comparaison, sélecteur de mode, données ou bit '
                    'mémorisé) peut la maintenir. Condition : commentaire de la cellule / « Chemins C&E ». [À VÉRIFIER]',
    'code.N.short': 'Dans la logique, mais non fonctionnel – ne déclenchera jamais  [ALARME]',
    'code.N.full': 'L’appareil est dans le chemin logique mais ne peut jamais couper la sortie : l’instruction a des '
                   'entrées de voies constantes, ou l’appareil est ponté par un contact constant (tag de valeur '
                   'initiale 1 jamais écrit par la logique). [ALARME CRITIQUE]',
    'code.S.short': 'Info : signal vers la commande std (pas une sortie de sécurité)',
    'code.S.full': 'Colonne d’information : état transmis à la commande STANDARD (p. ex. verrouillage vers une autre machine). Ce n’est pas une sortie de sécurité.',
    'code.SB.short': 'Comme S, avec contournement possible par la commande std',
    'code.SB.full': 'Comme S, avec contournement possible par un bit standard (voir XB).',
    'code.SC.short': 'Comme S, seulement avec un autre appareil (OU)',
    'code.SC.full': 'Comme S, seulement avec l’appareil partenaire (voir XC).',
    'code.SM.short': 'Comme S, sauf si une condition interne est remplie',
    'code.SM.full': 'Comme S, avec une condition interne pouvant maintenir le signal (voir XM).',
    'code.none.short': 'Aucun lien dans le code de la SafetyTask',
    'code.none.full': 'Aucun chemin logique dans le code de la SafetyTask entre l’appareil et la sortie.',
    # ------------------------------------------------------------------ types d'appareils
    'type.EMERGENCY STOP': 'Arrêt d’urgence', 'type.SAFETY DOOR': 'Porte de sécurité', 'type.SAFETY GATE': 'Portillon de sécurité',
    'type.SAFETY SWITCH': 'Interrupteur de sécurité', 'type.LIGHT CURTAIN': 'Barrière immatérielle', 'type.SAFETY SCANNER': 'Scrutateur de sécurité',
    'type.SAFETY MAT': 'Tapis de sécurité', 'type.TWO-HAND CONTROL': 'Commande bimanuelle', 'type.ENABLING DEVICE': 'Dispositif de validation',
    'type.ANALOG SAFETY INPUT': 'Entrée de sécurité analogique', 'type.SAFETY INPUT': 'Entrée de sécurité',
    'type.DIRECT SAFETY INPUT': 'Entrée de sécurité directe', 'type.EXTERNAL SAFETY SIGNAL': 'Signal de sécurité externe',
    'typedesc.EMERGENCY STOP': 'dispositif d’arrêt d’urgence (coup de poing)',
    'typedesc.SAFETY DOOR': 'protecteur mobile / porte (interrupteur de porte, interverrouillage)',
    'typedesc.SAFETY GATE': 'portillon / porte d’accès',
    'typedesc.SAFETY SWITCH': 'interrupteur de sécurité (de position / de verrouillage)',
    'typedesc.LIGHT CURTAIN': 'barrière / rideau immatériel',
    'typedesc.SAFETY SCANNER': 'scrutateur laser de sécurité',
    'typedesc.SAFETY MAT': 'tapis sensible à la pression',
    'typedesc.TWO-HAND CONTROL': 'dispositif de commande bimanuelle',
    'typedesc.ENABLING DEVICE': 'dispositif de validation / boîtier de validation',
    'typedesc.ANALOG SAFETY INPUT': 'entrée de sécurité analogique à deux voies',
    'typedesc.SAFETY INPUT': 'entrée de sécurité à deux voies (type non reconnu dans le programme – voir la description)',
    'typedesc.DIRECT SAFETY INPUT': 'entrée de sécurité utilisée directement dans la logique, sans instruction d’entrée de sécurité',
    'typedesc.EXTERNAL SAFETY SIGNAL': 'signal de sécurité consommé d’un autre automate (tag produced/consumed de sécurité)',
    'fn.EMERGENCY STOP': 'Arrêt d’urgence', 'fn.SAFETY DOOR': 'Verrouillage du protecteur – l’ouverture de la porte arrête',
    'fn.SAFETY GATE': 'Verrouillage du portillon – l’ouverture arrête', 'fn.SAFETY SWITCH': 'Interrupteur de sécurité',
    'fn.LIGHT CURTAIN': 'Arrêt à l’interruption de la barrière', 'fn.SAFETY SCANNER': 'Arrêt à la violation du champ de protection du scrutateur',
    'fn.SAFETY MAT': 'Arrêt en marchant sur le tapis', 'fn.TWO-HAND CONTROL': 'Commande bimanuelle',
    'fn.ENABLING DEVICE': 'Fonction de validation', 'fn.ANALOG SAFETY INPUT': 'Seuil de sécurité analogique',
    'fn.SAFETY INPUT': 'Fonction d’entrée de sécurité', 'fn.DIRECT SAFETY INPUT': 'Entrée de sécurité directe',
    'fn.EXTERNAL SAFETY SIGNAL': 'Verrouillage depuis un autre automate de sécurité',
    'act.EMERGENCY STOP': 'Appuyez sur l’arrêt d’urgence', 'act.SAFETY DOOR': 'Ouvrez la porte', 'act.SAFETY GATE': 'Ouvrez le portillon',
    'act.SAFETY SWITCH': 'Actionnez l’interrupteur de sécurité', 'act.LIGHT CURTAIN': 'Interrompez la barrière avec la tige d’essai',
    'act.SAFETY SCANNER': 'Introduisez l’objet d’essai dans le champ de protection du scrutateur', 'act.SAFETY MAT': 'Montez sur le tapis de sécurité',
    'act.TWO-HAND CONTROL': 'Relâchez un des organes de commande bimanuelle', 'act.ENABLING DEVICE': 'Relâchez le dispositif de validation',
    'act.ANALOG SAFETY INPUT': 'Amenez le signal analogique au-delà du seuil de sécurité', 'act.SAFETY INPUT': 'Ouvrez le circuit d’entrée de sécurité',
    'act.DIRECT SAFETY INPUT': 'Ouvrez le circuit d’entrée', 'act.EXTERNAL SAFETY SIGNAL': 'Déclenchez la fonction de sécurité dans l’automate producteur',
    # ------------------------------------------------------------------ types de sorties
    'kindshort.ROUT': 'ROUT', 'kindshort.CROUT': 'CROUT', 'kindshort.OUT': 'Sortie de sécurité', 'kindshort.STO': 'STO CIP Safety',
    'kindshort.SS1': 'SS1 CIP Safety', 'kindshort.SBC': 'SBC CIP Safety', 'kindshort.SLS': 'SLS CIP Safety', 'kindshort.INFO': 'Bit std (info)',
    'kind.ROUT': 'Redundant Output – paire de sorties de sécurité commandant des contacteurs / vannes de sécurité avec retour EDM (NEGATIVE : sortie ON → retour OFF ; '
                 'POSITIVE : le retour suit la sortie). Les sorties suivent Enable – le réarmement du ROUT n’efface que le défaut.',
    'kind.CROUT': 'Configurable Redundant Output – comme ROUT, avec temps de réaction du retour et surveillance Input/Output Status.',
    'kind.OUT': 'Point de sortie de sécurité écrit par une bobine (OTE) sans instruction de sortie avec EDM.',
    'kind.STO': 'Variateur via CIP Safety : :SO.SafeTorqueOff = 1 couple autorisé, 0 = STO. Réarmement du variateur :SO.Reset ; état :SI.TorqueDisabled, :SI.SafetyFault.',
    'kind.SS1': 'Demande de Safe Stop 1 au variateur via CIP Safety (arrêt contrôlé, puis STO).',
    'kind.SBC': 'Safe Brake Control via CIP Safety.',
    'kind.SLS': 'Demande de Safely-Limited Speed via CIP Safety.',
    'kind.INFO': 'Bit d’information écrit par la SafetyTask et lu par la commande standard (p. ex. verrouillage vers une autre machine). Ce n’est pas une sortie de sécurité.',
    # ------------------------------------------------------------------ instructions
    'ins.ESTOP': 'Emergency Stop (legacy) – 2 voies ; .O1 = 1 OK, 0 = actionné / défaut ; réarmement MANUAL ou AUTOMATIC.',
    'ins.RIN': 'Redundant Input (legacy) – 2 voies (portes, portillons, interrupteurs).',
    'ins.LC': 'Light Curtain (legacy) – entrée Mute = 1 ignore la barrière (muting) ; filtre d’entrée en ms.',
    'ins.DIN': 'Diverse Input – 2 voies complémentaires.',
    'ins.ENPEN': 'Enable Pendant – dispositif de validation.',
    'ins.THRS': 'Two-Hand Run Station – commande bimanuelle.', 'ins.THRSE': 'Two-Hand Run Station Enhanced.',
    'ins.DCS': 'Dual Channel Input Stop – fonction de sécurité configurable, temps de discordance, redémarrage MANUAL/AUTOMATIC.',
    'ins.DCST': 'Dual Channel Input Stop with Test.', 'ins.DCSTM': 'Dual Channel Input Stop with Test and Mute.',
    'ins.DCSTL': 'Dual Channel Input Stop with Test and Lock.', 'ins.DCSRT': 'Dual Channel Input Start.',
    'ins.DCM': 'Dual Channel Input Monitor.', 'ins.DCA': 'Dual Channel Analog Input.', 'ins.DCAF': 'Dual Channel Analog Input (virgule flottante).',
    'ins.SMAT': 'Safety Mat – tapis de sécurité.',
    'ins.ROUT': 'Redundant Output – sortie redondante avec surveillance EDM (Feedback).',
    'ins.CROUT': 'Configurable Redundant Output – sortie redondante avec surveillance EDM et temps de réaction du retour.',
    'ins.TSAM': 'Two Sensor Asymmetrical Muting – muting asymétrique à deux capteurs.', 'ins.TSSM': 'Two Sensor Symmetrical Muting – muting symétrique à deux capteurs.',
    'ins.FSBM': 'Four Sensor Bidirectional Muting – muting bidirectionnel à quatre capteurs.',
    'ins.FPMS': 'Five Position Mode Selector – sélecteur de mode.', 'ins.EPMS': 'Eight Position Mode Selector – sélecteur de mode.',
    'ins.TON': 'Timer On Delay – temporisation au travail.', 'ins.TOF': 'Timer Off Delay – temporisation au repos (catégorie d’arrêt 1).',
    'ins.RTO': 'Retentive Timer On.', 'ins.TONR': 'Timer On Delay with Reset.',
    'ins.TOFR': 'Timer Off Delay with Reset – temporisation au repos (catégorie d’arrêt 1).', 'ins.RTOR': 'Retentive Timer On with Reset.',
    'ins.TONS': 'Temporisation de sécurité au travail.', 'ins.TOFS': 'Temporisation de sécurité au repos (catégorie d’arrêt 1).',
    'ins.OSF / OSR': 'One Shot Falling / Rising – impulsion sur front (généralement pour le réarmement).',
    'ins.XIC / XIO': 'Contact normalement ouvert (teste 1) / normalement fermé (teste 0).',
    'ins.OTE / OTL / OTU': 'Bobine / mémorisation (Latch) / démémorisation (Unlatch).',
    'ins..O1': 'Sortie d’une instruction de sécurité : 1 = état sûr / armé (OK), 0 = violation / déclenchement.',
    'ins..FP': 'Fault Present – instruction en défaut (p. ex. discordance des voies, défaut EDM).',
    'ins.unknown': 'Instruction utilisée dans la SafetyTask (voir la documentation Rockwell).',
    # ------------------------------------------------------------------ légende (coin / bloc)
    'lg.title': 'LÉGENDE DES DÉSIGNATIONS',
    'lg.ids': 'ID des appareils : ',
    'lg.id_suffix': '  (TYPE zone.n°)',
    'lg.abbr_head': 'Abréviations : ',
    'lg.abbr_line': 'R = rung (à partir de 0) · M/A = réarmement manuel/automatique · Cat. 0 = STO / coupure, Cat. 1 = SS1 · · = ET, ∥ = OU · '
                    'std = commande standard · bit std = tag SafetyTagMap (standard → sécurité)',
    'lg.full_note': 'Légende complète avec couleurs : sous la matrice et dans la feuille « Légende ».',
    'lg.read': 'Lecture',
    'lg.codes': 'Codes des cellules de la matrice',
    'lg.ids_head': 'Désignations des appareils (ID)',
    'lg.format': 'Format',
    'lg.id_format': 'Format de l’ID : TYPE zone.numéro – p. ex. « ES 3.1 » = arrêt d’urgence n° 1 dans la zone 3. ID attribués séquentiellement sauf '
                    'définition dans la configuration ; le tag Logix est toujours indiqué à côté.',
    'lg.kinds': 'Types de sorties',
    'lg.abbr_main': 'Principales abréviations (liste complète : feuille « Légende »)',
    'read.gi': 'Lecture : ligne = sortie (effet), colonne = appareil (cause). Cellule = ce qui arrive à la sortie de la ligne lorsque l’appareil de la colonne se déclenche.',
    'read.motor': 'Lecture : ligne = appareil (cause), colonne = sortie (effet). Survolez une cellule colorée – le commentaire montre le chemin à travers les rungs.',
    'read.valve': 'Disposition comme MOTOR (lignes = appareils), colonnes = sorties marquées comme vannes dans la configuration.',
    'abbr': [
        ['Saw R22', 'Routine « Saw », rung 22. Les rungs sont numérotés à partir de 0 – comme dans Studio 5000.'],
        ['M / A', 'Réarmement MANUAL (nécessite un bouton / un front) / AUTOMATIC (automatique dès que la cause disparaît).'],
        ['Cat. 0 / Cat. 1', 'Catégorie d’arrêt selon IEC 60204-1 : 0 = coupure immédiate de l’énergie (STO), 1 = freinage contrôlé, puis coupure (SS1, temporisation au repos).'],
        ['STO / SS1', 'Safe Torque Off / Safe Stop 1.'],
        ['EDM', 'External Device Monitoring – boucle de retour des contacts des contacteurs / vannes (Feedback ROUT/CROUT). Métadonnée – ce n’est pas une cause.'],
        ['Enable Group', 'Condition (tag de zone ou ensemble de bits .O1) qui doit être vraie pour que la sortie puisse être enclenchée.'],
        ['·   ∥   NOT', 'Dans les descriptions logiques : · = ET (série), ∥ = OU (branche parallèle), NOT = contact XIO.'],
        ['std', 'Commande standard (programmes des tâches standard – non sécurité).'],
        ['SafetyTagMap', 'Mappage d’un tag standard vers un tag de sécurité (std → sécurité). Autorisé uniquement pour le réarmement / le diagnostic, jamais comme source d’une fonction de sécurité.'],
        ['Module:4:O.Pt00', 'Adresse E/S : adaptateur « Module », emplacement 4, sortie (« O ») point 00 ; « :I.Pt02 » = entrée point 02 ; « :SO. » / « :SI. » = sortie / entrée CIP Safety d’un variateur.'],
        ['CRTL', 'Connection Reaction Time Limit d’une connexion CIP Safety = RPI × (TM + NDM) pour les entrées (Rockwell 1756-RM012).'],
        ['[ALARME CRITIQUE]', 'Contournement / appareil non fonctionnel ou tag std maintenant la logique de sécurité – correction requise.'],
        ['[À VÉRIFIER]', 'Ambiguïté dans le code ou la description – à vérifier sur site / sur les schémas (rapport de validation, avec routine et rung).'],
        ['MORT', 'Appareil / tag / voie sans effet sur aucune sortie de sécurité.'],
    ],
    'colors': [
        ['Zone / groupe de sorties', 'En-tête de zone (colonne dans Group Interlocks) ou de groupe de sorties (colonne dans MOTOR).'],
        ['ID / tag', 'Cellule avec l’ID de l’appareil ou le tag de sortie ; ligne de zone dans MOTOR/VALVE.'],
        ['Groupe de sorties', 'Ligne d’en-tête d’un groupe de sorties dans Group Interlocks.'],
        ['Type d’appareil', 'En-tête du type d’appareil / en-têtes de colonnes.'],
        ['Métadonnées', 'Lignes de métadonnées (réarmement, catégorie d’arrêt, EDM). Texte rouge = avertissement (réarmement A, 0 sortie coupée).'],
    ],
    'dv.err_title': 'Code hors légende',
    'dv.err': 'Utilisez un code de la légende : {codes} (ou vide).',
    'dv.prompt_title': 'Code',
    'dv.prompt': 'Choisissez un code – voir la feuille « Légende ».',
    # ------------------------------------------------------------------ Group Interlocks / MOTOR / VALVE
    'gi.effect': 'Sortie (effet) – description',
    'gi.tag': 'Tag de sortie',
    'gi.enable': 'Enable Group',
    'gi.reset_row': 'Réarmement de l’appareil (M = MANUAL / A = AUTOMATIC)',
    'gi.cat_row': 'Catégorie d’arrêt',
    'gi.count_row': 'Nombre de sorties de sécurité coupées',
    'gi.valve_head': 'VANNES DE SÉCURITÉ (section VALVE du modèle)',
    'gi.valve_none': 'Aucune marquée – les sorties de la SafetyTask ne sont pas identifiées comme vannes. Récepteurs des sorties ROUT/CROUT à vérifier sur les schémas.',
    'm.type': 'Type',
    'm.desc': 'Description de l’appareil (programme / commentaires E/S)',
    'm.id': 'ID / tag Logix',
    'm.meta_head': 'MÉTADONNÉES DES SORTIES (EDM / RÉARMEMENT – colonnes de métadonnées, pas des causes)',
    'm.kind': 'Type de sortie',
    'm.addr': 'Adresse / IP',
    'm.rung': 'Rung de sortie',
    'm.enable': 'Enable Group (condition)',
    'm.edm': 'EDM / retour',
    'm.reset': 'Réarmement de la sortie',
    'm.restart': 'Redémarrage',
    'm.cat': 'Catégorie d’arrêt',
    'm.count': 'Nombre d’appareils coupant la sortie (X, X1, XB, XM, S, SB, SM) – formule',
    'v.legend_ref': 'Légende : feuille « Légende » (ID des appareils TYPE zone.n°)',
    'v.none_head': 'AUCUNE VANNE DE SÉCURITÉ IDENTIFIÉE DANS LA SafetyTask',
    'v.none_text': 'Aucune sortie n’est marquée comme vanne (pneumatique / hydraulique). Si les sorties {outs} alimentent des vannes – marquez-les dans la configuration (effects: <tag>: valve: true).',
    # ------------------------------------------------------------------ textes de métadonnées
    'edm.cip': 'SI.TorqueDisabled / SI.SafetyFault (CIP Safety)',
    'rs.rout_fault': '(réarmement du défaut ROUT)',
    'rs.none': 'aucun (pas d’auto-maintien – suit la logique)',
    'rs.so_reset': '  + rung SO.Reset ({rung})',
    'restart.rout': 'AUTO – la sortie ROUT/CROUT suit Enable (réarmement des appareils = redémarrage)',
    'restart.rout_seal': 'MANUEL – le rung ROUT/CROUT a un démarrage / auto-maintien : redémarrage uniquement par '
                         '{tags}',
    'restart.auto': 'AUTO – signal de niveau dans la branche d’auto-maintien : {tags}',
    'restart.manual': 'MANUEL – front de réarmement + auto-maintien',
    'restart.follow': 'suit la logique',
    # ------------------------------------------------------------------ feuille Appareils
    'd.zone': 'Zone', 'd.id': 'ID', 'd.type': 'Type', 'd.tag': 'Tag Logix', 'd.desc': 'Description', 'd.instr': 'Instruction',
    'd.cha': 'Voie A', 'd.chb': 'Voie B', 'd.routine': 'Routine', 'd.rung': 'Rung', 'd.reset_type': 'Réarmement (type)',
    'd.reset_tag': 'Tag de réarmement', 'd.reset_src': 'Source du réarmement (physique / logique)', 'd.reset_rung': 'Rung du réarmement',
    'd.mute': 'Muting (entrée Mute)', 'd.n_eff': 'Nb de sorties de sécurité coupées', 'd.cat': 'Cat. d’arrêt', 'd.status': 'État',
    'st.dead': 'MORT – aucun effet sur les sorties de sécurité', 'st.auto': 'Réarmement AUTO', 'st.equal': 'Voies A = B (monovoie)',
    'st.const': 'Entrées constantes', 'st.std': 'Entrées de la commande std (SafetyTagMap)', 'st.mute': 'Muting par la commande std',
    'st.direct': 'Entrée directe sans instruction de sécurité', 'st.external': 'Tag de sécurité consommé', 'st.heuristic': 'Opérandes déduits – à vérifier',
    # ------------------------------------------------------------------ feuille Sorties
    'o.group': 'Groupe', 'o.tag': 'Tag', 'o.desc': 'Description', 'o.kind': 'Type', 'o.addr': 'Adresse / IP', 'o.rung': 'Rung de sortie',
    'o.enable': 'Enable Group', 'o.enable_rung': 'Rung Enable', 'o.logic': 'Logique Enable (du rung ; · = ET, ∥ = OU)',
    'o.edm': 'EDM / retour', 'o.reset': 'Réarmement', 'o.restart': 'Redémarrage', 'o.cat': 'Catégorie d’arrêt', 'o.crtl': 'Output CRTL [ms]',
    'o.aux_head': 'SORTIES DE SÉCURITÉ HORS MATRICE (aucun appareil d’entrée dans leur logique ou non enclenchées à l’état sain) – voir le rapport de validation',
    'o.reason.no_device': 'Aucun appareil d’entrée de sécurité dans la logique (p. ex. déverrouillage, voyant, demande) – pas une fonction d’arrêt.',
    'o.reason.not_energized': 'Non enclenchée à l’état sain (nécessite une demande / une séquence pour s’enclencher).',
    # ------------------------------------------------------------------ feuille Chemins
    'p.dev': 'Appareil (cause)', 'p.eff': 'Sortie (effet)', 'p.code': 'Code',
    'p.path': 'Chemin logique (tag [routine rung]) – de l’instruction d’entrée à la sortie',
    'p.extra': 'Bit de contournement (std) / partenaire OU / condition',
    # ------------------------------------------------------------------ Rapport
    'r.title': 'RAPPORT DE VALIDATION – AUDIT DU CODE GuardLogix (SafetyTask)',
    'r.note': 'Les rungs sont numérotés à partir de 0 (comme dans Studio 5000). Ordre d’exécution : {order}. Désignations : feuille « Légende ». '
              'Le rapport est généré automatiquement – chaque point doit être examiné par une personne compétente.',
    'r.sec_alarm': '1. CONTOURNEMENTS / APPAREILS NON FONCTIONNELS / AFI DÉTECTÉS   [ALARME CRITIQUE]   ({n})',
    'r.sec_dead': '2. ENTRÉES / SORTIES / TAGS MORTS   ({n})',
    'r.sec_verify': '3. ÉLÉMENTS [À VÉRIFIER]   ({n})',
    'r.cols_alarm': [['N°', 'Routine', 'Rung', 'Élément', 'Constat', 'Recommandation']],
    'r.cols_dead': [['N°', 'Routine', 'Rung', 'Élément', 'Constat', 'Classification']],
    'r.cols_verify': [['N°', 'Routine', 'Rung', 'Élément', 'Constat', 'Action']],
    'r.none': 'Aucun élément trouvé.',
    'r.priority': 'PRIORITÉ : ',
    # ------------------------------------------------------------------ constats : ALARME
    'f.const_channels': 'L’instruction {instr} {tag} a des entrées de voies constantes ({cha}, {chb}) – elle ne peut JAMAIS déclencher, alors que sa sortie est utilisée dans : {uses}. '
                        'Elle donne une fausse impression de protection.',
    'f.const_channels.rec': 'Raccorder les voies physiques à l’instruction ou retirer l’appareil de la documentation de sécurité ; vérifier le câblage.',
    'f.std_channels': 'Les voies A/B de {instr} {tag} proviennent de tags STANDARD mappés via SafetyTagMap ({cha}, {chb}). Source : {src}. '
                      'La fonction n’a aucune intégrité de sécurité.',
    'f.std_channels.rec': 'Raccorder l’appareil à un module d’entrées de sécurité ou transmettre le signal comme tag de sécurité produced/consumed entre automates de sécurité.',
    'f.std_bypass': 'Le bit standard {bit} est dans une branche parallèle à la condition de sécurité – avec le bit = 1 les appareils {devices} ne coupent pas : {effects}. '
                    'Source du bit : {src}. Un tag SafetyTagMap maintient directement la logique de sécurité.',
    'f.std_bypass.rec': 'Supprimer le contournement par la commande standard ; si une condition est nécessaire, la construire à partir d’entrées / instructions de sécurité (p. ex. muting TSAM/TSSM/FSBM).',
    'f.std_mute': 'Le muting de {tag} ({instr}, opérande {operand}) est commandé par le(s) bit(s) standard {bits}. Source : {src}.',
    'f.std_mute.rec': 'Réaliser le muting uniquement avec TSAM/TSSM/FSBM et des capteurs de muting sur des entrées de sécurité ; ne pas inhiber depuis la commande standard.',
    'f.mute_const': 'L’entrée Mute de {tag} est la constante 1 – la barrière est inhibée en permanence.',
    'f.mute_const.rec': 'Raccorder l’entrée Mute à une fonction de muting sûre ou la mettre à 0.',
    'f.std_parallel': 'Le bit standard {bit} peut à lui seul activer {tag}, dont la logique exige sinon des conditions d’entrées de sécurité : {expr}. Source : {src}.',
    'f.std_parallel.rec': 'Supprimer la branche standard ou la remplacer par un signal de sécurité (p. ex. surveillance sûre de l’arrêt via CIP Safety).',
    'f.estop_auto': 'Le(s) arrêt(s) d’urgence {tags} ont un réarmement AUTOMATIC – après déverrouillage du bouton, O1 = 1 et les sorties {effects} peuvent se réenclencher '
                    'sans réarmement manuel (ISO 13850 : le réarmement d’un arrêt d’urgence doit être une action manuelle délibérée et ne doit pas provoquer de redémarrage).',
    'f.estop_auto.rec': 'Passer le Reset Type à MANUAL avec un bouton de réarmement hors de la zone dangereuse ; vérifier qu’aucune sortie ne redémarre automatiquement.',
    'f.equal_channels': 'Les deux voies de {instr} {tag} pointent vers la même entrée {ch} – pas de redondance ni de détection de discordance ; la fonction est '
                        'de fait monovoie ({n} sortie(s) de sécurité concernée(s)).',
    'f.equal_channels.rec': 'Raccorder la voie B à une entrée séparée et corriger l’opérande ; vérifier le câblage du capteur.',
    'f.afi': 'Instruction AFI (Always False) dans {rung} – le rung est désactivé en permanence ; il coupe en '
             'permanence : {outputs}.',
    'f.afi.rec': 'Supprimer l’AFI ou documenter la raison ; vérifier qu’aucune fonction de sécurité ne dépend de ce rung.',
    'f.const_branch': 'Une branche composée uniquement de contacts constants ({consts}) est toujours vraie et ponte '
                      'la logique de {tag}. Appareils pontés : {devices}.',
    'f.const_branch.rec': 'Supprimer la branche de pontage ou remplacer la constante par une véritable condition de sécurité.',
    'f.reset_std_auto': 'Le bit de réarmement {bit} est généré automatiquement (mémorisé dans la séquence standard ou écrit par la SafetyTask elle-même) et réarme : {resets}. '
                        'Source : {src}. Réarmement sans action délibérée de l’opérateur.',
    'f.reset_std_auto.rec': 'Réarmer uniquement par bouton-poussoir (front) hors de la zone dangereuse ; supprimer les sources de réarmement automatique de la commande standard.',
    # ------------------------------------------------------------------ constats : MORTS
    'f.dead_device': 'La sortie de {tag} ne coupe aucune sortie de sécurité ; elle n’est utilisée que dans : {uses}.',
    'f.dead_muting': 'La sortie .O1 de l’instruction de muting {tag} n’est utilisée dans aucun rung.',
    'f.const_tags': 'Tags jamais écrits dans la SafetyTask (valeurs initiales constantes) mais lus dans la logique : {tags}.',
    'f.unused_tags': 'Tags de sécurité définis mais non utilisés dans la logique exécutée de la SafetyTask : {tags}.',
    'f.unused_inputs': 'Entrées de sécurité du module {module} non utilisées dans la SafetyTask : {channels}.',
    'f.unused_outputs': 'Sorties de sécurité du module {module} non utilisées dans la SafetyTask : {channels}.',
    'f.unused_module': 'Module d’entrées de sécurité {module} – aucune de ses entrées n’est utilisée dans la SafetyTask.',
    'f.uncalled_routine': 'La routine {routine} ({n} rungs) n’est jamais appelée (pas de JSR) – sa logique n’est pas exécutée.',
    'f.drive_unused': 'Le variateur {module} a une connexion CIP Safety mais aucune référence dans la SafetyTask.',
    'f.module_unused': 'Le module {module} a une connexion de sécurité mais aucune référence dans la SafetyTask.',
    'f.drives_hardwired': 'Variateurs sans connexion CIP Safety (un éventuel STO câblé est hors du code) : {modules}.',
    'cls.dead_input': 'Entrée morte (pour les sorties de sécurité)', 'cls.dead_block': 'Bloc mort', 'cls.const_tag': 'Tags constants',
    'cls.dead_tags': 'Tags morts', 'cls.dead_channel': 'Voies mortes', 'cls.dead_routine': 'Routine morte',
    'cls.outside_code': 'Hors du code', 'cls.dead': 'Mort',
    # ------------------------------------------------------------------ constats : À VÉRIFIER
    'f.aux_no_device': 'La sortie de sécurité {tag} n’est coupée par aucun appareil d’entrée de sécurité (logique : {expr}) – p. ex. déverrouillage ou voyant. '
                       'Vérifier la fonction et ses conditions.',
    'f.aux_not_energized': 'La sortie de sécurité {tag} n’est pas enclenchée à l’état sain (logique : {expr}) – absente de la matrice ; vérifier la fonction.',
    'f.crtl_inputs': 'Entrées de sécurité de {adapter} : RPI {rpi} ms, Timeout Multiplier {tm}, Network Delay '
                     'Multiplier {ndm} % → Input CRTL {crtl} ms. Temps de réponse le plus défavorable de la logique '
                     'seule (Input CRTL + filtre LC + période de la tâche {period} ms + watchdog {watchdog} ms + '
                     'Output CRTL) jusqu’à {total} ms – hors temps du capteur et d’arrêt. Appareils : {devices}. '
                     'Vérifier par rapport à l’appréciation du risque et aux distances de sécurité (ISO 13855) ; '
                     'détails : feuille « Fonctions de sécurité ». Retard dû à l’ordre d’exécution inclus : {lags} × '
                     'période de la tâche.',
    'f.crtl_outputs': 'Modules de sorties de sécurité {modules} : RPI {rpi} ms, TM {tm}, NDM {ndm} % → Output CRTL {crtl} ms.',
    'f.crtl_drives': 'Connexions de sortie CIP Safety des variateurs : RPI {rpi} ms, TM {tm}, NDM {ndm} % → CRTL {crtl} ms pour : {modules}.',
    'f.osf_ote': 'OSF/OSR et OTE sur le même tag {tag} dans un rung – l’OTE écrase l’impulsion de front par le niveau (réarmement par niveau au lieu du front).',
    'f.double_ote': 'Le tag {tag} est écrit par {n} bobines OTE – seule la dernière du cycle détermine la valeur.',
    'f.rout_reset_fp': 'Le réarmement du défaut {reset} de {tag} est conditionné par {other} (défaut d’une AUTRE instruction de sortie) – probable erreur de copie.',
    'f.or_devices': 'Les appareils {a} et {b} sont en parallèle (OU) – le déclenchement de l’un d’eux ne coupe pas {effects} (code XC). À confirmer avec l’appréciation du risque.',
    'f.auto_restart': 'La branche d’auto-maintien de {tag} contient un signal de niveau ({levels}) – la sortie redémarre automatiquement à son retour (pas de réarmement indépendant).',
    'f.auto_reset_guard': 'L’appareil de protection {tag} a un réarmement AUTOMATIC – après fermeture, les sorties {effects} peuvent redémarrer sans réarmement. Confirmer qu’un '
                          'redémarrage est impossible lorsqu’une personne se trouve dans la zone dangereuse (ISO 13849-1 §5.2.2, ISO 14119).',
    'f.reset_std': 'Réarmement par la commande standard : le bit {bit} réarme {resets}. Source : {src}. Vérifier l’emplacement et la visibilité du bouton de réarmement '
                   '(réarmement manuel hors de la zone dangereuse, ISO 13849-1 §5.2.2).',
    'f.std_not_written': 'Le bit mappé depuis le standard {bit} est lu dans la SafetyTask, mais aucune écriture de '
                         '{src} n’a été trouvée dans le code standard. Seuls un IHM/SCADA, une instruction MSG ou '
                         'une modification en ligne pourraient l’écrire.',
    'f.missing_comments': 'Pas de commentaires de voies E/S sur {module} ({channels}) – affectation de {who} uniquement d’après les noms des tags.',
    'f.free_cmp': 'Comparaison {leaf} dans la logique de {effects} – supposée {value} à l’état sain ; le résultat dépend des données.',
    'f.free_data': 'Bit dépendant de données {leaf} (écrit par une instruction de données) dans la logique de {effects} – supposé {value} à l’état sain.',
    'f.free_latch': 'Bit mémorisé {leaf} (OTL/OTU) dans la logique de {effects} – supposé {value} à l’état sain ; vérifier les conditions de mémorisation.',
    'f.free_unk': 'Bit {leaf} de valeur inconnue dans la logique de {effects} – supposé {value}.',
    'f.free_mute': 'Le muting {leaf} agit sur {effects} – pendant le muting la barrière ne coupe pas (code XM).',
    'f.free_ext': 'Tag de sécurité consommé {leaf} dans la logique de {effects} – vérifier l’automate producteur.',
    'f.direct_direct': 'L’entrée de sécurité {tag} est utilisée directement dans la logique de {effects} sans instruction d’entrée de sécurité (pas de surveillance de discordance).',
    'f.direct_external': 'Le tag de sécurité consommé {tag} coupe {effects} – la fonction est réalisée dans un autre automate.',
    'f.heuristic': 'Les opérandes de {instr} {tag} ont été attribués heuristiquement ({roles}) – confirmer les voies et le réarmement dans Studio 5000.',
    'f.device_conditional': 'L’instruction d’entrée de sécurité {tag} est sur un rung conditionnel – si le rung est faux, la sortie .O1 est remise à zéro.',
    'f.routine_not_analysed': 'La routine {routine} ({kind}) n’a pas pu être analysée (protégée ou non ladder) – sa logique n’est pas reflétée dans la matrice.',
    'f.aoi_conditional': 'L’Add-On Instruction {aoi} est appelée sur un rung conditionnel – l’analyse suppose EnableIn = 1.',
    'f.flow': 'Instruction de contrôle du déroulement {instr} dans la SafetyTask – la matrice suppose l’exécution continue de chaque rung.',
    'f.unknown_instr': 'L’instruction {instr} n’est pas connue de l’analyseur – traitée comme transparente ; vérifier son effet manuellement.',
    'f.aoi_protected': 'L’Add-On Instruction {aoi} ({inst}) est protégée (source protection) – ses sorties sont traitées comme inconnues.',
    'f.jsr_conditional': 'La routine {routine} est appelée conditionnellement – ses sorties gardent leur état lorsqu’elle n’est pas exécutée.',
    'f.pair_mismatch': 'Les sorties {a} et {b} de {tag} ont des causes différentes dans la logique – vérifier le câblage des deux voies.',
    'f.loads': 'Le code ne définit pas ce qui est alimenté par les sorties {outputs} (contacteurs / STO câblé / vannes) – à confirmer sur les schémas électriques.',
    'f.stop_cat0': 'Aucune temporisation au repos sur un chemin appareil de sécurité → sortie, donc toutes les fonctions '
                   'de sécurité sont en catégorie d’arrêt 0 (STO / retombée du contacteur). Pour les machines à '
                   'forte inertie, envisager SS1 selon l’appréciation du risque.',
    'f.stop_cat1': 'Temporisations au repos sur les chemins appareil de sécurité → sortie : {timers} – les sorties '
                   '{effects} s’arrêtent en catégorie 1 (SS1) ; vérifier la temporisation par rapport au temps '
                   'd’arrêt.',
    'f.forces': 'Les forçages ne sont pas enregistrés dans l’export – vérifier l’onglet Forces des tags de sécurité en ligne dans Studio 5000.',
    'f.completeness': 'Fichier analysé {src} ; routines exécutées et nombres de rungs : {routines}. Confirmer les nombres de rungs dans Studio 5000.',
    'f.afi_noop': 'AFI (Always False) dans {rung} sur un rung sans instruction de sortie (p. ex. seulement NOP) – '
                  'sans effet sur la logique aujourd’hui, mais c’est un rung désactivé dans la tâche de sécurité.',
    'f.afi_noop.rec': 'Supprimer le rung ou documenter son but ; vérifier qu’aucune fonction de sécurité ne devait '
                      's’y trouver.',
    'f.map_written': 'Le tag de sécurité {tag} est la destination du SafetyTagMap (depuis le tag standard {src}) et '
                     'il est aussi écrit par la logique de sécurité en {writers}. La valeur standard est copiée au '
                     'début de chaque cycle de la tâche de sécurité puis écrasée – le mappage est sans effet et '
                     'trompeur.',
    'f.map_written.rec': 'Supprimer le mappage ou utiliser un tag de sécurité distinct pour le résultat de la '
                         'logique ; documenter la source voulue.',
    'f.map_read_before_write': 'Le tag de sécurité {tag} est mappé depuis le tag standard {src} (SafetyTagMap) et '
                               'écrit par la logique de sécurité en {writers}, mais il est lu plus tôt dans le cycle '
                               'en {readers} – à cet endroit sa valeur provient de la commande STANDARD.',
    'f.map_read_before_write.rec': 'Supprimer le mappage ou placer l’écriture de sécurité avant chaque lecture ; la '
                                   'valeur standard ne doit pas influencer la fonction de sécurité.',
    'f.aux_always_on': 'La sortie de sécurité {tag} est activée sans condition (logique : {expr}) – aucun appareil '
                       'de sécurité ne peut la couper (p. ex. alimentation d’un capteur ou source de test).',
    'f.aux_always_on.rec': 'Vérifier sur les schémas ce qui est alimenté par cette sortie ; aucune charge dangereuse '
                           'ne doit y être raccordée.',
    'f.aux_inverse': 'La sortie de sécurité {tag} n’est activée que lorsque {devices} déclenchent (logique : {expr}) '
                     '– voyant, déverrouillage d’interverrouillage ou similaire, pas une sortie de fonction de '
                     'sécurité ; non affichée dans la matrice.',
    'f.aux_inverse.rec': 'Vérifier la fonction ; si elle déverrouille un protecteur, vérifier les conditions (arrêt, '
                         'temporisation).',
    'f.channel_copy': 'Les voies de ces instructions sont des tags intermédiaires copiés depuis des entrées '
                      'physiques (XIC(entrée) OTE(copie)) : {devices}. Les copies sont écrites avant l’instruction '
                      'dans le cycle ; la matrice, le CRTL et les commentaires d’E/S utilisent les entrées '
                      'physiques.',
    'f.channel_copy.rec': 'Les rungs de copie ne doivent pas avoir de conditions supplémentaires ; utiliser '
                          'directement les entrées physiques dans l’instruction est plus clair.',
    'f.channel_copy_late': 'Les voies de ces instructions sont des tags intermédiaires copiés depuis des entrées '
                           'physiques, et les rungs de copie s’exécutent APRÈS l’instruction dans le cycle : '
                           '{devices}. L’instruction évalue l’état des entrées du cycle précédent – le temps de '
                           'réponse augmente d’une période de la SafetyTask ({period} ms).',
    'f.channel_copy_late.rec': 'Déplacer les rungs de copie avant les instructions (ordre des JSR dans MainRoutine) '
                               'ou utiliser directement les entrées physiques ; inclure la période supplémentaire '
                               'dans le temps de réponse.',
    'f.channel_logic': 'La voie {ch} de {instr} {tag} n’est pas une entrée physique mais un tag calculé par la '
                       'logique : {expr}. La redondance et la surveillance de discordance de l’instruction portent '
                       'alors sur cette logique, pas sur le capteur.',
    'f.channel_logic.rec': 'Raccorder directement les voies physiques à l’instruction ou justifier la logique dans '
                           'le concept de sécurité.',
    'f.scan_lag': 'Le tag {tag} est écrit en {writer} mais lu plus tôt dans le cycle en {readers} – ces rungs '
                  'utilisent la valeur du cycle précédent : +1 période de SafetyTask ({period} ms) dans le temps de '
                  'réponse de : {effects}.',
    'f.scan_lag.rec': 'Modifier l’ordre des routines / rungs pour que le tag soit écrit avant d’être lu, ou inclure '
                      'la période supplémentaire dans le temps de réponse.',
    'f.edm_same_channel': 'Les deux entrées de retour de {instr} {tag} utilisent la même voie {ch} – les contacts '
                          'auxiliaires des deux contacteurs sont câblés en série sur une seule entrée ; un défaut de '
                          'cette entrée ou de ce fil n’est pas détecté par l’EDM.',
    'f.edm_same_channel.rec': 'Vérifier que cela satisfait la catégorie / le PL requis ; sinon câbler chaque retour '
                              'sur sa propre entrée.',
    'f.rout_extra_logic': 'Les sorties {outputs} de {instr} {tag} sont aussi coupées par {devices}, qui n’agissent '
                          'pas via la validation de {instr}. Si seuls ceux-ci déclenchent, les sorties retombent '
                          'alors que {tag}.O1 reste actif – le retour ne correspond plus, {tag} signale un défaut de '
                          'retour (réarmement requis) et l’EDM ne surveille pas ce chemin de coupure.',
    'f.rout_extra_logic.rec': 'Intégrer ces conditions dans la validation de {tag} afin que chaque chemin de coupure '
                              'passe par l’instruction surveillée.',
    'f.timer_other': 'La temporisation au repos {tag} ({instr}, présélection {preset} ms) n’est pas sur un chemin '
                     'appareil de sécurité → sortie : elle retarde la condition {cond} ; utilisée par : {users}. Ce '
                     'n’est pas une catégorie d’arrêt 1 d’une fonction de sécurité (p. ex. retard '
                     'd’interverrouillage ou de libération).',
    'f.timer_other.rec': 'Si elle libère un interverrouillage, vérifier la temporisation par rapport au temps de '
                         'ralentissement de la machine.',
    # ------------------------------------------------------------------ feuille Légende
    'l.title': 'LÉGENDE DES DÉSIGNATIONS ET MÉTHODE',
    'l.s1': '1. CODES DES CELLULES DE LA MATRICE', 'l.s2': '2. LECTURE DE LA MATRICE', 'l.s3': '3. DÉSIGNATIONS DES APPAREILS (ID)', 'l.s4': '4. ZONES',
    'l.s5': '5. TYPES DE SORTIES (EFFETS)', 'l.s6': '6. INSTRUCTIONS DE SÉCURITÉ UTILISÉES', 'l.s7': '7. ABRÉVIATIONS DES MÉTADONNÉES / DU RAPPORT',
    'l.s8': '8. COULEURS DES EN-TÊTES ET DES LIGNES', 'l.s9': '9. MÉTHODE ET REMARQUES', 'l.s10': '10. FEUILLES DU CLASSEUR',
    'l.s11': '11. CHAMPS À REMPLIR ET RÉSULTATS DES ESSAIS', 'l.s12': '12. HISTORIQUE DES RÉVISIONS', 'l.s13': '13. SOURCES',
    'l.cols_codes': [['Code', 'Signification (courte)', 'Description complète', 'Nombre – MOTOR', 'Nombre – Group Interl.']],
    'l.sheet': 'Feuille', 'l.axes': 'Axes', 'l.id_abbr': 'Abréviation ID', 'l.type_hdr': 'Type (en-tête de colonne)', 'l.meaning': 'Signification',
    'l.instr': 'Instruction', 'l.count': 'Nombre', 'l.zone_no': 'N° de zone', 'l.id_prefix': 'Préfixe ID', 'l.zone_name': 'Nom de la zone',
    'l.kind': 'Type', 'l.mark': 'Désignation', 'l.sample': 'Exemple', 'l.element': 'Élément', 'l.contents': 'Contenu',
    'l.yellow': '(jaune)', 'l.dropdown': 'Liste déroulante',
    'l.dropdown_txt': 'Les cellules de la matrice (Group Interlocks, MOTOR) ont une liste de codes et une mise en forme conditionnelle – un code modifié '
                      'manuellement prend automatiquement la couleur de la légende. Remarque : le commentaire avec le chemin des rungs décrit l’état généré à partir du programme.',
    'l.rev': 'Révision', 'l.date': 'Date', 'l.changes': 'Description des modifications', 'l.author': 'Auteur', 'l.no': 'N°', 'l.doc': 'Document',
    'l.rev_auto': 'Généré automatiquement par safety-matrix-generator {version}.',
    'l.n.method': 'Méthode : chaque croisement est déterminé de façon déterministe à partir de la logique ladder de la SafetyTask (simulation booléenne de chaque rung '
                  'dans l’ordre de scrutation) : appareil déclenché (O1 = 0), autres appareils sains, bits standard = 0 → X ; si la mise à 1 d’un bit standard rétablit '
                  'la sortie → XB ; si une condition interne la rétablit → XM ; si la sortie ne tombe qu’avec un autre appareil → XC. Aucun lien n’est déduit de la similitude des noms.',
    'l.n.cat0': 'Catégorie d’arrêt : pas de temporisation au repos dans la SafetyTask – toutes les fonctions sont en catégorie 0 (STO via CIP Safety ou retombée du contacteur via ROUT).',
    'l.n.cat1': 'Catégorie d’arrêt : les chemins passant par des temporisations au repos (TOF/TOFR/TOFS) sont en catégorie 1, avec la présélection indiquée dans le commentaire et les métadonnées.',
    'l.n.edm': 'L’EDM / retour et les boutons de réarmement figurent uniquement dans les métadonnées (MOTOR – lignes sous la matrice, feuilles « Appareils » et « Sorties »), jamais comme causes.',
    'l.n.rout': 'Les sorties ROUT/CROUT ont deux voies (p. ex. Pt00/Pt01) – la matrice a une colonne par instruction de sortie (les deux voies sont vérifiées pour des causes identiques).',
    'l.n.comment': 'Les commentaires des cellules MOTOR contiennent le chemin tag [routine R rung] de l’instruction d’entrée jusqu’à la sortie.',
    'l.n.ids': 'Les ID des appareils (TYPE zone.n°) sont attribués séquentiellement sauf définition dans la configuration ; le tag Logix est toujours indiqué à côté.',
    'l.n.tool': 'Généré avec safety-matrix-generator {version} (auteur : Robert Pietroń). Le résultat ne remplace pas la validation selon ISO 13849-2 / IEC 62061.',
    'input_note': 'Champs jaunes – à remplir (données des fiches techniques, de l’appréciation du risque, de SISTEMA ou résultats d’essais). Tous les autres champs ont été générés à partir du programme.',
    'result.OK': 'Résultat conforme au résultat attendu.',
    'result.NOK': 'Essai non conforme – décrire dans la colonne des remarques et signaler pour correction.',
    'result.N/A': 'Sans objet / essai irréalisable (indiquer la raison).',
    # ------------------------------------------------------------------ Fonctions de sécurité
    'sf.title': 'FONCTIONS DE SÉCURITÉ – TEMPS DE RÉPONSE ET NIVEAU DE PERFORMANCE',
    'sf.method': 'Temps de réponse (pire cas) = retard du capteur + Input CRTL + filtre LC + (période de la Safety Task + watchdog) + Output CRTL + retard de la sortie / '
                 'de l’actionneur. Input CRTL = RPI × (TM + NDM) ; Output CRTL = période de la Safety Task × (TM + NDM − 1) – Rockwell 1756-RM012. Valeurs CRTL lues '
                 'dans l’export (ReactionTimeLimit) ; Safety Task : période {period} ms, watchdog {watchdog} ms. Temps d’arrêt de la machine (ISO 13855) = temps de '
                 'réponse + temps de freinage / de ralentissement – à mesurer.',
    'sf.input_hint': 'Sources typiques : temps de réponse des barrières / scrutateurs, temps de retombée des contacteurs – fiche technique ; PLr – appréciation du risque (ISO 13849-1, annexe A) ; PL/PFHd – SISTEMA.',
    'sf.cols': [['SF', 'ID', 'Tag de l’appareil', 'Fonction de sécurité', 'Sorties coupées (X / X1 / XB / XM)', 'Cat. d’arrêt', 'Structure d’entrée (du code)',
                 'Module d’entrée (RPI / TM / NDM)', 'Input CRTL [ms]', 'Filtre LC [ms]', 'Période Safety Task + watchdog [ms]', 'Output CRTL max [ms]',
                 'Retard du capteur [ms]', 'Retard sortie / actionneur [ms]', 'Temps de réponse – total [ms]', 'PLr (appréciation du risque)', 'Catégorie (B, 1–4)',
                 'PL atteint / PFHd', 'Remarques']],
    'sf.s.const': 'Entrées constantes – aucune fonction [ALARME]',
    'sf.s.direct': 'Entrée de sécurité directe sans instruction (monovoie) [ALARME]',
    'sf.s.external': 'Tag de sécurité consommé (fonction dans un autre automate)',
    'sf.s.single': 'Monovoie (voie A = B) – {instr} [ALARME]',
    'sf.s.std': 'Voies de la commande std (SafetyTagMap) – {instr} [ALARME]',
    'sf.s.two': 'Deux voies – {instr}',
    'sf.s.mute': ' ; muting par la commande std [ALARME]',
    'sf.s.xb': ' ; contournement std (XB)',
    'sf.s.xc': ' ; branche OU (XC)',
    'sf.s.xm': ' ; condition interne (XM)',
    'sf.n.xc': 'Coupe {effs} seulement avec {partners} (branche OU).',
    'sf.n.none': 'Aucun effet sur les sorties de sécurité – fonction non réalisée dans la SafetyTask.',
    'sf.n.nonfunc': 'Appareil non fonctionnel (entrées constantes) – la fonction ne marche pas.',
    'sf.n.crtl': 'Input CRTL ≥ {ms} ms – voir le rapport de validation (PRIORITÉ).',
    'sf.n.std': 'Signal provenant de la commande standard – temps de réponse indéterminé.',
    'sf.n.delay': 'Temporisation au repos dans le chemin : {ms} ms (catégorie 1) – à ajouter au temps de réponse.',
    'sf.n.lag': 'L’ordre d’exécution ajoute {n} période(s) de SafetyTask ({ms} ms) – incluses dans la colonne de la '
                'tâche.',
    'sf.only_xc': 'seulement avec le partenaire (XC) : {effs}',
    'sf.cf_note': 'Total sur fond rouge : > 1000 ms ; jaune : 500–1000 ms (mise en forme conditionnelle). Le total est calculé automatiquement après saisie des retards des appareils.',
    # ------------------------------------------------------------------ Procès-verbal d'essais
    't.title': 'PROCÈS-VERBAL DES ESSAIS DE VALIDATION DES FONCTIONS DE SÉCURITÉ (ISO 13849-2)',
    't.pre': 'Conditions préalables : tous les appareils réarmés, sorties de sécurité enclenchées (état prêt), personne dans les zones dangereuses, essai sans matière / '
             'en mode test. Les résultats attendus sont générés à partir du code de la SafetyTask (matrice MOTOR) – un écart entre la réalité et l’attente = NOK.',
    't.result_hint': 'Résultat : OK / NOK / N/A (liste). ',
    't.cols': [['N°', 'Type d’essai', 'ID / Tag', 'Description de l’appareil / de l’élément', 'Action d’essai', 'Résultat attendu (selon le code SafetyTask)',
                'Réarmement / redémarrage – comportement attendu', 'Référence (routine / rung)', 'Remarques / alarme', 'Résultat', 'Date', 'Réalisé par', 'Remarques d’essai']],
    't.k.func': 'Fonction', 't.k.or': 'Combinaison OU', 't.k.byp': 'Contournement std (documentaire)', 't.k.edm': 'EDM', 't.k.comm': 'Perte de communication',
    't.act.xb': 'Le(s) bit(s) de contournement {bits} doivent être inactifs.',
    't.act.mute': 'Muting inactif.',
    't.act.disc': '2) Essai de discordance : appareil à l’état OK, ouvrez seulement la voie A ({a}), puis seulement la voie B ({b}).',
    't.exp.n': 'AUCUN déclenchement – l’instruction a des entrées constantes dans le code ({rung}) ; les sorties restent enclenchées. [ALARME CRITIQUE]',
    't.exp.nconst': 'AUCUNE coupure pour {outs} – l’appareil est ponté par le contact constant {bits} ; ces sorties '
                    'restent enclenchées. [ALARME CRITIQUE]',
    't.exp.off': '1) Coupées : {outs}',
    't.exp.sto': ' (variateurs : :SI.TorqueDisabled = 1)',
    't.exp.rest': '. Autres sorties inchangées.',
    't.exp.notoff': 'NE se couperont PAS : {effs} (branche OU avec {partners} – voir l’essai OU).',
    't.exp.disc': '2) {instr}.FP = 1 (défaut de discordance), O1 = 0 – coupures comme en 1) ; réarmement possible seulement après rétablissement des deux voies.',
    't.exp.disc_short': '2) {instr}.FP = 1 (défaut de discordance), O1 = 0.',
    't.exp.single': '2) Essai de discordance IMPOSSIBLE – les deux voies de l’instruction sur la même entrée. [ALARME CRITIQUE]',
    't.exp.xc_only': 'Un déclenchement isolé NE coupe AUCUNE sortie de sécurité ; {effs} ne se coupe(nt) qu’avec {partners} (branche OU) – voir l’essai de combinaison OU.',
    't.exp.none': 'Aucun effet sur les sorties de sécurité (l’appareil ne commande aucune sortie dans la SafetyTask) – confirmer l’intention de conception.',
    't.rst.manual': 'Appareil : réarmement MANUAL ({tag} [{rr}] ← {src}) ; sans réarmement O1 = 0.',
    't.rst.auto': 'Appareil : réarmement AUTOMATIC – O1 revient seul dès que la cause disparaît',
    't.rst.auto_estop': ' [ALARME : arrêt d’urgence]',
    't.rst.follow': 'Appareil : réarmement selon la configuration de l’instruction.',
    't.rs.rout': 'Sorties ROUT/CROUT ({outs}) : se réenclenchent seules après le réarmement de l’appareil (la sortie suit Enable).',
    't.rs.auto': 'Sorties {outs} : reviennent AUTOMATIQUEMENT avec {tags} [À VÉRIFIER].',
    't.rs.manual': 'Sorties ({n} : {outs}) : réarmement requis {resets}.',
    't.rs.follow': 'Sorties {outs} : suivent la logique.',
    't.rs.where': 'Sources de réarmement des sorties : feuille « Sorties ».',
    't.note.xb': 'Contournement par la commande std : {bits} – voir l’essai CONTOURNEMENT.',
    't.note.auto': 'Réarmement AUTO.',
    't.note.std': 'Voies issues de données standard – essai de discordance côté automate source.',
    't.or.act': '1) Déclenchez seulement {a}. 2) Déclenchez seulement {b}. 3) Déclenchez les deux en même temps.',
    't.or.exp': '1), 2) {outs} restent ENCLENCHÉES. 3) Coupées : {outs}.',
    't.or.rst': 'Comme dans les essais de fonction des deux appareils.',
    't.or.note': 'Branche parallèle OU – à confirmer avec l’appréciation du risque [À VÉRIFIER].',
    't.byp.act': 'Essai contrôlé, personne dans la zone : activez la condition qui met à 1 le bit {bit} ({src}), puis déclenchez l’appareil.',
    't.byp.exp': 'Selon le code : {outs} restent ENCLENCHÉES – la fonction est pontée par la commande standard. Après correction du programme : coupure comme dans l’essai de fonction.',
    't.byp.note': '[ALARME CRITIQUE] – voir le rapport de validation.',
    't.edm.act_neg': 'Sortie coupée (zone arrêtée), ouvrez le circuit de retour {fb} (simulation d’un contacteur soudé – pas de contact NF), puis réarmez les appareils et essayez d’enclencher.',
    't.edm.act_pos': 'Sortie coupée, pontez le retour {fb} (retour = 1 avec sortie coupée – simulation d’un contacteur soudé), puis réarmez les appareils et essayez d’enclencher.',
    't.edm.exp': '{tag}.FP = 1 (défaut EDM) ; les sorties {outs} NE s’enclenchent PAS.',
    't.edm.rst': 'Après suppression de la cause : réarmement du défaut {reset} [{rr}] ← {src}.',
    't.comm.what': 'Adaptateur {name} ({cat}, {addr}) – modules Safety I/O',
    't.comm.act': 'Débranchez le câble Ethernet de l’adaptateur {name} pendant le fonctionnement de la ligne.',
    't.comm.exp': 'Entrées de sécurité de l’adaptateur = 0 (état de connexion = défaut) → déclenchés : {ids}. Coupées : {outs}.',
    't.comm.rst': 'Après rétablissement de la connexion : les sorties restent coupées jusqu’au réarmement des appareils selon les essais de fonction.',
    't.comm.ref': 'Configuration E/S',
    't.comm.note': 'Détection au plus tard après l’Input CRTL des modules ({crtl}).',
    't.drv.id': 'Variateurs CIP Safety',
    't.drv.what': '{n} variateur(s) avec CIP Safety',
    't.drv.act': 'Pour chaque variateur : débranchez sa connexion réseau pendant le fonctionnement.',
    't.drv.exp': 'Le variateur passe en STO (perte de la connexion CIP Safety) ; :SI.ConnectionFaulted = 1 bloque le rung :SO.SafeTorqueOff là où il est utilisé.',
    't.drv.rst': 'Après rétablissement : le STO reste actif jusqu’au réarmement (front de réarmement + :SO.Reset).',
    't.drv.ref': 'Rungs STO ({routines})',
    't.summary': 'Synthèse',
    't.sum.count': 'Nombre d’essais',
    't.sum.open': 'Non réalisés',
    't.approve': 'Approbation du procès-verbal (nom, date, signature) :',
    't.done_by': 'Réalisé par', 't.checked_by': 'Vérifié par', 't.approved_by': 'Approuvé par',
    # ------------------------------------------------------------------ feuille Start
    's.subtitle': 'Matrice de causes et effets – GuardLogix {proc} {ver}, SafetyTask {period} ms, programme {src}',
    's.author': 'Auteur : {author}   •   Révision : {rev}   •   Date : {date}',
    's.lang_label': 'Langue',
    's.switch_hint': '◄ choisissez une langue dans la liste – toutes les feuilles basculent automatiquement',
    's.dict_note': 'Les textes proviennent de la feuille « {dict} » (les traductions peuvent y être corrigées ; une traduction vide affiche le texte anglais). '
                   'Les codes de la matrice (X, X1, XB, XC, XM, N, S…) et les tags du programme sont identiques dans toutes les langues.',
    's.sheet': 'Feuille', 's.contents': 'Contenu', 's.summary': 'Synthèse', 's.value': 'Valeur',
    's.sum.devices': 'Appareils d’entrée (causes)',
    's.sum.effects': 'Sorties de sécurité (effets) + signaux d’information',
    's.sum.cells': 'Croisements X / X1 / XB / XC / XM / N dans la matrice MOTOR',
    's.sum.alarm': '[ALARME CRITIQUE] – éléments du rapport',
    's.sum.dead': 'Éléments morts – éléments du rapport',
    's.sum.verify': '[À VÉRIFIER] – éléments du rapport',
    's.sum.tests': 'Essais dans le procès-verbal de validation',
}
