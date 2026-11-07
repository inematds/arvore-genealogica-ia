# 🌳 Árbol genealógico con IA

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![Tu árbol con IA](guia/assets/banner-es.jpg)](https://inematds.github.io/arvore-genealogica-ia/guia/es/)

## Qué es

Esta es una guía gratuita para armar el árbol genealógico de tu familia usando correctamente un chat de IA (ChatGPT, Claude, Gemini). Explica qué acierta el video viral «ChatGPT encuentra a tus familiares» y dónde la IA inventa personas. Incluye 8 prompts listos para usar que obligan a la IA a mostrar las pruebas, una lista de archivos donde investigar de verdad y una lista de verificación para confirmar cada nombre. Para usarla, solo necesitas un chat de IA y, si quieres dibujar el árbol, Python 3.

## 📖 Guía de uso

Guía completa (página de presentación + paso a paso): **https://inematds.github.io/arvore-genealogica-ia/guia/es/**

## La regla

> **La IA no es la detective. Es tu asistente. Quien confirma es el documento.**

Toda persona nueva en el árbol necesita un registro con **nombre + fecha + lugar** que tú mismo hayas abierto. Lo demás queda marcado como **HIPÓTESIS**.

## Qué incluye

> Los prompts y documentos de `prompts/` y `docs/` están en portugués (la página de la guía trae todos los prompts en español).

| Carpeta | Qué es |
|---|---|
| [`docs/mito-verdade.md`](docs/mito-verdade.md) | Las 4 solicitudes del video viral, una por una: qué funciona y por qué la IA inventa familiares. |
| [`prompts/`](prompts/) | 8 prompts listos para usar: entrevista, tabla, leer un documento antiguo, dónde buscar, investigación con pruebas, auditar una respuesta, ciudadanía, árbol visual. |
| [`docs/onde-pesquisar.md`](docs/onde-pesquisar.md) | Archivos reales: FamilySearch, registro civil (copia íntegra), parroquias, archivos, Museu da Imigração, Hemeroteca, Antenati, Digitarq, Matricula, ADN. |
| [`docs/checklist-conferencia.md`](docs/checklist-conferencia.md) | Qué confirmar antes de incluir a alguien en el árbol y las señales de invención. |
| [`scripts/arvore.py`](scripts/arvore.py) | Transforma la tabla CSV en un árbol visual (HTML), con verificación automática. |
| [`modelos/pessoas.csv`](modelos/pessoas.csv) | Tabla de ejemplo (familia ficticia). |

## El proceso, de principio a fin

| # | Paso | Comando / archivo | Quién |
|---|---|---|---|
| 1 | Entrevistar a la familia y reunir los documentos de la casa | [`prompts/01-entrevista-familia.md`](prompts/01-entrevista-familia.md) | 🧠 tú + chat de IA |
| 2 | Organizar todo en una tabla con `fonte` y `status` | [`prompts/02-organizar-arvore.md`](prompts/02-organizar-arvore.md) → `minha-familia.csv` | 🧠 tú + chat de IA |
| 3 | Transcribir y traducir documentos antiguos (foto) | [`prompts/03-ler-documento-antigo.md`](prompts/03-ler-documento-antigo.md) | 🧠 tú + chat de IA |
| 4 | Descubrir dónde buscar y abrir cada enlace | [`prompts/04-onde-procurar.md`](prompts/04-onde-procurar.md) + [`docs/onde-pesquisar.md`](docs/onde-pesquisar.md) | 🧠 tú |
| 5 | Investigar con pruebas (enlace directo o HIPÓTESIS) | [`prompts/05-pesquisa-com-prova.md`](prompts/05-pesquisa-com-prova.md) | 🧠 tú + chat con navegación |
| 6 | Auditar listas que la IA ya proporcionó (chat nuevo) | [`prompts/06-auditar-resposta.md`](prompts/06-auditar-resposta.md) | 🧠 tú + chat de IA |
| 7 | Confirmar cada persona nueva | [`docs/checklist-conferencia.md`](docs/checklist-conferencia.md) | 🧠 tú |
| 8 | (Si quieres) lista de documentos para la ciudadanía | [`prompts/07-cidadania-documentos.md`](prompts/07-cidadania-documentos.md) → consulado | 🧠 tú |
| 9 | Dibujar el árbol con verificación automática | `python3 scripts/arvore.py minha-familia.csv --saida minha-arvore.html` | ⚙️ script |

## Ejecutar el script

```bash
git clone https://github.com/inematds/arvore-genealogica-ia
cd arvore-genealogica-ia
python3 scripts/arvore.py modelos/pessoas.csv --saida exemplo.html        # familia fictícia
python3 scripts/arvore.py minha-familia.csv --so-confirmados --saida so-provas.html
python3 -m unittest discover tests                                        # 9 pruebas
```

El script no tiene dependencias (solo Python 3); el HTML generado necesita internet para dibujarse. Avisa cuando:
- una persona está **CONFIRMADO sin fuente**, o con una fuente genérica (solo la dirección del sitio), y la degrada a HIPÓTESIS;
- un `pai_id`/`mae_id` no existe en la tabla;
- el padre o la madre tendría menos de 12 o más de 70 años cuando nació el hijo.

## Ciudadanía: atención

Las reglas cambiaron. Italia limitó la ciudadanía por descendencia en 2025 (Decreto-Ley 36/2025, convertido en Ley 74/2025), y Portugal cambió la Ley de Nacionalidad en 2025–2026, con partes cuestionadas ante el Tribunal Constitucional (información verificada en noviembre de 2026). Esta guía no ofrece asesoría legal: confirma la información en el consulado o con un abogado especialista.

---

Contenido abierto y gratuito · [INEMA.CLUB](https://inema.club)
