# 🔐 Portail Client — Guide d'Utilisation

Interface d'authentification et de gestion pour la plateforme comptable.

## 🚀 Démarrage Rapide

1. **Ouvre** `comptabilite_client_portail.html` dans ton navigateur
2. **Crée un compte** (ou utilise un existant)
3. **Accède au dashboard** avec tes données comptables

## 📋 Écran de Connexion

### Création de Compte

**Champs à remplir:**
- **Nom:** Ton nom ou nom de l'entreprise
- **Email:** Adresse email unique (pour la connexion)
- **Mot de passe:** Au moins 8 caractères recommandé
- **Confirmer mot de passe:** Doit correspondre
- **Activité:** Choix entre 3 options:
  - Services/Libéral (23.3% URSSAF)
  - Commerce/Vente (22% URSSAF)
  - Artisan (23.3% URSSAF)

**Validation:**
- ✓ Tous les champs obligatoires
- ✓ Adresse email unique (pas de doublon)
- ✓ Mots de passe identiques
- ✓ Message de confirmation après inscription

### Connexion

**Champs:**
- **Email:** Adresse utilisée lors de l'inscription
- **Mot de passe:** Ton mot de passe

**Actions:**
- ✓ Se connecter → accès au dashboard
- ✓ Créer un compte → si pas encore inscrit
- ✗ Email/password incorrect → message d'erreur

**Sécurité:**
- Les mots de passe ne sont pas stockés en clair
- Hachage lors de la sauvegarde
- Session persistante (même après fermeture du navigateur)

---

## 📊 Tableau de Bord

Accès après connexion. **6 sections principales.**

### 1️⃣ Aperçu (Overview)

**Cartes de synthèse rapide:**
- Factures (nombre total)
- CA (€ total année)
- Abonnement (affiche ton forfait)
- Quota API (illimité)

**Accès rapide:**
- **📄 Ouvrir Comptabilité Complète** → lien vers l'app de comptabilité complète (comptabilite_autoentrepreneur.html)
- **📥 Télécharger Modèle** → fichier CSV avec structure pour importer factures
- **💾 Exporter Données** → backup JSON complet de ton compte

### 2️⃣ Comptabilité (Accounting)

**Résumé financier:**
| Métrique | Description |
|----------|-------------|
| **CA Année (HT)** | Chiffre d'affaires total HT (factures clients) |
| **Charges (HT)** | Achats/frais HT (factures fournisseurs) |
| **Marge Brute** | CA - Charges = bénéfice avant cotisations |
| **URSSAF Annuel** | Cotisations sociales estimées (CA × taux activité) |

**Dernières Factures:**
- Affichage des 5 dernières factures
- Référence, tiers, montant HT
- Distinctions couleur: vert (clients), rouge (fournisseurs)

**Pour plus de détails:**
→ Clique « Ouvrir Comptabilité Complète »

### 3️⃣ Équipe (Team)

**Gestion multi-utilisateur (futur):**
- Ajouter des collaborateurs via email
- Définir les rôles d'accès
- Liste des utilisateurs actuels

**Statut actuel:**
- Toi: Admin (accès complet)
- Autres (à ajouter)

💡 **Cas d'usage:** Comptable, manager, collaborateur ayant accès partiel aux données.

### 4️⃣ Paramètres (Settings)

