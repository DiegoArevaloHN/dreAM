#!/usr/bin/env python3
"""Valida una diapositiva justo después de que Claude la crea o edita.

Hook PostToolUse (Edit|Write). Solo revisa archivos dentro de `_posts/`.
Si encuentra un problema, sale con código 2 para que Claude lo corrija
inmediatamente en lugar de descubrirlo en el build.

Comprueba:
  1. Nombre de archivo con el formato AAAA-MM-DD-slug.md que Jekyll exige.
  2. Fecha del nombre no futura (`future: false` en _config.yml haría
     desaparecer la diapositiva sin dar ningún error).
  3. Clave `date:` del front matter tampoco futura: gana a la del nombre, así
     que una fecha futura ahí esconde la diapositiva igual de silenciosamente.
  4. Front matter presente y con `layout: slide`.
  5. Que exista un `title` (aunque sea vacío a propósito).
  6. Que no haya fechas duplicadas que hagan el orden impredecible.
"""

import datetime
import json
import os
import re
import sys

NAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-[^/]+\.(md|markdown|html)$")

# El front matter de Jekyll son las líneas entre el primer '---' del archivo y
# el siguiente '---' que esté solo en su línea. Partir por content.split("---")
# rompe en cuanto un valor contiene '---' (por ejemplo un guion largo escrito a
# mano en un título), y entonces el hook rechaza archivos perfectamente válidos.
FRONT_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)

LAYOUT_RE = re.compile(r"""^\s*layout:\s*["']?slide["']?\s*$""", re.MULTILINE)
TITLE_RE = re.compile(r"^\s*title:", re.MULTILINE)
# Acepta `date: 2026-01-01`, con o sin hora, con o sin comillas.
DATE_RE = re.compile(
    r"""^\s*date:\s*["']?(\d{4})-(\d{2})-(\d{2})""", re.MULTILINE
)

# El proyecto, deducido de la ubicación de este propio archivo
# (<repo>/.claude/hooks/check-slide.py). No depende de que el payload traiga
# `cwd`, que es opcional y puede faltar.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def hoy():
    """Fecha de hoy en la zona horaria que usa Jekyll para `future: false`.

    `_config.yml` declara una `timezone`, y es ésa —no la de la máquina ni
    UTC— la que decide si una diapositiva se considera futura. Entre la
    medianoche local y la de esa zona, usar la equivocada produce avisos
    falsos.
    """
    zona = None
    try:
        with open(os.path.join(REPO, "_config.yml"), encoding="utf-8") as handle:
            encontrado = re.search(
                r"^timezone:\s*(\S+)", handle.read(), re.MULTILINE
            )
        if encontrado:
            zona = encontrado.group(1).strip("\"'")
    except OSError:
        pass

    if zona:
        try:
            from zoneinfo import ZoneInfo

            return datetime.datetime.now(ZoneInfo(zona)).date()
        except Exception:
            pass

    return datetime.date.today()


def fecha_valida(year: int, month: int, day: int) -> bool:
    """Jekyll acepta años como 0000 (la portada usa 0000-01-01), que
    datetime.date no admite. Validamos el calendario de verdad solo cuando el
    año está en el rango que datetime soporta."""
    if year >= datetime.MINYEAR:
        try:
            datetime.date(year, month, day)
            return True
        except ValueError:
            return False
    return 1 <= month <= 12 and 1 <= day <= 31


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or ""
    if not path:
        return 0

    posts_dir = os.path.realpath(os.path.join(payload.get("cwd") or REPO, "_posts"))
    # realpath resuelve enlaces simbólicos: sin eso, una ruta con enlaces se
    # compara como distinta y el hook se desactiva solo, en silencio.
    if os.path.realpath(os.path.dirname(os.path.abspath(path))) != posts_dir:
        return 0
    if not os.path.isfile(path):
        return 0

    name = os.path.basename(path)
    problems = []
    limite = hoy()

    match = NAME_RE.match(name)
    if not match:
        problems.append(
            f"El nombre '{name}' no sirve: Jekyll exige AAAA-MM-DD-slug.md "
            "(por ejemplo 2026-07-30-mi-diapositiva.md). Sin ese formato la "
            "diapositiva no se publica."
        )
    else:
        year, month, day = (int(g) for g in match.groups()[:3])
        if not fecha_valida(year, month, day):
            problems.append(
                f"La fecha del nombre '{name}' no existe en el calendario."
            )
        elif (year, month, day) > (limite.year, limite.month, limite.day):
            problems.append(
                f"La fecha {year:04d}-{month:02d}-{day:02d} del nombre está en "
                "el futuro y _config.yml tiene `future: false`, así que esta "
                "diapositiva NO aparecerá en la presentación. Usa la fecha de "
                "hoy o anterior."
            )

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            content = handle.read()
    except OSError as error:
        print(f"No pude leer {name}: {error}", file=sys.stderr)
        return 0

    front_match = FRONT_RE.match(content)
    if front_match is None:
        problems.append(
            "Falta el front matter. El archivo debe empezar con una línea '---', "
            "luego 'layout: slide' y 'title: \"...\"', y cerrar con otra '---'."
        )
    else:
        front = front_match.group(1)
        if not LAYOUT_RE.search(front):
            problems.append(
                "El front matter no declara 'layout: slide'. Sin ese layout la "
                "diapositiva se renderiza mal."
            )
        if not TITLE_RE.search(front):
            problems.append(
                "El front matter no tiene 'title:'. Usa title: \"\" si quieres "
                "una diapositiva sin encabezado."
            )

        # La clave `date:` gana a la fecha del nombre. Si es futura, la
        # diapositiva desaparece aunque el nombre del archivo sea correcto.
        fecha_front = DATE_RE.search(front)
        if fecha_front:
            fy, fm, fd = (int(g) for g in fecha_front.groups())
            if not fecha_valida(fy, fm, fd):
                problems.append(
                    f"La fecha '{fy:04d}-{fm:02d}-{fd:02d}' del front matter no "
                    "existe en el calendario."
                )
            elif (fy, fm, fd) > (limite.year, limite.month, limite.day):
                problems.append(
                    f"El front matter tiene `date: {fy:04d}-{fm:02d}-{fd:02d}`, "
                    "una fecha futura. Esa clave manda sobre la del nombre, así "
                    "que la diapositiva NO se publicará. Quítala o ponle una "
                    "fecha de hoy o anterior."
                )

    # Fechas duplicadas: el orden de site.posts se vuelve arbitrario.
    if match:
        prefix = name[:10]
        try:
            vecinos = os.listdir(posts_dir)
        except OSError:
            vecinos = []
        # NAME_RE filtra los respaldos del editor (.orig, .bak, .swp): no son
        # diapositivas y no deben contar como duplicados.
        siblings = [
            other
            for other in vecinos
            if other != name and other.startswith(prefix) and NAME_RE.match(other)
        ]
        if siblings:
            problems.append(
                f"Ya existe otra diapositiva con la fecha {prefix} "
                f"({', '.join(sorted(siblings))}). Dos diapositivas con la misma "
                "fecha tienen un orden impredecible: cámbiale la fecha a una libre."
            )

    if problems:
        print(f"Problemas en {name}:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print(
            "Corrígelos ahora. Detalles en .claude/skills/presentaciones/SKILL.md",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
