# Guía rápida — qué escribir para que Claude haga el trabajo

Esta guía es para ti, no para Claude. No necesitas saber programar: basta con
escribir una de estas frases.

---

## Los 6 comandos que resuelven casi todo

Escríbelos tal cual, empezando por la barra `/`.

### `/nueva-presentacion <tema>`
Crea una presentación completa desde cero.

> `/nueva-presentacion los resultados de ventas de Factured en el último trimestre`

Claude investiga si hace falta, escribe las diapositivas, las revisa y te
**muestra imágenes** de cómo quedaron. No publica nada todavía.

### `/nueva-slide <lo que quieres decir>`
Añade una diapositiva a la presentación que ya existe.

> `/nueva-slide una diapositiva de cierre invitando a agendar una reunión`

### `/vista-previa`
Te muestra una imagen de cada diapositiva, tal como se verán proyectadas.
Úsalo siempre antes de publicar.

### `/verificar`
Comprueba que todo está sano: que el sitio se genera, que no hay enlaces
rotos y que **todas** tus diapositivas se están publicando. Te responde con
una lista de ✅ y ❌.

### `/publicar`
Guarda los cambios y los sube a GitHub creando un Pull Request. Antes de
subir nada, verifica que todo funcione. Si algo está roto, se detiene y te
lo explica.

### `/traducir-deck <idioma>`
Traduce toda la presentación.

> `/traducir-deck inglés`

---

## Y si prefieres pedirlo con tus palabras

También funciona. Claude reconoce la intención y usa las herramientas correctas:

- "hazme una presentación de 8 diapositivas sobre X"
- "el sitio no funciona, arréglalo"
- "muéstrame cómo se ven las diapositivas"
- "ábreme la presentación en el navegador" *(la levanta en `localhost:4000`)*
- "cambia el tema de la presentación a algo más claro"
- "revisa la presentación antes de que la muestre mañana"
- "mueve la diapositiva de precios al final"
- "falta una diapositiva, revisa las fechas"

---

## Los especialistas que trabajan por dentro

No tienes que invocarlos: Claude los llama cuando toca. Pero si quieres pedir
uno directamente, nómbralo.

| Especialista | Para qué sirve |
|---|---|
| `slide-author` | Escribe y estructura las diapositivas |
| `deck-reviewer` | Revisa calidad, accesibilidad y ortografía antes de publicar |
| `build-doctor` | Arregla el sitio cuando algo se rompe |
| `investigador` | Busca datos con fuentes verificables para tus diapositivas |

> "usa el deck-reviewer para revisar la presentación"

---

## Las dos reglas que evitan el 90% de los problemas

1. **Si una diapositiva que pediste no aparece, casi siempre es la fecha.**
   Cada diapositiva lleva una fecha interna que tú nunca ves; si queda por
   delante de hoy, el sistema la esconde sin avisar. No tienes que entenderlo:
   solo escribe **"falta una diapositiva, revisa las fechas"** y Claude lo
   arregla. (Hay validaciones automáticas que lo cazan al crearla, pero esta es
   la señal por si alguna se escapa.)

2. **Ejecuta `/verificar` antes de `/publicar`.** Es la diferencia entre
   descubrir un error tú o descubrirlo tu audiencia.

---

## Qué pasa cuando publicas

`/publicar` **no** cambia el sitio público de inmediato. Crea un *Pull Request*:
una propuesta de cambio que queda esperando tu visto bueno.

Se crea **como borrador** (*draft*), que significa "aún no listo para
publicar". Para que el cambio llegue a la web, en GitHub tienes que:

1. Pulsar **Ready for review** (quitarle el estado de borrador)
2. Pulsar **Merge** (incorporarlo)

Hasta ese momento el sitio público no cambia nada.

Claude vigila ese Pull Request y te avisa si algo falla en las comprobaciones
automáticas.

---

## Pequeño glosario

Cuatro palabras que verás en GitHub y en lo que te escriba Claude:

| Palabra | Qué significa, en corto |
|---|---|
| **Repositorio** | La carpeta del proyecto, guardada en GitHub con todo su historial. |
| **Rama** (*branch*) | Una copia donde se trabaja sin tocar lo que está publicado. `master` es la publicada. |
| **Fusionar** (*merge*) | Incorporar los cambios de una rama a lo publicado. Es el paso que hace que el sitio cambie. |
| **Pull Request** | La propuesta de fusionar esos cambios, para revisarla antes. |

---

## Si algo se rompe

Escribe simplemente:

> "algo no funciona, revísalo y arréglalo"

Claude reproducirá el error, encontrará la causa y lo corregirá. Los fallos
típicos de este proyecto ya están documentados para él en `CLAUDE.md`, así que
no tiene que adivinar.
