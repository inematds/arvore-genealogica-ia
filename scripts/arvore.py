#!/usr/bin/env python3
"""Tabela CSV da família -> árvore visual (HTML com Mermaid) + conferência.

Uso:
  python3 scripts/arvore.py modelos/pessoas.csv --saida minha-arvore.html
  python3 scripts/arvore.py modelos/pessoas.csv --so-confirmados --saida so-provas.html
  python3 scripts/arvore.py modelos/pessoas.csv --mermaid   # só imprime o Mermaid

Colunas: id,nome,nascimento,local_nascimento,pai_id,mae_id,fonte,status,nota
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
import re
import sys

COLUNAS = ["id", "nome", "nascimento", "local_nascimento", "pai_id", "mae_id", "fonte", "status", "nota"]


def ano(txt):
    m = re.search(r"(1[5-9]\d\d|20\d\d)", txt or "")
    return int(m.group(1)) if m else None


def ler(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f))
    if not linhas:
        sys.exit("erro: tabela vazia")
    faltam = [c for c in COLUNAS if c not in linhas[0]]
    if faltam:
        sys.exit(f"erro: faltam colunas: {', '.join(faltam)}")
    pessoas = {}
    for i, l in enumerate(linhas, start=2):
        p = {c: (l.get(c) or "").strip() for c in COLUNAS}
        if not p["id"]:
            sys.exit(f"erro: linha {i} sem id")
        if p["id"] in pessoas:
            sys.exit(f"erro: id repetido: {p['id']}")
        p["status"] = p["status"].upper().replace("Ó", "O")
        pessoas[p["id"]] = p
    return pessoas


def fonte_generica(fonte):
    """Fonte que não aponta um registro: só o domínio, ou texto de modelo ("aqui", "link")."""
    f = fonte.strip().lower()
    if re.fullmatch(r"https?://[^/\s]+/?", f):
        return True
    return bool(re.search(r"\b(aqui|link direto|colar|cole)\b", f))


def conferir(pessoas):
    avisos = []
    for p in pessoas.values():
        if p["status"] == "CONFIRMADO" and p["fonte"] and fonte_generica(p["fonte"]):
            p["status"] = "HIPOTESE"
            avisos.append(f"{p['id']} {p['nome']}: fonte genérica ('{p['fonte']}'), não aponta um registro -> virou HIPOTESE")
        if p["status"] == "CONFIRMADO" and not p["fonte"]:
            p["status"] = "HIPOTESE"
            avisos.append(f"{p['id']} {p['nome']}: marcado CONFIRMADO sem fonte -> virou HIPOTESE")
        if p["status"] not in ("CONFIRMADO", "HIPOTESE"):
            avisos.append(f"{p['id']} {p['nome']}: status '{p['status']}' desconhecido -> HIPOTESE")
            p["status"] = "HIPOTESE"
        for campo in ("pai_id", "mae_id"):
            pid = p[campo]
            if not pid:
                continue
            if pid not in pessoas:
                avisos.append(f"{p['id']} {p['nome']}: {campo} '{pid}' não existe na tabela")
                continue
            a_filho, a_pai = ano(p["nascimento"]), ano(pessoas[pid]["nascimento"])
            if a_filho and a_pai:
                idade = a_filho - a_pai
                if idade < 12 or idade > 70:
                    avisos.append(
                        f"{p['id']} {p['nome']}: {pessoas[pid]['nome']} teria {idade} anos no nascimento — confira")
    return avisos


def rotulo(p):
    partes = [p["nome"] or p["id"]]
    det = " · ".join(x for x in (p["nascimento"], p["local_nascimento"]) if x)
    if det:
        partes.append(det)
    if p["status"] == "HIPOTESE":
        partes.append("(hipótese)")
    txt = "<br/>".join(html.escape(x, quote=False) for x in partes)
    return txt.replace('"', "'")


def mermaid(pessoas, so_confirmados=False):
    vivos = {k: p for k, p in pessoas.items() if not so_confirmados or p["status"] == "CONFIRMADO"}
    out = ["flowchart TD",
           "  classDef conf fill:#1f2937,stroke:#E2A23B,stroke-width:2px,color:#f9fafb",
           "  classDef hip fill:#111827,stroke:#9ca3af,stroke-width:1px,stroke-dasharray:5 4,color:#d1d5db"]
    for k, p in vivos.items():
        out.append(f'  {k}["{rotulo(p)}"]')
        out.append(f"  class {k} {'conf' if p['status'] == 'CONFIRMADO' else 'hip'}")
    for k, p in vivos.items():
        for campo in ("pai_id", "mae_id"):
            pid = p[campo]
            if pid in vivos:
                linha = "-->" if p["status"] == "CONFIRMADO" and vivos[pid]["status"] == "CONFIRMADO" else "-.->"
                out.append(f"  {pid} {linha} {k}")
    return "\n".join(out)


PAGINA = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Árvore genealógica</title>
<style>
body{{margin:0;background:#0c0c10;color:#e5e7eb;font-family:system-ui,sans-serif;padding:16px}}
h1{{font-size:20px;margin:0 0 4px}} p{{color:#9ca3af;margin:0 0 12px;font-size:14px}}
.av{{background:#1c1917;border-left:3px solid #E2A23B;padding:8px 12px;margin:0 0 12px;font-size:13px}}
.av li{{margin:2px 0}} .mermaid{{overflow:auto}}
</style></head><body>
<h1>Árvore genealógica</h1>
<p>Precisa de internet para desenhar (usa o Mermaid). {n_conf} confirmados (caixa com borda âmbar) · {n_hip} hipóteses (tracejadas). Linha cheia = elo com prova dos dois lados.</p>
{avisos}
<pre class="mermaid">
{mmd}
</pre>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true,theme:"dark",securityLevel:"strict"}});</script>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser(description="CSV da família -> árvore visual com conferência")
    ap.add_argument("csv")
    ap.add_argument("--saida", default="arvore.html")
    ap.add_argument("--so-confirmados", action="store_true", help="desenha só quem tem fonte")
    ap.add_argument("--mermaid", action="store_true", help="só imprime o código Mermaid")
    a = ap.parse_args()

    pessoas = ler(a.csv)
    avisos = conferir(pessoas)
    for av in avisos:
        print("aviso:", av, file=sys.stderr)
    mmd = mermaid(pessoas, a.so_confirmados)
    if a.mermaid:
        print(mmd)
        return
    n_conf = sum(p["status"] == "CONFIRMADO" for p in pessoas.values())
    bloco = ""
    if avisos:
        bloco = '<div class="av"><b>Conferir:</b><ul>' + "".join(
            f"<li>{html.escape(x)}</li>" for x in avisos) + "</ul></div>"
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(PAGINA.format(n_conf=n_conf, n_hip=len(pessoas) - n_conf, avisos=bloco, mmd=mmd))
    print(f"ok: {a.saida} ({n_conf} confirmados, {len(pessoas) - n_conf} hipóteses, {len(avisos)} avisos)")


if __name__ == "__main__":
    main()
