# 05 · Pesquisa com prova (o prompt que trava a alucinação)

**Para quê:** é a versão segura do pedido "pesquise e ache parentes que eu não tenho". Use num chat que navega na web (modo agente ou pesquisa). A regra obriga a IA a trazer a prova e a separar o que achou do que supõe.

```text
Pesquise registros públicos de <NOME COMPLETO>, nascido por volta de <ANO> em <LUGAR>, filho de <PAI> e <MÃE> (se souber).

REGRAS OBRIGATÓRIAS:
1) Só inclua uma pessoa na lista CONFIRMADOS se você abriu um registro com NOME + DATA + LOCAL, e me dê o LINK direto desse registro (não a página inicial do site) e o nome da coleção.
2) Para cada confirmado, diga qual informação do registro liga essa pessoa à minha família (pais citados, cônjuge, endereço). Sobrenome igual NÃO é ligação.
3) Tudo o que for suposição vai numa lista separada chamada HIPÓTESES, com o motivo e o documento que confirmaria.
4) Se não achar nada, responda "não encontrei". Isso é uma resposta válida e eu prefiro a ela a um nome inventado.
5) Não preencha datas ou lugares que não estejam no registro.
```

Depois, para cada CONFIRMADO, passe o [checklist de conferência](../docs/checklist-conferencia.md).