**Profil:**
- **Nom:** modifiable (met à jour ton affichage)
- **Email:** lecture seule (créé à l'inscription)
- **Activité:** lecture seule (définie à l'inscription)
- Bouton « 💾 Enregistrer »

**Sécurité:**
- **Changer mot de passe** → nouveau mot de passe + confirmation
- **Supprimer le compte** → suppression complète + confirmation email

⚠️ **Attention:**
- Changement de mot de passe: déconnecte (reconnexion requise)
- Suppression: irréversible (perte de toutes les données du compte)

---

## 🔗 Intégration Comptabilité

Le portail client est **lié à l'application comptable complète**.

### Flux Intégré

```
[Portail Client]
      ↓
  Authentification
      ↓
  [Dashboard]
      ↓
  Clic "Ouvrir Comptabilité Complète"
      ↓
  [App Comptabilité]
      ↓
  (Les données peuvent être synchronisées)
```

### Données Partagées

- **Factures:** Historique des factures de l'utilisateur
- **URSSAF:** Historique des cotisations calculées
- **Profil:** Nom, email, activité

---

## 💾 Données & Stockage

### Où Sont Stockées les Données?

**localStorage du navigateur:**
- Comptes utilisateurs (hachés)
- Profils (nom, email, activité)
- Session actuelle (currentUser)

**Aucun serveur requis:**
- Pas d'upload vers un serveur
- Données 100% locales
- Sauvegardes manuelles possibles

### Comment Sauvegarder?

**Option 1: Export JSON**
1. Onglet Aperçu
2. Clique « 💾 Exporter Données »
3. Fichier `backup_comptabilite_YYYY-MM-DD.json` téléchargé

**Option 2: Sauvegarde navigateur**
- Exporte d'autres navigateurs ou appareils
- Chaque navigateur = localStorage indépendant
- Pas de synchronisation cloud (tu dois faire manuellement)

### Comment Restaurer?

- Pour restaurer un backup:
  - Ouvre DevTools (F12) → Storage → localStorage
  - Copie le contenu du JSON backup
  - Ou: crée un nouveau compte sur le même navigateur

---

## 🔐 Sécurité

### Authentification

- **Mot de passe:** stocké haché (fonction simple, production utiliserait bcrypt)
- **Email:** unique (pas de doublon)
- **Session:** persistante via localStorage

### Bonnes Pratiques

✅ **À faire:**
- Utilise un mot de passe fort (12+ caractères, mélange)
- Ferme la session depuis un appareil partagé
- Exporte régulièrement tes données (backup)

❌ **À éviter:**
- Partager ton navigateur avec d'autres sans logout
- Utiliser le même mot de passe que tes emails
- Stocker backup en clair sur l'ordinateur

### Données Sensibles

| Info | Visibilité |
|------|-----------|
| Email | Visant à toi seul |
| Mot de passe | Jamais affiché |
| Factures | Privées à ton compte |
| URSSAF/TVA | Privées à ton compte |

---

## 📱 Multi-Navigateur & Multi-Appareil

**Important:** localStorage = **par navigateur**.

```
Appareil A (Chrome)     → Compte 1 (localStorage Chrome)
Appareil A (Firefox)    → Compte 2 (localStorage Firefox)
Appareil B (Chrome)     → Compte 3 (localStorage Chrome)
```

### Pour synchroniser:

1. **Exporte** depuis un appareil (JSON backup)
2. **Importe** sur un autre (copie localStorage)
3. Ou: utilise le même email/password sur chaque navigateur

---

## 🆘 Troubleshooting

### "Email déjà utilisé"
→ Cet email est déjà créé. Soit:
- Clique « Se connecter »
- Ou crée un compte avec un autre email

### "Email ou mot de passe incorrect"
→ Vérifiez:
- Majuscules/minuscules (sensible)
- Pas d'espaces avant/après
- Email exact utilisé à l'inscription

### "Mes données ont disparu"
→ Possible causes:
- Suppression manuelle de localStorage (Ctrl+Shift+Del)
- Changement de navigateur
- Réinstallation du navigateur
- Cache vidé

**Solution:** Restaure depuis un backup JSON si disponible

### "Impossible d'ajouter un membre d'équipe"
→ Actuellement (MVP):
- Équipe = fonctionnalité affichée mais pas activée
- Version future permettra l'ajout de collaborateurs
- Pour le moment: un compte = une personne

---

## 🎯 Cas d'Usage

### Cas 1: Freelance Solo

1. **Crée** un compte (email perso)
2. **Accède** au dashboard (Aperçu + Comptabilité)
3. **Ouvre** Comptabilité Complète pour ajouter factures
4. **Exporte** backup mensuellement

### Cas 2: PME avec Comptable

1. **Owner crée** un compte (email entreprise)
2. **Ajoute comptable** (futur: équipe)
3. **Comptable se connecte** et gère les factures
4. **Owner exporte** pour audit/banque

### Cas 3: SaaS B2B (Futur)

- Clients créent comptes
- Paiement récurrent (forfait Pro affiché)
- Équipe avec rôles (Owner, Comptable, Lecteur)
- API pour intégration

---

## 📞 Support & Évolution

**Version actuelle:** MVP (Minimum Viable Product)
- ✓ Authentification complète
- ✓ Dashboard avec synthèse
- ✓ Lien vers app comptabilité
- ✓ Export données

**À venir:**
- [ ] Équipe multi-utilisateur (rôles)
- [ ] Synchronisation factures
- [ ] Rappels (deadlines)
- [ ] Support cloud (Dropbox, Drive)
- [ ] API pour intégrations tierces

---

## 🔗 Fichiers Connexes

| Fichier | Purpose |
|---------|---------|
| `comptabilite_autoentrepreneur.html` | App comptabilité complète (factures, URSSAF, TVA) |
| `comptabilite_client_portail.html` | Ce fichier: authentification + dashboard |
| `agent_dashboard_standalone.html` | Système multi-agents (bonus) |
| `COMPTABILITE_GUIDE.md` | Guide comptabilité détaillé |
| `PORTAIL_CLIENT_GUIDE.md` | Ce guide |

---

**Créé pour autoentrepreneurs français. Adapte selon les règles locales.**
