# 🩸 Castlevania: Dominus Collection — Tradução PT-BR

> Tradução **não-oficial** para **Português do Brasil** dos três Castlevania de Nintendo DS presentes na *Castlevania Dominus Collection* (Steam).

<p align="center">
  <img alt="Idioma" src="https://img.shields.io/badge/idioma-Portugu%C3%AAs%20(BR)-009c3b">
  <img alt="Plataforma" src="https://img.shields.io/badge/plataforma-PC%20%2B%20Steam%20Deck-1b2838">
  <img alt="Versão" src="https://img.shields.io/badge/vers%C3%A3o-1.0-8b0000">
  <img alt="Uso" src="https://img.shields.io/badge/uso-n%C3%A3o--comercial-important">
</p>

---

## 📜 Sobre

A **Castlevania Dominus Collection** reúne os clássicos de Nintendo DS da série. Esta tradução leva **todo o texto jogável** dos três jogos DS para o português do Brasil — história, diálogos, itens, equipamentos, bestiário, magias, menus, loja, missões e biblioteca.

A tradução ocupa o **slot do idioma Espanhol** do jogo. Depois de instalar, basta escolher, dentro do jogo, a **European Version** e o idioma **Español** — o texto aparece em português. Nada mais no jogo é alterado.

> ⚠️ **Aviso:** esta é uma **tradução amadora**, feita por um fã, e **pode conter erros** — typos, trechos com sentido ligeiramente diferente do original, quebras de linha ou espaçamentos imperfeitos em alguma caixa de diálogo. Não é um trabalho profissional/oficial. Se encontrar algum erro, fique à vontade para abrir uma [*issue*](../../issues) que eu corrijo em versões futuras. 🙂

---

## 🎮 O que foi traduzido

| Jogo | Frases traduzidas | Cobertura do texto jogável |
|------|:---:|:---:|
| **Castlevania: Order of Ecclesia** | 1.494 | ✅ 100% |
| **Castlevania: Dawn of Sorrow** | 1.016 | ✅ 100% |
| **Castlevania: Portrait of Ruin** | 1.529 | ✅ 100% |

Isso inclui, em cada jogo:

- 📖 **História completa** — todas as cutscenes, do prólogo ao final (incluindo os epílogos)
- 💬 Todos os **diálogos** e NPCs
- 🗡️ **Itens, armas, armaduras, acessórios** e suas descrições
- 👹 **Bestiário** — nomes e descrições de todos os inimigos e chefes
- ✨ **Magias, glifos, almas, habilidades** e descrições
- 🧭 **Menus, loja, save, opções, missões e biblioteca/lore**
- 🗺️ **Nomes das áreas** do mapa

Cada jogo passou por uma **verificação byte a byte** no arquivo final: o texto foi lido de volta direto dos arquivos do jogo e comparado com a tradução — **0 divergências** nos três.

---

## 🚫 O que **não** foi traduzido (de propósito)

| Item | Por quê |
|------|---------|
| Nomes de personagens (Dracula, Jonathan, Charlotte...) | Mantidos no original, como na série |
| Armas lendárias (**Vampire Killer**, Valmanway, Masamune...) | Nomes próprios icônicos |
| **Títulos das músicas** (sound test) | Preservam a identidade da trilha |
| Nomes de pratos gourmet (Foie Gras, Penne Arrabiata...) | Nomes reais de culinária |
| **Haunted Castle** e **Haunted Castle Revisited** | Jogos de ação arcade, praticamente sem texto |
| **Menu/Museu da própria coleção** | O texto ali é *renderizado como imagem/animação* (formato Emote), não como tabela de texto editável — traduzir exigiria refazer gráficos e fontes, com alto risco e pouco retorno |
| Mensagens da **Nintendo Wi-Fi Connection** | Serviço desligado desde 2014; nunca aparecem |

Ou seja: **99% do texto que você realmente vê jogando os três Castlevania de DS está em português.**

---

## 🛠️ Como foi feito (resumo técnico)

