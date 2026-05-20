---
hide:
  - navigation
  - toc
  - footer
---

<div class="page-headers">
<h1>Buenas Primeras Lineas </h1>
</div>

Mapea tu primera linea! Estas coordenadas apuntan hacia lines electricas faciles de mapear para principiantes. También puedes añadir "buenas primeras líneas" [abajo de la pagina web](#quieres-anadir-una-buena-linea).

??? success "INTRODUCCION (Haz clic)"
    Bienvenido a nuestra plataforma interactiva y centro de contribución a «buenas primeras líneas» a través de OpenStreetMap! Haga clic en el cuadro «buenas primeras líneas» que prefiera y comience a cartografiar la infraestructura electrica directamente en iD o JOSM :rocket:
    Si es tu primera mapeando, explora nuestro tutorial [JOSM Starter-Kit](https://mapyourgrid.org/starter-kit/#josm-starter-kit) or [iD Starter-Kit](https://mapyourgrid.org/starter-kit/#id-starter-kit). Puedes usar el hashtag **#MapYourGrid** en tus cambios para apoyar la inciativa! 

    Como usar: <br>
    1. Pulsa en una des la lineas<br>
    2. Si utilizas iD, pulsa el botón del editor de iD, que abrirá directamente una página de edición en iD y te teletransportará a la ubicación de esa línea.<br>
    3. Si utilizas JOSM, asegúrate de que «Remoto» esté activado y de que tu bloqueador de anuncios esté desactivado. Pulsa el botón JOSM y ve a JOSM. Serás teletransportado a la primera línea correcta. Sin embargo, el país no se cargará, pero puedes hacerlo utilizando nuestro Map It 📍 para ese país o región.<br>
    4. Una vez que hayas terminado el mapeo, vuelve a esta página y al cuadro de tu primera línea correcta, y haz clic en «completado» si lograste terminar la línea, o en «intentado» si lo intentaste pero no lo lograste.




<div id="gfl-container">
  <div id="loading">Loading good first lines...</div>
</div>

### **<div class="tools-header">Quieres añadir una buena linea?</div>**

<div id="add-gfl-form">
  <div class="form-group">
    <label for="add-coordinates">Coordenadas *</label>
    <input type="text" id="add-coordinates" placeholder="" required>
    <small>Latitud,Longitud (ejemplo: 43.22443,12.82870)</small>
  </div>
  
  <div class="form-group">
    <label for="add-country">País (en Ingles) *</label>
    <input type="text" id="add-country" placeholder="" required>
    <small>Ejemplo: Spain</small>
  </div>
  
  <div class="form-group">
    <label for="add-details">Region/Detalles (Opcional)</label>
    <input type="text" id="add-details" placeholder="" maxlength="200">
    <small>Ejemplo: "Madrid Region", "Linea sube"</small>
  </div>
  
  <button id="submit-gfl" class="submit-btn">Añadir Buena Primera Linea</button>
  <div id="form-message"></div>
</div>

## *Líneas archivadas*

[Líneas archivadas :fontawesome-solid-paper-plane:](archive/archive.md){ .md-button .md-button--primary }

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="/assets/javascripts/gfl.js"></script>
