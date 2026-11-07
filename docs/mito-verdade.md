# Mito × verdade: "o ChatGPT monta sua árvore genealógica inteira"

Um vídeo viral ensina 4 pedidos no chat de IA e promete uma árvore completa, parentes que você nunca conheceu e até uma cidadania. Abaixo, passo por passo, o que se sustenta.

| # | O que o vídeo promete | Funciona? | Por quê |
|---|---|---|---|
| 1 | "Me pergunta tudo e monta minha árvore inicial" | ✅ Sim | A IA só organiza o que **você** contou. Não há o que inventar, e ela é ótima em organizar. |
| 2 | "Conta a história da minha linhagem pelo sobrenome" | ⚠️ Meia verdade | A origem de um sobrenome é genérica (região, ofício, apelido). **Mesmo sobrenome não é mesma família**: milhares de pessoas sem parentesco têm o mesmo nome. |
| 3 | "Pesquise registros e ache parentes que eu não tenho" | ❌ É aqui que ela inventa | As bases boas pedem login ou são pagas. No Brasil, muito registro de cartório e de paróquia não está indexado na internet. Com nomes comuns, a IA junta homônimos e **preenche os buracos com gente plausível**. "Nomes que você nunca ouviu falar" é justamente o perigo: você não tem como saber se é parente ou invenção. |
| 4 | "Monta a árvore visual completa" | ✅ Desenha | Mas um desenho bonito não deixa verdadeiros os nomes do passo 3. |
| + | "Você vai até encontrar uma cidadania" | ❌ Exagero | Cidadania por descendência se prova com **certidões** (nascimento, casamento, óbito, às vezes com apostila e tradução), não com resposta de chat. E as regras ficaram mais duras: a Itália limitou a cidadania por descendência em 2025 (Decreto-Lei 36/2025, convertido na Lei 74/2025) e Portugal mudou a lei da nacionalidade em 2025–2026, com partes questionadas no Tribunal Constitucional. Informação conferida em novembro de 2026: confira sempre no consulado. |

## O que é "alucinação" aqui

Um modelo de linguagem escreve o texto mais **provável**, não o mais **verdadeiro**. Se você pede "ache parentes" e ele não encontra um registro, a resposta mais provável não é "não achei": é uma lista de nomes com cara de real (sobrenome certo, cidade certa, época certa). Mesmo quando ele navega na web, pode ler um registro de um homônimo e ligá-lo à sua família sem prova.

## A regra que resolve

> **A IA não é o detetive. É a sua assistente. Quem confirma é o documento.**

Toda pessoa nova na árvore precisa de um **link de registro** (ou um documento físico) com **nome + data + local** que você mesmo abriu e conferiu. O resto fica marcado como **HIPÓTESE**. Os prompts da pasta [`prompts/`](../prompts/) já trazem essa regra.
