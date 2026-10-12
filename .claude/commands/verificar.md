---
description: Comprueba que todo está bien antes de publicar (build, enlaces, orden)
allowed-tools: Read, Glob, Grep, Bash, Agent
---

Verifica el estado completo del repositorio y responde en español, sin jerga.

Ejecuta, en este orden:

1. **Entorno**
   ```sh
   ruby -v && bundle -v && bundle exec jekyll -v
   ```

2. **Build y validación de enlaces**
   ```sh
   script/cibuild
   ```

3. **Inventario de diapositivas**
   ```sh
   ls _posts/
   find _posts -type f | wc -l
   grep -o 'class="page-break"' _site/index.html | wc -l
   ```
   Los dos números deben coincidir. No cuentes `<section`: lo emiten también la
   sección `overview` opcional y cualquier HTML suelto dentro de una
   diapositiva, así que infla el recuento.

   Si no coinciden, alguna diapositiva no se publica. Por orden de
   probabilidad: **fecha futura** (en el nombre o en la clave `date:` del front
   matter, con `future: false`), falta `layout: slide`, o el nombre no sigue el
   formato `AAAA-MM-DD-slug.md`.

4. **Fechas**: ninguna futura (ni en el nombre ni en `date:`), ninguna
   duplicada.

5. **Git**: `git status` y `git log --oneline -3`. Di si hay cambios sin
   guardar y en qué rama estás.

Si algo falla, lanza el agente `build-doctor` para que lo arregle y vuelve a
verificar.

## Formato de la respuesta

```
✅ / ❌  Entorno
✅ / ❌  El sitio compila
✅ / ❌  Enlaces e imágenes correctos
✅ / ❌  Todas las diapositivas se publican (N de N)
✅ / ❌  Fechas correctas

Diapositivas, en orden:
1. ...

Estado de git: rama X, N cambios sin guardar
```

Si algo está en ❌, explica en una frase qué pasa y qué hay que hacer.