Este projeto envolveu **engenharia reversa** do empacotamento do motor **M2** usado na coleção:

1. **Desempacotamento** do arquivo `alldata.bin` + índice `alldata.psb.m` (formato **MDF**, com *shell* zlib e keystream dependente do nome do arquivo).
2. **Descoberta da _code page_ customizada** de cada jogo (caixa mista, acentos, pontuação, quebras de linha e centenas de *tokens* de controle de diálogo — retratos, emoções, ícones de botão, cores).
3. Escrita de um **codec sem perdas** (decodifica → re-codifica byte-exato, validado em todos os idiomas do jogo).
4. **Estratégia de sobrescrever o slot Espanhol** usando o Inglês como base (o que não fosse traduzido continuaria legível).
5. Aplicação com *patch* **in-place** ou **relocação** quando o texto crescia além do espaço original.
6. **Auditoria de integridade de _tokens_** (contagem de caixas de diálogo e marcadores) + **verificação end-to-end** relendo os arquivos do jogo.

Foram **~4.000 frases** traduzidas e conferidas ao longo do processo.

---

## 💾 Instalação

> **Requisitos:** o jogo *Castlevania Dominus Collection* instalado pela **Steam**, na versão original (sem outros mods). O instalador usa **Python 3** — no **Steam Deck / Linux** já vem instalado; no **Windows**, se não tiver, baixe em [python.org/downloads](https://www.python.org/downloads/) marcando *"Add Python to PATH"*.

### 🪟 Windows

1. Baixe e **descompacte** este pacote.
2. **Feche o jogo.**
3. Dê **duplo-clique** em `Instalar-Windows.bat`.
4. Ele encontra a pasta do jogo sozinho, confere e aplica. *(Se não achar, arraste a pasta do jogo para a janela e pressione ENTER.)*
5. Pronto! Abra o jogo → **European Version** → idioma **Español**.

### 🎮 Steam Deck

1. **Feche o jogo** e vá para o **Modo Desktop**.
2. Copie esta pasta para o Deck (ex.: `~/Downloads`).
3. Abra o **Konsole** e rode:
   ```bash
   cd ~/Downloads/CastlevaniaPTBR
   python3 instalar.py
   ```
4. Ele detecta o jogo no SSD **ou no cartão SD**, confere e aplica.
5. Volte ao **Modo Jogo** → abra o jogo → **European Version** → **Español**.

O instalador **não duplica** o arquivo de 1,2 GB: ele altera apenas as partes necessárias e confere tudo por **SHA-1** antes e depois. Se algo não bater, ele **aborta sem estragar nada**.

---

## ↩️ Como reverter

Steam → clique com o direito no jogo → **Propriedades** → **Arquivos instalados** → **Verificar integridade dos arquivos**. O Steam baixa de volta os originais. Simples assim.

> ⚠️ Se a Konami atualizar o jogo, o instalador pode recusar (a verificação SHA-1 falha por segurança). Nesse caso, aguarde uma versão atualizada da tradução.

---

## ⚖️ Licença e uso

Esta é uma **tradução de fã**, feita **sem fins lucrativos** e **sem qualquer afiliação** com a Konami ou a M2.

- ✅ **Pode** baixar, usar e compartilhar **gratuitamente**.
- ✅ **Pode** repostar, desde que **credite** o autor e **mantenha** este aviso.
- ❌ **É proibido vender, cobrar, monetizar ou lucrar** de qualquer forma com esta tradução.
- ❌ **É proibido distribuir os arquivos do jogo.** Compartilhe **apenas o patch** deste repositório — nunca o `alldata.bin` ou outros arquivos originais da Konami.

*Castlevania* e todos os nomes relacionados são marcas registradas da **Konami**. Este projeto não é oficial e não substitui a compra do jogo.

---

## 🙏 Créditos

**Tradução, engenharia reversa e ferramentas:** **Wender_sky** *(Steam)*

Feito com muito café e respeito pela série. 🦇

---

<p align="center"><i>“What is a man? A miserable little pile of secrets!”</i></p>
