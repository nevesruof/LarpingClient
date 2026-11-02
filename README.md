# Larp Client website · 0.14.1

The original Larp website, updated in place. Its original landing layout, Inter typography, black/glass palette, rounded cards, curtains, tilted hero and loading-card preview are preserved.

## What changed

- The old menu illustration is replaced by the current client layout: category sidebar, separate profile panel, two-column module cards and lower search/actions bar.
- The interactive preview includes HUD, PvP, Utility, Visuals, Cosmetics, Kill Efects, Waypoints, Macros, Discord and Client settings.
- Existing product-preview tabs retain the HUD editor and cosmetic selector. Music & lyrics and Captures are added in the same tab system.
- Text, feature cards, requirements, release notes and guides reflect client 0.14.1, with 116 registered modules and NEW badges for recent additions.
- Discord identity is built in. The existing private-access contact remains unchanged.
- The HUD editor uses a real Minecraft night panorama, original item textures and the supplied player head. Its example target is FastL_ and the server is mc.hypixel.net. Keystrokes contains only actual keys.
- A gameplay gallery and interactive Shulker Preview/profile demonstrations extend the existing design. Mobile preview tabs scroll horizontally, and key animations pause while hidden or offscreen.
- The `larp.` wordmark is restored. The gallery starts with the supplied title screen and continues with the nighttime gameplay capture.
- Exclusive FAQs animate open and closed, including interrupted transitions and reduced-motion support. A compact release journal and shortcut links add navigation without changing the overall design.
- Captures uses an interactive recordings gallery demonstration instead of a screenshot poster. Saving a sample adds a local gallery row; it does not record or export media.

## Build and preview

No Node packages or framework installation are required. Python 3 builds the site:

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000`. For Vercel, the repository includes the generated pages and assets at its root: use framework **Other**, no install/build commands and output directory **.** (the root). The build also produces `dist/` for other static hosts. Regenerate before publishing source changes.

## Source structure

- `scripts/build.py`: original landing composition, common header/footer and static output.
- `scripts/menu_preview.py`: updated menu and new preview-tab markup.
- `assets/css/site.css`: original stylesheet, preserved unchanged.
- `assets/css/docs.css`: original documentation stylesheet, preserved unchanged.
- `assets/css/client-preview.css`: scoped styling for the current menu and added controls.
- `assets/js/site.js`: original tabs, draggable HUD and cosmetic selector; the obsolete menu renderer is removed.
- `assets/js/client-preview.js`: current menu, category navigation, local module toggles/settings, exclusive kill selection, profile/reset demonstrations and sample lyrics controls.
- `assets/js/curtains.js`: original visual effect, throttled and suspended offscreen or while the tab is hidden.
- `assets/data/modules.json`: current 116-module catalog extracted from the client source.
- `scripts/content_updates.py` and `scripts/docs_build.py`: current guides and searchable reference.
- `site.config.json`: version, requirements and existing contact.
- `scripts/website_details.py`, `assets/css/showcase.css` and `assets/js/showcase.js`: HUD assets, gallery and small interactive feature previews.
- `assets/js/faq.js` and `assets/js/captures-demo.js`: accessible FAQ transitions and the bounded local recording-gallery demonstration.

To refresh the catalog from client source:

```sh
python3 scripts/extract_modules.py PATH_TO_CLIENT/src/main/java/dev/larp/client assets/data/modules.json PATH_TO_CLIENT/src/main/resources/assets/larpclient/clarity/modules.json
python3 scripts/build.py
python3 scripts/validate.py
```

## Preview boundaries

The menu is a browser demonstration; its controls never change Minecraft settings or send game commands. Supplied gameplay screenshots and original cosmetic renders are real assets. Lyrics text is original sample copy. The capture demo only adds sample gallery entries and never records, plays or exports actual media.

Client desktop media features require Windows. Website previews do not establish client FPS or native capture compatibility.

## Credits

Material Icons (Apache 2.0), Inter (SIL OFL), Clarity cosmetic renders (CC0), and gameplay screenshots and player head supplied by the project owner. Vanilla Minecraft item textures and panorama © Mojang Studios / Microsoft, sourced through [MC Assets](https://mcasset.cloud/1.21.11/assets/minecraft/textures). See `assets/img/minecraft/CREDITS.md`. Not affiliated with Mojang or Microsoft.
