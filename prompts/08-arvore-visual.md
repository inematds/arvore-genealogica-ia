# 08 · Árvore visual só com quem foi confirmado

**Para quê:** o desenho final. Duas formas:

**A) Pelo script deste projeto (recomendado).** Salve a tabela do prompt 02 como `minha-familia.csv` e rode:

```bash
python3 scripts/arvore.py minha-familia.csv --saida minha-arvore.html
```

Abre no navegador: confirmados em caixa cheia, hipóteses em caixa tracejada (ou fora, com `--so-confirmados`).

**B) Pelo chat.**

```text
Com esta tabela CSV, desenhe a árvore genealógica em Mermaid (flowchart TD).
Pessoas com status CONFIRMADO em caixa normal; HIPOTESE em caixa com borda tracejada e o texto "(hipótese)".
Não acrescente ninguém que não esteja na tabela.

<cole o CSV>
```

Para guardar a árvore em um site de genealogia (FamilySearch, MyHeritage, Ancestry), o formato universal é o **GEDCOM** (.ged): esses sites importam e exportam nele.
