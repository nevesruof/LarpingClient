# Larp Client — sitio web

Landing + documentación de Larp Client, estilo zeta.ac. HTML/CSS/JS estático (sin frameworks), listo para Vercel.

## Subirlo a Vercel
1. Sube esta carpeta a un repo de GitHub.
2. En vercel.com → **Add New → Project** → importa el repo.
3. Framework Preset: **Other**. Build Command: vacío. Output Directory: vacío (la raíz).
4. Deploy. `vercel.json` ya activa las URLs limpias (`/docs/modules` en vez de `/docs/modules.html`) y la caché.

Con la CLI: `npm i -g vercel` y luego `vercel --prod` dentro de la carpeta.

## Antes de publicar
El cliente es privado: los botones dicen **"You are my friend?"** y llevan a la sección de acceso, donde
la gente te escribe para que les des el mod. En `site.config.json`:
- **contactUrl**: tu link de contacto (por ejemplo tu perfil de Discord `https://discord.com/users/TU_ID`
  o una invitación). Si está vacío se usa `discordUrl`; si ambos están vacíos el botón aparece sin link.
- **contactLabel**: el texto del botón (por defecto "Message Take").
- **discordUrl**: invitación a tu servidor. Si está vacío, los botones de Discord no aparecen.
- **siteUrl**: tu dominio final (se usa en las etiquetas para compartir en Discord/Twitter).

Después de cambiar `site.config.json` vuelve a generar:
```
python scripts/build.py
```

## Estructura
```
index.html            landing (generada)
404.html              página no encontrada (generada)
docs/*.html           documentación (generada, 17 páginas)
assets/css            site.css (landing y base) · docs.css
assets/js             site.js (menú interactivo, HUD arrastrable, cosméticos) · curtains.js (fondo de cortinas) · docs.js (búsqueda, filtro, índice)
assets/data           modules.json (sacado del código del mod) · search.json (índice de búsqueda)
assets/img            logo.svg · icons.svg (mismos íconos Material que el cliente) · cosmetics/ (renders reales) · og.jpg
assets/fonts          Inter (OFL)
scripts/              build.py · docs_build.py (contenido de las docs) · extract_modules.py · build_icons.py
```

## Cuando agregues módulos al cliente
```
python scripts/extract_modules.py <ruta>/larp-client/src/main/java/dev/larp/client assets/data/modules.json
python scripts/build.py
```
Eso actualiza el menú interactivo de la landing, los números y la referencia de módulos de las docs.
Para cambiar textos de las docs edita `scripts/docs_build.py`; para la landing, `scripts/build.py`.

## Créditos
Íconos Material (Apache 2.0), fuente Inter (SIL OFL 1.1), motor de cosméticos de Clarity (CC0).
