# 💼 Plateforme Comptable Autoentrepreneur

Gestion complète et intégrée de la comptabilité pour autoentrepreneur français.

## 🚀 Démarrage

1. **Ouvre le fichier** `comptabilite_autoentrepreneur.html` dans ton navigateur (double-clique)
2. **Aucune installation** — tout fonctionne en local (localStorage)
3. Les données persistent entre les sessions

## 📚 Modules

### 📄 Factures
Gère toutes tes factures clients et fournisseurs.

**Factures Clients (Ventes)**
- Enregistre tes factures de vente/prestation
- TVA collectée (que tu dois déclarer)
- Contribue au chiffre d'affaires

**Factures Fournisseurs (Achats)**
- Enregistre tes achats/charges
- TVA déductible (que tu peux récupérer)
- Réduit ta marge nette

**Champs pour chaque facture:**
- Type (client ou fournisseur)
- Date
- Numéro/référence (ex: FAC-001)
- Tiers (nom du client/fournisseur)
- Description
- Montant HT (€)
- TVA (%, par défaut 20%)

💡 **Astuce:** Les montants TTC s'affichent automatiquement.

### 🛡️ URSSAF - Cotisations Sociales

Calcule tes cotisations sociales (obligatoires en France).

**Taux par activité:**
- **Commerce / Vente:** 22%
- **Services / Libéral / Artisan:** 23.3%

**Comment ça marche:**
1. Sélectionne ta période (mois/année)
2. Choisis ton activité
3. Saisis ton chiffre d'affaires du mois
4. Clique « Calculer » → tu vois la cotisation

**Exemple:**
- CA du mois: 2 000€
- Activité: Services (23.3%)
- Cotisation URSSAF = 2 000€ × 23.3% = **466€ à payer**

💡 **Gestion:** Les cotisations sont calculées **mensuellement** mais payées généralement **trimestriellement**.

### 📋 TVA - Déclaration & Gestion

Gère et déclare ta TVA.

**Vocabulaire:**
- **TVA Collectée:** TVA que tu as facturé à tes clients (tu dois la reverser)
- **TVA Déductible:** TVA que tu as payée sur tes achats (tu peux la récupérer)
- **TVA Nette = TVA Collectée - TVA Déductible**

**Régimes TVA:**
- **Micro-entreprise:** déclaration simplifiée (pas remboursement de TVA)
- **Régime normal:** déclaration complète (récupération TVA déductible)

**Exemple calcul:**
| Item | Montant |
|------|---------|
| CA Clients (5 000€ @ 20%) | + 1 000€ TVA collectée |
| Charges Fournisseurs (2 000€ @ 20%) | - 400€ TVA déductible |
| **À payer à l'État** | **600€** |

### 📈 Tableau de Bord

**Cartes de synthèse:**
- CA ce mois
- Charges ce mois
- CA total année
- Nombre total de factures

**Factures ce mois:** nombre de factures clients/fournisseurs

**Statut fiscal:** 
- Ton régime (micro ou normal)
- CA année
- Marge brute
- Vérification du seuil micro-entreprise (72 600€)

### 📑 Rapports

Génère des rapports comptables.

**Types:**
- **Export mensuel:** détail du mois en cours
- **Export annuel:** synthèse de l'année

**Contient:**
- CA Clients (HT)
- Charges Fournisseurs (HT)
- Marge brute (CA - Charges)

