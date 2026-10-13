---
name: presentaciones
description: Reglas completas para crear, editar, ordenar y publicar diapositivas en este repositorio (Jekyll + reveal.js). Úsala siempre que la tarea implique tocar archivos de _posts/, cambiar el tema o los estilos de la presentación, ajustar transiciones o fondos de reveal.js, cambiar el orden de las diapositivas, o publicar el deck en GitHub Pages.
---

# Autoría de diapositivas en `github-slideshow`

## Cómo se convierte un archivo en diapositiva

`index.html` recorre `site.posts reversed` e incluye `_includes/slide.html` por
cada post. Es decir: **cada archivo de `_posts/` es exactamente una diapositiva**,
y el orden lo determina la fecha del nombre del archivo, de la más antigua a la
más reciente.

```
_posts/0000-01-01-intro.md   → diapositiva 1
_posts/0001-01-01-que-es.md  → diapositiva 2
_posts/0001-01-02-como.md    → diapositiva 3
```

## Plantilla mínima

```markdown
---
layout: slide
title: "Título visible"
---

Contenido en Markdown.
```

## Las cuatro trampas de este repositorio

1. **Fechas futuras = diapositiva invisible.** `_config.yml` tiene
   `future: false`. Una diapositiva fechada mañana simplemente no se publica, y
   el build **no da error**. Es el fallo más frecuente y el más difícil de
   detectar. Usa siempre la fecha de hoy o anterior.

2. **Fechas duplicadas = orden impredecible.** Dos archivos con el mismo
   `AAAA-MM-DD` quedan en un orden que Jekyll no garantiza. Cada diapositiva
   necesita su propia fecha.

3. **Formato del nombre.** Sin el patrón `AAAA-MM-DD-slug.md`, Jekyll ni
   siquiera considera el archivo un post: desaparece sin avisar.

4. **`baseurl` está comentado a propósito** en `_config.yml` (commit `f3d6e95`).
   Si lo reactivas, los CSS y JS de reveal.js dejan de cargar en GitHub Pages.

## Estrategia de fechas recomendada

Para un deck nuevo, usa una base antigua y **saltos de 10 días**, para que
siempre quede hueco donde intercalar. Deja `0000-01-01` para la portada si
quieres que vaya primera:

```
0000-01-01-portada.md
0001-01-01-contexto.md
0001-01-11-problema.md
0001-01-21-solucion.md
0001-01-31-datos.md
0001-02-10-cierre.md
```

Para **insertar** entre dos diapositivas, usa una fecha intermedia libre
(entre `0001-01-11` y `0001-01-21` caben nueve). Si no queda hueco, renumera
las siguientes: las fechas solo ordenan, no se muestran, así que renumerar no
cuesta nada.

> ⚠️ **No uses la clave `date:` del front matter para intercalar.** Es cierto
> que gana a la fecha del nombre, pero con el esquema de años `0001` que usa
> este deck Jekyll resuelve mal esas fechas: la `timezone: Europe/Berlin` de
> `_config.yml` arrastra el desfase horario histórico (+00:53) y el salto
> juliano/gregoriano, de modo que `date: 0001-01-02 12:00` aterriza en
> `0000-12-31` y la diapositiva **salta al principio del deck**. Comprobado
> ejecutando el build. Con años modernos sí funciona, pero no es el caso aquí.
>
> Además, dos archivos con el mismo prefijo `AAAA-MM-DD` los rechazan el hook
> y el CI, así que el archivo intercalado necesita igualmente una fecha libre
> en el nombre.

## Front matter soportado

Definido por `_includes/slide.html`:

| Clave | Efecto |
|---|---|
| `layout: slide` | **Obligatorio.** |
| `title: "..."` | Encabezado `<h1>`. Con `""` no se muestra encabezado. |
| `slide-id: mi-ancla` | Pone `id="mi-ancla"` en la `<section>`, para enlazar directo. |
| `classes: [a, b]` | Añade clases CSS a la `<section>`. Sin esta clave se usa `slide`. |
| `data: {clave: valor}` | Se convierte en atributos `data-clave="valor"` de reveal.js. |
| `date: ...` | Sobrescribe la fecha del nombre. **Evítala** (ver el aviso de arriba): con años `0001` ordena mal, y si es futura la diapositiva desaparece. |

Ejemplos útiles de `data` en reveal.js 3.x:

```yaml
data:
  background: "#1a1a1a"          # color de fondo de esa diapositiva
  background-image: "/img/x.png" # imagen de fondo
  transition: fade               # transición solo para esta diapositiva
  background-transition: zoom
```

