# **PSN Unfriender**

A Python script to manage your PlayStation Network (PSN) friend list efficiently by automatically removing friends that do not match specific patterns.

---

## **English**

### **Overview**
The PSN Unfriender script helps you clean up your friend list on PlayStation Network by:
- Authenticating using an `npsso_token`.
- Fetching your friend list.
- Allowing you to keep specific friends based on patterns in their usernames.
- Removing the rest automatically.

---

### **Features**
- **Pattern Matching**: Keep only the friends whose usernames match your custom-defined patterns.
- **Rate Limit Handling**: Automatically detects API rate limits and stops execution.
- **Clear Output**: Provides a well-organized and color-coded summary of actions.

---

### **Installation**

1. **Retrieve your `npsso_token`:**
   - Log into the [PlayStation website](https://www.playstation.com/).
   - Visit the following URL: [Sony SSO Cookie API](https://ca.account.sony.com/api/v1/ssocookie).
   - Copy the `npsso` token and save it for later.

2. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/psn-unfriender.git
   cd psn-unfriender
   ```

3. **Update `configuration.json`**:
   Add your `npsso_token` and define patterns for usernames you want to keep.

   Example `configuration.json`:
   ```json
   {
     "npsso_token": "YOUR_TOKEN_HERE",
     "nameWhitelistPatterns": [
       ".*Warrior.*",
       ".*Wicked.*"
     ]
   }
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the script**:
   ```bash
   python unfriender.py
   ```

---

### **Usage**

#### **Configuration Options**
- Add patterns in the `nameWhitelistPatterns` field of the `configuration.json` file to specify which friends to keep.
- Example:
   If you want to keep all friends whose usernames include the words "Warrior" or "Wicked":
   ```json
   {
     "nameWhitelistPatterns": [
       ".*Warrior.*",
       ".*Wicked.*"
     ]
   }
   ```

---

### **Example Output**
```plaintext
Found 12 friends

Friends to remove (9): 
FierceChampion42
MightyDragon99
RadiantPhoenix48
DaringSorcerer64
DaringTitan45
MysticNinja42
VividLegend82
DaringPhoenix41
VividSamurai69

Friends to keep (3): 
WickedNinja30
WickedDragon84
FierceWarrior92
```

---

### **Known Limitations**
- The PlayStation API may enforce rate limits of **300 requests per 20 minutes**. The script handles this by stopping when limits are hit.
- Usernames are case-sensitive when matched against patterns.

---

## **Français**

### **Présentation**
Le script PSN Unfriender permet de gérer efficacement votre liste d'amis sur le PlayStation Network en :
- S'authentifiant via un `npsso_token`.
- Récupérant votre liste d'amis.
- Permettant de conserver uniquement certains amis en fonction de critères définis.
- Supprimant automatiquement les autres.

---

### **Fonctionnalités**
- **Filtrage par motifs** : Gardez uniquement les amis dont les noms d'utilisateur correspondent à vos motifs personnalisés.
- **Gestion des limites API** : Le script détecte automatiquement les limites imposées par l'API et arrête son exécution.
- **Sortie claire et colorée** : Fournit un résumé bien organisé des actions.

---

### **Installation**

1. **Obtenez votre `npsso_token`** :
   - Connectez-vous sur le [site PlayStation](https://www.playstation.com/fr-fr/).
   - Visitez cette URL : [Sony SSO Cookie API](https://ca.account.sony.com/api/v1/ssocookie).
   - Copiez le token `npsso` et conservez-le.

2. **Clonez ce dépôt** :
   ```bash
   git clone https://github.com/your-username/psn-unfriender.git
   cd psn-unfriender
   ```

3. **Modifiez le fichier `configuration.json`** :
   Ajoutez votre `npsso_token` et définissez les motifs des noms à conserver.

   Exemple `configuration.json` :
   ```json
   {
     "npsso_token": "VOTRE_TOKEN_ICI",
     "nameWhitelistPatterns": [
       ".*Warrior.*",
       ".*Wicked.*"
     ]
   }
   ```

4. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

5. **Lancez le script** :
   ```bash
   python unfriender.py
   ```

---

### **Options de Configuration**
- Ajoutez des motifs dans le champ `nameWhitelistPatterns` du fichier `configuration.json` pour spécifier les amis à conserver.
- Exemple :
   Si vous souhaitez garder tous les amis dont les noms incluent "Warrior" ou "Wicked" :
   ```json
   {
     "nameWhitelistPatterns": [
       ".*Warrior.*",
       ".*Wicked.*"
     ]
   }
   ```

---

### **Exemple de Sortie**
```plaintext
12 amis trouvés

Amis à supprimer (9) : 
FierceChampion42
MightyDragon99
RadiantPhoenix48
DaringSorcerer64
DaringTitan45
MysticNinja42
VividLegend82
DaringPhoenix41
VividSamurai69

Amis à garder (3) : 
WickedNinja30
WickedDragon84
FierceWarrior92
```

---

### **Limitations Connues**
- L'API PlayStation impose une limite de **300 requêtes par 20 minutes**. Le script gère cette contrainte en arrêtant l'exécution lorsqu'elle est atteinte.
- Les noms d'utilisateur sont sensibles à la casse lors de la correspondance des motifs.

---

### **Contributions**
Les contributions sont les bienvenues ! Ouvrez une *issue* ou soumettez une *pull request* pour proposer des améliorations ou corriger des bugs.

---

### **License**
Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT). Vous êtes libre de l'utiliser, le modifier et le distribuer.
