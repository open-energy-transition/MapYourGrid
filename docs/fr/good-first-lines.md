---
hide:
  - navigation
  - toc
  - footer
---

<div class="page-headers">
<h1>Bonnes Premieres Lignes </h1>
</div>

Cartographie ta premiere ligne! Ces coordonnées pointent vers des lignes electriques faciles à cartographier pour les débutants. Tu peux aussi rajouter des "bonnes premieres lignes" [en bas de la page](#rajouter-une-ligne).

??? success "INTRODUCTION (Cliquer)"
    Bienvenue sur notre plateforme interactive et centre de contribution aux « bonnes premières lignes » via OpenStreetMap ! Cliquez sur la case « bonnes premières lignes » de votre choix et commencez à cartographier l'infrastructure électrique directement dans iD ou JOSM. :rocket:
    Si tu es un débutant, explore notre tutoriel [JOSM Starter-Kit](https://mapyourgrid.org/starter-kit/#josm-starter-kit) ou [iD Starter-Kit](https://mapyourgrid.org/starter-kit/#id-starter-kit). Tu peux aussi utiliser notre hashtag **#MapYourGrid** pour  soutenir l'initiative! 

    Comment utiliser: <br>
    1. Cliquez sur l'une des lignes.<br>
    2. Si vous utilisez iD, appuyez sur le bouton de l'éditeur iD, qui ouvrira directement une page d'édition dans iD et vous téléportera à l'emplacement de cette ligne..<br>
    3. Si vous utilisez JOSM, assurez-vous que l'option 'Controle à distance' est activée et que votre bloqueur de pub est désactivé. Cliquez sur le bouton JOSM et accédez à JOSM. Vous serez redirigé vers la première ligne correcte. Cependant, le pays ne se chargera pas, mais vous pouvez le faire en utilisant notre outil Map It 📍 pour ce pays ou cette région.<br>
    4. Une fois que vous avez terminé le mappage, revenez à cette page et à la case de votre première ligne correcte, puis cliquez sur « terminé » si vous avez réussi à terminer la ligne, ou sur « essayé » si vous avez essayé mais sans succès.




<div id="gfl-container">
  <div id="loading">Loading good first lines...</div>
</div>

### **<div class="tools-header">Rajouter une ligne</div>**

<div id="add-gfl-form">
  <div class="form-group">
    <label for="add-coordinates">Coordonnées *</label>
    <input type="text" id="add-coordinates" placeholder="" required>
    <small>Latitude,Longitude (exemple: 43.22443,12.82870)</small>
  </div>
  
  <div class="form-group">
    <label for="add-country">Pays (en anglais) *</label>
    <input type="text" id="add-country" placeholder="" required>
    <small>Exemple: Spain</small>
  </div>
  
  <div class="form-group">
    <label for="add-details">Region/Details (Optionnel)</label>
    <input type="text" id="add-details" placeholder="" maxlength="200">
    <small>Exemple: "Madrid Région", "Ligne descend"</small>
  </div>
  
  <button id="submit-gfl" class="submit-btn">Ajouter Bonne Premiere Ligne</button>
  <div id="form-message"></div>
</div>

## *Lignes archivées*

[Lignes archivées :fontawesome-solid-paper-plane:](archive/archive.md){ .md-button .md-button--primary }

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="/assets/javascripts/gfl.js"></script>