#!/usr/bin/env python3
"""Tabela CSV da família -> árvore visual (HTML com Mermaid) + conferência.
Family CSV -> visual tree (HTML with Mermaid) + checks.  CSV de la familia -> árbol visual + revisión.

Uso / Usage / Uso:
  python3 scripts/arvore.py modelos/pessoas.csv --saida minha-arvore.html     (Windows: py scripts\\arvore.py ...)
  python3 scripts/arvore.py modelos/people.csv --so-confirmados --saida only-proof.html
  python3 scripts/arvore.py modelos/personas.csv --mermaid   # só imprime o Mermaid

Colunas aceitas (o idioma da tabela define o idioma das mensagens e da página):
  PT: id,nome,nascimento,local_nascimento,pai_id,mae_id,fonte,status,nota        CONFIRMADO / HIPOTESE
  EN: id,name,birth,place_of_birth,father_id,mother_id,source,status,note        CONFIRMED / HYPOTHESIS
  ES: id,nombre,nacimiento,lugar_nacimiento,padre_id,madre_id,fuente,estado,nota CONFIRMADO / HIPOTESIS
Regras de conferência:
  - CONFIRMADO sem fonte, ou com fonte genérica (só o site, "aqui"), vira HIPOTESE (com aviso);
  - pai_id/mae_id que não existe na tabela gera aviso;
  - pai ou mãe com menos de 12 ou mais de 70 anos no nascimento do filho gera aviso.
Sem dependências: só a biblioteca padrão do Python 3. O HTML gerado precisa de internet ao abrir
(carrega o Mermaid, a biblioteca que desenha o diagrama).
"""
import argparse
import csv
import html
import io
import re
import sys
import unicodedata

COLUNAS = ["id", "nome", "nascimento", "local_nascimento", "pai_id", "mae_id", "fonte", "status", "nota"]
ALIAS = {
    "en": dict(zip(COLUNAS, ["id", "name", "birth", "place_of_birth", "father_id", "mother_id", "source", "status", "note"])),
    "es": dict(zip(COLUNAS, ["id", "nombre", "nacimiento", "lugar_nacimiento", "padre_id", "madre_id", "fuente", "estado", "nota"])),
    "pt": dict(zip(COLUNAS, COLUNAS)),
}
CONF = {"CONFIRMADO", "CONFIRMED", "CONFIRMADA"}
HIP = {"HIPOTESE", "HIPOTESIS", "HYPOTHESIS"}
# fonte que diz que não há fonte
VAZIAS = {"", "n/a", "na", "nao ha", "nenhuma", "nenhum", "sem fonte", "none", "no source", "ninguna", "no hay", "sin fuente", "?"}

T = {
    "pt": dict(
        sem_fonte="{id} {nome}: marcado CONFIRMADO sem fonte -> virou HIPÓTESE",
        generica="{id} {nome}: fonte genérica ('{fonte}'), não aponta um registro -> virou HIPÓTESE",
        status="{id} {nome}: status '{st}' desconhecido -> HIPÓTESE",
        pai="{id} {nome}: {campo} '{pid}' não existe na tabela",
        idade="{id} {nome}: {pai} teria {idade} anos no nascimento — confira",
        hip="(hipótese)", titulo="Árvore genealógica", conferir="Conferir:",
        legenda="Precisa de internet para desenhar (usa o Mermaid). {c} confirmados (caixa com borda âmbar) · {h} hipóteses (tracejadas). Linha cheia = elo com prova dos dois lados.",
        ok="ok: {s} ({c} confirmados, {h} hipóteses, {a} avisos)",
        vazia="erro: tabela vazia", faltam="erro: faltam colunas: {c}", semid="erro: linha {i} sem id",
        repetido="erro: id repetido: {id}", html="pt-BR"),
    "en": dict(
        sem_fonte="{id} {nome}: marked CONFIRMED without a source -> now HYPOTHESIS",
        generica="{id} {nome}: generic source ('{fonte}') that does not point to a record -> now HYPOTHESIS",
        status="{id} {nome}: unknown status '{st}' -> HYPOTHESIS",
        pai="{id} {nome}: {campo} '{pid}' is not in the table",
        idade="{id} {nome}: {pai} would have been {idade} at the birth — check it",
        hip="(hypothesis)", titulo="Family tree", conferir="Check:",
        legenda="Needs internet to draw (uses Mermaid). {c} confirmed (amber border) · {h} hypotheses (dashed). Solid line = link with proof on both sides.",
        ok="ok: {s} ({c} confirmed, {h} hypotheses, {a} warnings)",
        vazia="error: empty table", faltam="error: missing columns: {c}", semid="error: row {i} has no id",
        repetido="error: duplicate id: {id}", html="en"),
    "es": dict(
        sem_fonte="{id} {nome}: marcado CONFIRMADO sin fuente -> pasó a HIPÓTESIS",
        generica="{id} {nome}: fuente genérica ('{fonte}'), no apunta a un registro -> pasó a HIPÓTESIS",
        status="{id} {nome}: estado '{st}' desconocido -> HIPÓTESIS",
        pai="{id} {nome}: {campo} '{pid}' no existe en la tabla",
        idade="{id} {nome}: {pai} tendría {idade} años en el nacimiento — revísalo",
        hip="(hipótesis)", titulo="Árbol genealógico", conferir="Revisar:",
        legenda="Necesita internet para dibujar (usa Mermaid). {c} confirmados (borde ámbar) · {h} hipótesis (punteadas). Línea continua = vínculo con prueba en ambos lados.",
        ok="ok: {s} ({c} confirmados, {h} hipótesis, {a} avisos)",
        vazia="error: tabla vacía", faltam="error: faltan columnas: {c}", semid="error: fila {i} sin id",
        repetido="error: id repetido: {id}", html="es"),
}


