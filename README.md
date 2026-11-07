# 🌳 Árvore genealógica com IA

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![Sua árvore com IA](guia/assets/banner.jpg)](https://inematds.github.io/arvore-genealogica-ia/guia/)

## O que é

Este é um guia gratuito para montar a árvore genealógica da sua família usando um chat de IA (ChatGPT, Claude, Gemini) do jeito certo. Ele explica o que o vídeo viral "o ChatGPT acha seus parentes" acerta e onde a IA inventa pessoas. Traz 8 prompts prontos que obrigam a IA a mostrar a prova, a lista de acervos onde pesquisar de verdade e um checklist para conferir cada nome. Para usar, basta um chat de IA e, se quiser a árvore desenhada, Python 3.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/arvore-genealogica-ia/guia/**

## A regra

> **A IA não é o detetive. É a sua assistente. Quem confirma é o documento.**

Toda pessoa nova na árvore precisa de um registro com **nome + data + local** que você mesmo abriu. O resto fica marcado como **HIPÓTESE**.

## O que tem aqui

| Pasta | O que é |
|---|---|
| [`docs/mito-verdade.md`](docs/mito-verdade.md) | Os 4 pedidos do vídeo viral, um por um: o que funciona e por que a IA inventa parentes. |
| [`prompts/`](prompts/) | 8 prompts prontos: entrevista, tabela, ler documento antigo, onde procurar, pesquisa com prova, auditar resposta, cidadania, árvore visual. |
| [`docs/onde-pesquisar.md`](docs/onde-pesquisar.md) | Acervos de verdade: FamilySearch, cartório (inteiro teor), paróquias, arquivos, Museu da Imigração, Hemeroteca, Antenati, Digitarq, Matricula, DNA. |
| [`docs/checklist-conferencia.md`](docs/checklist-conferencia.md) | O que conferir antes de pôr alguém na árvore, e os sinais de invenção. |
| [`scripts/arvore.py`](scripts/arvore.py) | Transforma a tabela CSV em árvore visual (HTML), com conferência automática. |
| [`modelos/pessoas.csv`](modelos/pessoas.csv) | Tabela de exemplo (família fictícia). |

## O processo, do início ao fim

| # | Passo | Comando / arquivo | Quem |
|---|---|---|---|
| 1 | Entrevistar a família e juntar os papéis da casa | [`prompts/01-entrevista-familia.md`](prompts/01-entrevista-familia.md) | 🧠 você + chat de IA |
| 2 | Organizar tudo numa tabela com `fonte` e `status` | [`prompts/02-organizar-arvore.md`](prompts/02-organizar-arvore.md) → `minha-familia.csv` | 🧠 você + chat de IA |
| 3 | Transcrever e traduzir documentos antigos (foto) | [`prompts/03-ler-documento-antigo.md`](prompts/03-ler-documento-antigo.md) | 🧠 você + chat de IA |
| 4 | Descobrir onde procurar e abrir cada link | [`prompts/04-onde-procurar.md`](prompts/04-onde-procurar.md) + [`docs/onde-pesquisar.md`](docs/onde-pesquisar.md) | 🧠 você |
| 5 | Pesquisar com prova (link direto, ou HIPÓTESE) | [`prompts/05-pesquisa-com-prova.md`](prompts/05-pesquisa-com-prova.md) | 🧠 você + chat com navegação |
| 6 | Auditar listas que a IA já deu (chat novo) | [`prompts/06-auditar-resposta.md`](prompts/06-auditar-resposta.md) | 🧠 você + chat de IA |
| 7 | Conferir cada pessoa nova | [`docs/checklist-conferencia.md`](docs/checklist-conferencia.md) | 🧠 você |
| 8 | (Se quiser) lista de documentos para cidadania | [`prompts/07-cidadania-documentos.md`](prompts/07-cidadania-documentos.md) → consulado | 🧠 você |
| 9 | Desenhar a árvore com conferência automática | `python3 scripts/arvore.py minha-familia.csv --saida minha-arvore.html` | ⚙️ script |

## Rodar o script

```bash
git clone https://github.com/inematds/arvore-genealogica-ia
cd arvore-genealogica-ia
python3 scripts/arvore.py modelos/pessoas.csv --saida exemplo.html        # família fictícia
python3 scripts/arvore.py minha-familia.csv --so-confirmados --saida so-provas.html
python3 -m unittest discover tests                                        # 9 testes
```

O script não tem dependências (só Python 3); o HTML gerado precisa de internet para desenhar. Ele avisa quando:
- uma pessoa está **CONFIRMADO sem fonte**, ou com fonte genérica (só o endereço do site), e a rebaixa para HIPÓTESE;
- um `pai_id`/`mae_id` não existe na tabela;
- o pai ou a mãe teria menos de 12 ou mais de 70 anos no nascimento do filho.

## Cidadania: atenção

As regras mudaram. A Itália limitou a cidadania por descendência em 2025 (Decreto-Lei 36/2025, convertido na Lei 74/2025), e Portugal mudou a Lei da Nacionalidade em 2025–2026, com partes questionadas no Tribunal Constitucional (informação conferida em novembro de 2026). Este guia não dá parecer jurídico: confirme no consulado ou com um advogado especialista.

---

Conteúdo aberto e gratuito · [INEMA.CLUB](https://inema.club)
