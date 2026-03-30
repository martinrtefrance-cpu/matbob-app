# ⚡ Application de Gestion des Demandes Matériel

Application Streamlit pour visualiser, filtrer et gérer les demandes de matériel réseau.

---

## 📁 Architecture du projet

```
app/
├── app.py              # Application principale (toutes les pages)
├── utils.py            # Fonctions utilitaires (chargement, sauvegarde, requêtes)
├── requirements.txt    # Dépendances Python
├── README.md           # Ce fichier
└── data/
    ├── BDD.xlsx        # Base de données principale (ne pas supprimer)
    └── demandes.xlsx   # Généré automatiquement lors des premières demandes
```

---

## 🚀 Lancer l'application

### 1. Prérequis

- Python 3.9 ou supérieur
- pip

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application

Depuis le dossier `app/` :

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à l'adresse :
**http://localhost:8501**

---

## 📄 Pages de l'application

| Page | Description |
|------|-------------|
| 📊 Dashboard | Graphiques de synthèse : sites, programmes, BIS, MES, PLQF |
| 🗄️ Base de données | Tableau filtrable avec export CSV/Excel |
| ✏️ Demandes | Formulaire de demande de modification ou suppression |
| 🔐 Administration | Validation/refus des demandes (mot de passe requis) |

---

## 🔐 Mot de passe admin

Le mot de passe par défaut est : **`admin1234`**

Pour le modifier, éditez la variable `ADMIN_PASSWORD` dans `app.py` :

```python
ADMIN_PASSWORD = "votre_nouveau_mot_de_passe"
```

---

## 🔧 Fonctionnement du système de demandes

1. Un utilisateur va sur la page **Demandes**, sélectionne une ligne et décrit la modification souhaitée.
2. La demande est enregistrée dans `data/demandes.xlsx` avec le statut **"En attente"**.
3. L'admin se connecte sur la page **Administration**, consulte les demandes et accepte ou refuse.
4. Si **acceptée** : la base de données `BDD.xlsx` est mise à jour automatiquement.
5. Si **refusée** : aucune modification n'est apportée.

### Format des modifications

Pour une demande de **modification**, utilisez le format suivant (une modification par ligne) :

```
Colonne: nouvelle valeur
CRPT: Lyon
Affectation PLQF: Siemens
Type de BIS: 63-30
```

---

## 📊 Graphiques disponibles

- Nombre de demandes par site (CRPT)
- Répartition par programme industriel
- Demandes par type de BIS
- Répartition par sous-politique
- Évolution des mises en service (MES PFM1)
- Répartition Huile / Air
- Affectation PLQF par fournisseur
