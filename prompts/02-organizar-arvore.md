# 02 · Organizar a árvore em tabela (funciona)

**Para quê:** transformar o que você juntou numa tabela no formato do [`modelos/pessoas.csv`](../modelos/pessoas.csv), que o script [`scripts/arvore.py`](../scripts/arvore.py) transforma em árvore visual.

```text
Com tudo o que eu te contei nesta conversa, monte uma tabela CSV com estas colunas, nesta ordem:
id,nome,nascimento,local_nascimento,pai_id,mae_id,fonte,status,nota

Regras:
- id curto e único (ex.: p01, p02...). pai_id e mae_id usam esses ids (vazio se não sei).
- fonte = o link do registro ou o documento ("certidão de casamento, original em casa"). Vazio se não houver.
- status = CONFIRMADO só se a fonte estiver preenchida; senão HIPOTESE.
- nota = o que falta para confirmar.
- Não invente ninguém. Responda só com o CSV.
```