## Configuración global de la presentación

> ⚠️ **Gran parte del bloque `reveal:` de `_config.yml` no lo lee nadie.**
> `_includes/script.html` llama a `Reveal.initialize({ hash: true, dependencies: [...] })`
> con valores escritos a mano y no consulta ninguna variable del sitio
> (`grep -rn 'site\.reveal'` no devuelve nada). Las ~60 líneas de opciones
> (`transition`, `progress`, `center`, `width`, `height`, `controls`) y el
> bloque `slideNumber:` **son inertes**: editarlos no cambia nada, el build
> pasa y el resultado es idéntico.

Lo que sí tiene efecto:

| Dónde | Qué controla |
|---|---|
| `_config.yml` → `title` | El `<title>` de la pestaña del navegador (vía `_includes/head.html`). |
| `_config.yml` → `timezone` | Qué cuenta como "fecha futura" para `future: false`. |
| `_includes/head.html` | El **tema visual**. Hoy `css/theme/moon.css`. Disponibles en `node_modules/reveal.js/css/theme/`: `beige`, `black`, `blood`, `league`, `moon`, `night`, `serif`, `simple`, `sky`, `solarized`, `white`. |
| `_includes/script.html` | Transición, centrado, tamaño, barra de progreso: **aquí**, no en `_config.yml`. |
| Front matter `data:` de cada diapositiva | Fondo y transición **por diapositiva**. Esto sí funciona. |

`author` y `description` de `_config.yml` no se renderizan en ningún sitio.
`solarized.theme` solo pone `class="dark"` en el `<html>`, y el tema `moon` no
define ninguna regla para esa clase: cambiarlo no se nota.

Al tocar el tema o `script.html`, verifica el resultado con
`script/screenshots` — no supongas cómo queda, míralo.

### Opciones que rompen cosas en silencio

- `simple-slideshow: true` en `_config.yml` hace que `_includes/slide.html`
  **deje de emitir todos los atributos `data:`** de todas las diapositivas.
- `overview: true` añade una `<section id="overview">` extra al final.

## Buenas prácticas de contenido

- Una idea por diapositiva. Si dudas, divide.
- ~40 palabras máximo de cuerpo; 6 viñetas máximo.
- Títulos que afirmen algo, no etiquetas ("Ventas +18% en Q3", no "Ventas").
- Toda imagen con `alt` descriptivo. **Ojo: el build NO lo comprueba** —
  `script/cibuild` pasa `--ignore-empty-alt`, y kramdown emite `alt=""` cuando
  no escribes nada. Es responsabilidad de quien escribe y del agente
  `deck-reviewer`.
- Los enlaces deben decir a dónde llevan; nada de "aquí".
- Bloques de código: solo el fragmento relevante, ~12 líneas máximo.
- Portada al principio, conclusión o llamada a la acción al final.

## Flujo de trabajo completo

```sh
export BUNDLE_PATH=vendor/bundle LANG=C.UTF-8 LC_ALL=C.UTF-8

# 1. Escribir o editar archivos en _posts/
# 2. Compilar y validar
script/cibuild

# 3. Comprobar que TODAS las diapositivas se publicaron
find _posts -type f | wc -l
grep -o 'class="page-break"' _site/index.html | wc -l   # debe coincidir

# 4. Ver el resultado
script/screenshots                    # PNG por diapositiva en .preview/
```

> No cuentes `<section`: lo emiten también la sección `overview` opcional y
> cualquier HTML suelto dentro de una diapositiva, así que infla el recuento.
> `class="page-break"` sale exactamente una vez por diapositiva.

Si los dos números del paso 3 no coinciden, hay una diapositiva que no se
publica. Por orden de probabilidad:

1. Fecha futura, **en el nombre o en la clave `date:` del front matter**.
2. Falta `layout: slide`.
3. El nombre no sigue el formato `AAAA-MM-DD-slug.md`.

## Publicación

El sitio se publica con GitHub Pages desde `master`. El flujo correcto es:
rama de trabajo → commit → push → Pull Request → fusión a `master`. El comando
`/publicar` hace todo esto con las verificaciones previas.

## Qué no tocar

- `node_modules/` — reveal.js viene commiteado; se actualiza vía npm, no a mano.
- `_site/` — salida generada, está en `.gitignore`.
- `vendor/` y `.preview/` — locales, ignorados por git.
- `Gemfile.lock` — protegido por una regla `deny` en `.claude/settings.json`.
  Si hace falta regenerarlo, pídeselo al usuario y explica por qué.