💾 Bouton « Imprimer » pour PDF (utilise l'impression navigateur).

### ⚙️ Paramètres

Enregistre les infos de ton entreprise.

**Champs:**
- **Nom:** nom de ton business/SARL/EIRL
- **SIRET:** numéro SIRET (14 chiffres)
- **Email:** ton adresse de contact
- **Numéro TVA:** si applicable (optionnel)
- **Régime fiscal:** micro-entreprise ou régime normal

💾 **Enregistrer** pour sauvegarder.

🗑️ **Réinitialiser tout** supprime TOUTES les données (attention!).

---

## 📊 Cas d'Usage

### Cas 1: Freelance en Services

**Activité:** Services (23.3% URSSAF)

**Mois janvier:**
1. Crée une facture client: 3 000€ HT (client A)
2. Crée une facture client: 2 000€ HT (client B)
3. Crée une facture fournisseur: 500€ HT (logiciel SaaS)
4. Va dans URSSAF → calcule: 5 000€ CA → **1 165€ cotisation**
5. Va dans TVA → génère déclaration janvier:
   - TVA collectée: 5 000€ × 20% = 1 000€
   - TVA déductible: 500€ × 20% = 100€
   - **À payer: 900€**

### Cas 2: Micro-Entreprise Commerce

**Activité:** Commerce (22% URSSAF), seuil micro 72 600€/an

**Année en cours:**
1. Ajoute toutes les factures clients (revenu)
2. Ajoute les factures fournisseurs (stock, équipement)
3. Dashboard affiche:
   - CA annuel: 65 000€ ✓ (sous 72 600€)
   - Marge: 45 000€
4. Chaque mois:
   - Calcule cotisation URSSAF (22%)
   - Génère déclaration TVA trimestrielle

---

## 💾 Données & Stockage

**Où sont stockées tes données?**
- Stockage local (localStorage) du navigateur
- **Nunca uploaded** — reste sur ta machine
- Persiste même après fermeture du navigateur

**Sauvegarde:**
- Tes données se sauvent automatiquement
- Pour backup: **exporte un rapport**, ou copie le fichier `.html`

**Réinitialisation:**
- Onglet Paramètres → « Réinitialiser tout »
- Ou: efface les données du navigateur (`Ctrl+Shift+Del` → Données de site)

---

## ⚙️ Formules & Calculs

### TVA HT ↔ TTC
```
Montant TTC = Montant HT × (1 + Taux TVA / 100)
Montant TVA = Montant HT × (Taux TVA / 100)
```

### URSSAF Cotisation
```
Cotisation = Chiffre Affaires × Taux Activité
Exemple: 2 000€ × 23.3% = 466€
```

### Marge Brute
```
Marge = CA Clients - Charges Fournisseurs
```

### TVA Nette
```
TVA à Payer = TVA Collectée - TVA Déductible
(peut être négatif = crédit TVA)
```

---

## 🎯 Bonnes Pratiques

### Organisation des Factures
- **Numérotation:** FAC-001, FAC-002, ... (clients) et ACHAT-001 (fournisseurs)
- **Dates:** mets à jour systématiquement
- **Références:** garde cohérence avec tes emails/contrats

### TVA & URSSAF
- **Déclare mensuellement:** même si paiement trimestriel
- **Archive factures:** conservation légale 6 ans (France)
- **Justificatifs:** garde reçus/factures d'achat

### Périodicité
| Obligation | Fréquence |
|-----------|-----------|
| URSSAF | Mensuel (paiement trimestre/annuel) |
| TVA | Selon régime (mensuel, trimestriel, annuel) |
| Déclaration CA | Annuelle (avril) |
| Impôt sur le Revenu | Annuelle (mai) |

---

## ❓ FAQ

**Q: Je suis micro-entreprise, je dois payer TVA?**
A: Non, si tu as opté pour le régime de la franchise en base (standard). Tu ne déclares pas TVA mais tu ne peux pas la récupérer. La plateforme te permet de gérer "au cas où".

**Q: Comment imprimer un rapport?**
A: Va dans Rapports → génère → clique « Imprimer » → navigateur ouvre aperçu d'impression → Enregistrer en PDF.

**Q: Mes données vont disparaître?**
A: Non. localStorage persiste tant que tu n'effacesiras pas les données du site. Pour backup: exporte un rapport ou stocke une copie du fichier.

**Q: Puis-je changer de régime fiscal?**
A: Oui. Va dans Paramètres, change « Régime fiscal », puis enregistre. C'est utile si tu dépasses 72 600€ (obligation de passer en régime normal).

**Q: Qu'est-ce que le seuil 72 600€?**
A: Plafond de chiffre d'affaires annuel pour rester en micro-entreprise (France 2024). Au-delà: obligations du régime normal.

---

## 📞 Support & Limitations

**Limitations (par conception):**
- Aucun export vers logiciel comptable (pour intégration: créer version Python)
- Pas de remise de compte (signature numérique)
- Pas de bilan comptable avancé

**Pour aller plus loin:**
- Intégrer à un logiciel comptable pro (Sage, Ciel, etc.)
- Confier la comptabilité à un expert-comptable
- Utiliser plateforme web (Compta-Facile, Weedeye, etc.)

---

## 🛠️ Cas d'Amélioration Future

1. **Export CSV/PDF** pour intégration autres logiciels
2. **Multidevise** (€, $, £)
3. **Clients/Fournisseurs** récurrents (adresses enregistrées)
4. **Factures récurrentes** (abonnements)
5. **Graphiques** (CA trend, répartition charges)
6. **Synchronisation cloud** (Dropbox, Google Drive)
7. **Rappels** (deadline TVA, URSSAF)

---

## ✅ Vérification Complète

| Fonction | ✓ |
|----------|---|
| Gestion factures clients | ✓ |
| Gestion factures fournisseurs | ✓ |
| Calculs TVA (HT/TTC) | ✓ |
| Déclaration TVA (collectée/déductible) | ✓ |
| Calculs URSSAF (3 activités) | ✓ |
| Dashboard synthèse | ✓ |
| Rapports mensuels/annuels | ✓ |
| Stockage local | ✓ |
| Interface responsive | ✓ |
| Zéro serveur requis | ✓ |

---

**Créé pour les autoentrepreneurs français. Adapte aux règles locales de ton pays si applicable.**