def ano(txt):
    m = re.search(r"(1[5-9]\d\d|20\d\d)", txt or "")
    return int(m.group(1)) if m else None


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def ler(caminho):
    bruto = open(caminho, "rb").read()
    try:
        texto = bruto.decode("utf-8-sig")
    except UnicodeDecodeError:  # Excel do Windows salva "CSV" em cp1252
        texto = bruto.decode("cp1252", errors="replace")
    # o chat costuma cercar a tabela com ```csv ... ```: ignora essas linhas
    texto = "\n".join(l for l in texto.splitlines() if not l.strip().startswith("```"))
    texto = texto.strip()
    if not texto:
        sys.exit(" / ".join(T[l]["vazia"] for l in ("pt", "en", "es")))
    # Excel em PT/ES salva com ";" — detecta pelo cabeçalho
    sep = ";" if texto.splitlines()[0].count(";") > texto.splitlines()[0].count(",") else ","
    linhas = list(csv.DictReader(io.StringIO(texto), delimiter=sep))
    if not linhas:
        sys.exit(" / ".join(T[l]["vazia"] for l in ("pt", "en", "es")))
    cab = {(k or "").strip().lower() for k in linhas[0].keys()}
    linhas = [{(k or "").strip().lower(): v for k, v in l.items()} for l in linhas]
    # idioma = o que tem mais colunas presentes
    acertos = {l: len(set(ALIAS[l].values()) & cab) for l in ALIAS}
    lang = max(ALIAS, key=lambda l: (acertos[l], l == "pt"))
    al = ALIAS[lang]
    faltam = [al[c] for c in COLUNAS if al[c] not in cab]
    if faltam:
        if acertos[lang] <= 1:  # nem dá para saber o idioma: mostra os três
            sys.exit("\n".join(T[l]["faltam"].format(c=", ".join(ALIAS[l].values())) for l in ("pt", "en", "es")))
        sys.exit(T[lang]["faltam"].format(c=", ".join(faltam)))
    pessoas = {}
    for i, l in enumerate(linhas, start=2):
        p = {c: (l.get(al[c]) or "").strip() for c in COLUNAS}
        if not p["id"]:
            sys.exit(T[lang]["semid"].format(i=i))
        if p["id"] in pessoas:
            sys.exit(T[lang]["repetido"].format(id=p["id"]))
        if sem_acento(p["fonte"]).strip(" .-").lower() in VAZIAS:
            p["fonte"] = ""
        p["status_orig"] = p["status"]
        st = sem_acento(p["status"]).upper()
        p["status"] = "CONFIRMADO" if st in CONF else "HIPOTESE" if st in HIP else st
        pessoas[p["id"]] = p
    return pessoas, lang


def fonte_generica(fonte):
    """Fonte que não aponta um registro: só o domínio, ou texto de modelo ("aqui", "link")."""
    f = fonte.strip().lower()
    if re.fullmatch(r"https?://[^/\s]+/?", f):
        return True
    # texto de modelo: fala de "link" junto com "aqui/here/aquí", ou manda colar
    tem_link = re.search(r"\b(link|enlace)\b", f)
    return bool((tem_link and re.search(r"\b(aqui|here|aquí)\b", f))
                or re.match(r"^\W*(cole|colar|paste|pega|pegue|pegar)\b", f))


