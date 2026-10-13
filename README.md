# github-slideshow

Presentación de diapositivas publicada con GitHub Pages: un sitio estático
generado por **Jekyll** que renderiza las diapositivas con **reveal.js 3.9.2**.

- Cada diapositiva es un archivo Markdown en [`_posts/`](_posts/).
- El orden lo da la fecha del nombre del archivo: **la más antigua va primera**.
- El sitio se publica desde la rama `master`.

## Si no programas

Lee **[GUIA-RAPIDA.md](GUIA-RAPIDA.md)**. Son seis frases que puedes escribirle
a Claude Code para crear, revisar y publicar diapositivas sin tocar código:

| Comando | Qué hace |
|---|---|
| `/nueva-presentacion <tema>` | Crea una presentación completa desde cero |
| `/nueva-slide <idea>` | Añade una diapositiva |
| `/vista-previa` | Muestra una imagen de cada diapositiva |
| `/verificar` | Comprueba que todo está sano antes de publicar |
| `/publicar` | Guarda y sube los cambios |
| `/traducir-deck <idioma>` | Traduce la presentación entera |

## Si trabajas en el repositorio

```sh
script/setup        # instala las gemas en vendor/bundle
script/cibuild      # compila y valida enlaces
script/screenshots  # genera un PNG por diapositiva en .preview/
script/server       # servidor local en http://localhost:4000
```

Una diapositiva es un archivo `_posts/AAAA-MM-DD-slug.md` con este
encabezado:

```markdown
---
layout: slide
title: "Título de la diapositiva"
---

Contenido en Markdown. Una idea por diapositiva.
```

> ⚠️ **Nunca uses una fecha futura.** `_config.yml` tiene `future: false`, así
> que una diapositiva fechada mañana no se publica **y el build no da ningún
> error**. Un hook de Claude Code y el CI lo comprueban automáticamente.

Las reglas completas del proyecto están en [CLAUDE.md](CLAUDE.md), y las de
autoría de diapositivas en
[`.claude/skills/presentaciones/`](.claude/skills/presentaciones/SKILL.md).

## Créditos

Construido sobre [reveal.js](https://github.com/hakimel/reveal.js) de Hakim El
Hattab. El repositorio partió de la plantilla `github-slideshow` de GitHub
Training.
