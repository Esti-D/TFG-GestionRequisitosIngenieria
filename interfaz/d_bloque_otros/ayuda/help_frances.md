## Aide pour le logiciel RM Requirements Management

### Index
- [Téléchargement des documents dans la base de données](#téléchargement-des-documents-dans-la-base-de-données)
- [Requêtes](#requêtes)
- [Autres](#autres)
- [Paramètres](#paramètres)
- [Aide](#aide)

---

### Téléchargement des documents dans la base de données
1. À l'aide du bouton **Sélectionner un fichier** (qui ouvre l'explorateur de fichiers), choisissez le fichier PDF contenant les exigences. Il apparaîtra dans la fenêtre du visualiseur. Ensuite, démarrez le processus en appuyant sur le bouton **CHARGER**.

   1.1. **Reconnaissance de la hiérarchie des chapitres** : Les modèles qu'il reconnaît sont :  
        - `1.`
        - `1`
        - `1-`
        - `1)`

   1.2. **Modèles non reconnus** :  
        - 1. En cas de non-reconnaissance, l'option recommandée est **Modifier**, ce qui implique de convertir le PDF en un format modifiable à l'aide d'un logiciel externe pour incorporer l'un des modèles reconnus et gérer le document.  
        - 2. L'autre option disponible est **Forcer**. Dans ce mode, tout le document sera traité comme un seul chapitre, et toutes les exigences seront au même niveau hiérarchique.  

   1.3. **Modèles reconnus ou forcés** : Une fenêtre apparaîtra pour sélectionner le projet auquel vous souhaitez ajouter les exigences.

2. Une fois le projet sélectionné, confirmez pour continuer. Le processus de téléchargement sera terminé, affichant le contenu et permettant des modifications (si vous souhaitez corriger ou supprimer quelque chose).
3. Le système analysera la portée potentielle des sous-systèmes et proposera ceux qui pourraient être affectés. Vous pouvez en sélectionner quelques-uns ou tous, selon le cas.

À la fin, les exigences/document seront stockés et liés au projet et aux sous-systèmes correspondants.

---

### Requêtes
1. Vous pouvez rechercher des **documents**, **projets**, **sous-systèmes** et **exigences** (textes et tableaux/figures) en sélectionnant l'option souhaitée.
2. Pour répertorier tous les éléments, appuyez simplement sur le bouton **Requête**.
3. Pour effectuer une recherche spécifique, utilisez les filtres pour **Documents**, **Projets** et **Sous-systèmes**.
   - Vous pouvez appliquer un seul filtre ou les combiner. Par exemple, vous pouvez sélectionner les documents d'un projet spécifique et d'un seul sous-système.  
   - Les exigences affichées seront toujours issues de la dernière version du document, s'il en existe plusieurs.  
   - Vous pouvez supprimer un fichier directement depuis le visualiseur de requêtes ; cette option supprimera en cascade les exigences du document.  
   - Vous pouvez également supprimer les tableaux/images d'exigences depuis le visualiseur.

---

### Autres
1. **Projets** :  
   - Vous pouvez ajouter de nouveaux projets à la base de données pour leur attribuer des documents et des exigences.  
   - Le critère recommandé est d'utiliser le nom de la ville où le projet sera développé.  
   - Vous pouvez également supprimer des projets.
2. **Sous-systèmes** :  
   - Vous pouvez ajouter de nouveaux sous-systèmes à la base de données.  
   - Pour qu'un sous-système soit reconnu dans l'analyse de la portée d'un document/exigence, ses mots-clés doivent être inclus dans le fichier associé `TOKENES.csv`.  
   - Vous pouvez également supprimer des sous-systèmes.
3. **Attribuer** :  
   - Cette option vous permet de créer des relations entre documents et sous-systèmes après le téléchargement du document.  
   - Elle est conçue pour les cas où vous devez associer un document à un autre sous-système ultérieurement.  
   - Vous pouvez également supprimer des associations.

---

### Paramètres
1. Vous pouvez choisir la langue dans laquelle vous souhaitez travailler avec cette application. Cette version prend en charge le **français**, **anglais** et **espagnol**.

---

### Aide
1. Explication de chacune des options disponibles dans cette version du logiciel.