def conferir(pessoas, lang):
    t = T[lang]
    avisos = []
    for p in pessoas.values():
        if p["status"] == "CONFIRMADO" and p["fonte"] and fonte_generica(p["fonte"]):
            p["status"] = "HIPOTESE"
            avisos.append(t["generica"].format(id=p["id"], nome=p["nome"], fonte=p["fonte"]))
        if p["status"] == "CONFIRMADO" and not p["fonte"]:
            p["status"] = "HIPOTESE"
            avisos.append(t["sem_fonte"].format(id=p["id"], nome=p["nome"]))
        if p["status"] not in ("CONFIRMADO", "HIPOTESE"):
            avisos.append(t["status"].format(id=p["id"], nome=p["nome"], st=p["status_orig"]))
            p["status"] = "HIPOTESE"
        for campo in ("pai_id", "mae_id"):
            pid = p[campo]
            if not pid:
                continue
            if pid not in pessoas:
                avisos.append(t["pai"].format(id=p["id"], nome=p["nome"], campo=ALIAS[lang][campo], pid=pid))
                continue
            a_filho, a_pai = ano(p["nascimento"]), ano(pessoas[pid]["nascimento"])
            if a_filho and a_pai:
                idade = a_filho - a_pai
                if idade < 12 or idade > 70:
                    avisos.append(t["idade"].format(id=p["id"], nome=p["nome"], pai=pessoas[pid]["nome"], idade=idade))
    return avisos


def rotulo(p, lang):
    partes = [p["nome"] or p["id"]]
    det = " · ".join(x for x in (p["nascimento"], p["local_nascimento"]) if x)
    if det:
        partes.append(det)
    if p["status"] == "HIPOTESE":
        partes.append(T[lang]["hip"])
    txt = "<br/>".join(html.escape(x, quote=False) for x in partes)
    return txt.replace('"', "'")


def mermaid(pessoas, lang="pt", so_confirmados=False):
    vivos = {k: p for k, p in pessoas.items() if not so_confirmados or p["status"] == "CONFIRMADO"}
    out = ["flowchart TD",
           "  classDef conf fill:#1f2937,stroke:#E2A23B,stroke-width:2px,color:#f9fafb",
           "  classDef hip fill:#111827,stroke:#9ca3af,stroke-width:1px,stroke-dasharray:5 4,color:#d1d5db"]
    for k, p in vivos.items():
        out.append(f'  {k}["{rotulo(p, lang)}"]')
        out.append(f"  class {k} {'conf' if p['status'] == 'CONFIRMADO' else 'hip'}")
    for k, p in vivos.items():
        for campo in ("pai_id", "mae_id"):
            pid = p[campo]
            if pid in vivos:
                linha = "-->" if p["status"] == "CONFIRMADO" and vivos[pid]["status"] == "CONFIRMADO" else "-.->"
                out.append(f"  {pid} {linha} {k}")
    return "\n".join(out)


PAGINA = """<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
<style>
body{{margin:0;background:#0c0c10;color:#e5e7eb;font-family:system-ui,sans-serif;padding:16px}}
h1{{font-size:20px;margin:0 0 4px}} p{{color:#9ca3af;margin:0 0 12px;font-size:14px}}
.av{{background:#1c1917;border-left:3px solid #E2A23B;padding:8px 12px;margin:0 0 12px;font-size:13px}}
.av li{{margin:2px 0}} .mermaid{{overflow:auto}}
</style></head><body>
<h1>{titulo}</h1>
<p>{legenda}</p>
{avisos}
<pre class="mermaid">
{mmd}
</pre>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true,theme:"dark",securityLevel:"strict"}});</script>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser(description="CSV da família -> árvore visual com conferência (PT/EN/ES)")
    ap.add_argument("csv")
    ap.add_argument("--saida", "--output", "--salida", dest="saida", default="arvore.html")
    ap.add_argument("--so-confirmados", "--only-confirmed", "--solo-confirmados", dest="so_confirmados",
                    action="store_true", help="desenha só quem tem fonte / only people with a source")
    ap.add_argument("--mermaid", action="store_true", help="só imprime o código Mermaid")
    a = ap.parse_args()

    pessoas, lang = ler(a.csv)
    t = T[lang]
    avisos = conferir(pessoas, lang)
    for av in avisos:
        print("!", av, file=sys.stderr)
    mmd = mermaid(pessoas, lang, a.so_confirmados)
    if a.mermaid:
        print(mmd)
        return
    n_conf = sum(p["status"] == "CONFIRMADO" for p in pessoas.values())
    n_hip = len(pessoas) - n_conf
    bloco = ""
    if avisos:
        bloco = f'<div class="av"><b>{t["conferir"]}</b><ul>' + "".join(
            f"<li>{html.escape(x)}</li>" for x in avisos) + "</ul></div>"
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(PAGINA.format(lang=t["html"], titulo=t["titulo"], legenda=t["legenda"].format(c=n_conf, h=n_hip),
                              avisos=bloco, mmd=mmd))
    print(t["ok"].format(s=a.saida, c=n_conf, h=n_hip, a=len(avisos)))


if __name__ == "__main__":
    main()
