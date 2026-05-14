# Antigravity Kit

> Template per agenti AI con Skill, Agenti e Workflow

<div  align="center">
    <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit?theme=dark" alt="Antigravity Kit - Nổi bật trên Unikorn.vn" style="width: 210px; height: 54px;" width="210" height="54" /></a>
    <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit/rank?theme=dark&type=daily" alt="Antigravity Kit - Hàng ngày" style="width: 250px; height: 64px;" width="250" height="64" /></a>
    <a href="https://launch.j2team.dev/products/antigravity-kit" target="_blank"><img src="https://launch.j2team.dev/badge/antigravity-kit/dark" alt="Antigravity Kit on J2TEAM Launch" width="250" height="54" /></a>
</div>

## Installazione Rapida

```bash
npx github:Andryd22/antigravity-kit-andryd init -y
```

Opzioni disponibili:

```bash
npx github:Andryd22/antigravity-kit-andryd init -y --force   # Sovrascrive la cartella .agent/ esistente
npx github:Andryd22/antigravity-kit-andryd init -y --dry-run # Mostra un'anteprima senza scrivere file
npx github:Andryd22/antigravity-kit-andryd init -y --path ./myapp  # Directory di destinazione
npx github:Andryd22/antigravity-kit-andryd status         # Mostra i componenti inclusi
```

> **Cosa c'è di diverso?** Questo fork aggiunge agenti per AI/ML, Data Engineering, Embedded/IoT, LaTeX, la Caveman Mode (`/caveman`) e oltre 10 skill aggiuntive rispetto alla versione ufficiale.

Questo comando installa la cartella `.agent` contenente tutti i template all'interno del tuo progetto.

### ⚠️ Nota Importante su `.gitignore`
Se stai usando editor basati sull'AI come **Cursor** o **Windsurf**, aggiungere la cartella `.agent/` al tuo file `.gitignore` potrebbe impedire all'IDE di indicizzare i workflow. Questo fa sì che gli slash command (come `/plan`, `/debug`) non compaiano nel menu a tendina della chat.

**Soluzione Consigliata:**
Per mantenere la cartella `.agent/` locale (non tracciata da Git) senza perdere le funzionalità AI:
1. Assicurati che `.agent/` **NON** sia nel file `.gitignore` del tuo progetto.
2. Aggiungilo invece al tuo file di esclusione locale: `.git/info/exclude`

## Cosa è Incluso

| Componente    | Quantità | Descrizione                                                        |
| ------------- | -------- | ------------------------------------------------------------------ |
| **Agenti**    | 25       | Personas AI specializzate (frontend, backend, AI/ML, IoT, LaTeX, ecc.) |
| **Skill**     | 48       | Moduli di conoscenza specifici per dominio                         |
| **Workflow**  | 13       | Procedure attivabili tramite slash command                         |
| **Modern ES** | 2026+    | **Next.js 16 & React 19 Native** (Cache Components, PPR, Proxy)    |


## Utilizzo

### Usare gli Agenti

**Non c'è bisogno di menzionare esplicitamente gli agenti!** Il sistema rileva automaticamente e applica lo specialista (o gli specialisti) giusto:

```
Tu: "Aggiungi l'autenticazione JWT"
AI: 🤖 Applico @security-auditor + @backend-specialist...

Tu: "Correggi il pulsante della dark mode"
AI: 🤖 Uso @frontend-specialist...

Tu: "Il login restituisce un errore 500"
AI: 🤖 Uso @debugger per un'analisi sistematica...
```

**Come funziona:**

- Analizza silenziosamente la tua richiesta
- Rileva automaticamente i domini di competenza (frontend, backend, sicurezza, ecc.)
- Seleziona i migliori specialisti
- Ti informa su quale competenza sta venendo applicata
- Ottieni risposte a livello di specialista senza dover conoscere l'architettura del sistema

**Vantaggi:**

- ✅ Nessuna curva di apprendimento: descrivi solo ciò di cui hai bisogno
- ✅ Ottieni sempre risposte da esperti
- ✅ Trasparenza: mostra quale agente viene utilizzato
- ✅ Puoi sempre forzare l'uso di un agente menzionandolo esplicitamente

### Usare i Workflow

Richiama i workflow tramite gli slash command:

| Comando          | Descrizione                           |
| ---------------- | ------------------------------------- |
| `/brainstorm`    | Esplora le opzioni prima dell'implementazione |
| `/create`        | Crea nuove funzionalità o applicazioni |
| `/debug`         | Debugging sistematico                  |
| `/deploy`        | Esegue il deploy dell'applicazione     |
| `/enhance`       | Migliora il codice esistente           |
| `/orchestrate`   | Coordinazione multi-agente             |
| `/plan`          | Crea un piano dettagliato per le task  |
| `/preview`       | Visualizza un'anteprima delle modifiche in locale |
| `/status`        | Controlla lo stato del progetto        |
| `/test`          | Genera ed esegue i test                |
| `/ui-ux-pro-max` | Progetta interfacce con 50 stili       |
| `/caveman`       | Attiva la modalità di risposta per risparmiare token |
| `/html-it`       | Framework per output HTML di alta qualità |

Esempio:

```
/brainstorm authentication system
/create landing page with hero section
/debug why login fails
```

### Usare le Skill

Le skill vengono caricate automaticamente in base al contesto della task. L'AI legge le descrizioni delle skill e applica le conoscenze pertinenti.

## Strumento CLI

| Comando         | Descrizione                               |
| --------------- | ----------------------------------------- |
| `ag-kit init`   | Installa la cartella `.agent` nel tuo progetto |
| `ag-kit update` | Aggiorna all'ultima versione              |
| `ag-kit status` | Controlla lo stato dell'installazione     |

### Opzioni

```bash
ag-kit init --force        # Sovrascrive la cartella .agent esistente
ag-kit init --path ./myapp # Installa in una directory specifica
ag-kit init --branch dev   # Usa un branch specifico
ag-kit init --quiet        # Sopprime l'output (per CI/CD)
ag-kit init --dry-run      # Mostra un'anteprima senza eseguire modifiche
```

## Documentazione

- **[Esempio di Web App](https://antigravity-kit.unikorn.vn/docs/guide/examples/brainstorm)** - Guida passo-passo per creare un'applicazione web
- **[Documentazione Online](https://antigravity-kit.unikorn.vn/docs)** - Sfoglia tutta la documentazione online

## 🪨 Caveman Mode
Riduci l'uso dei token di circa il 65% con risposte concise e tecnicamente accurate.

### Utilizzo:
- Abilita: `/caveman on`
- Disabilita: `/caveman off`
- Livelli di intensità:
  - Lite: `/caveman lite`
  - Full (predefinito): `/caveman full`
  - Ultra: `/caveman ultra`

### Esempio:
```
Utente: /caveman on
AI: Modalità Caveman abilitata.

Utente: Spiega i React hooks.
AI: Gli hooks permettono ai componenti funzionali di usare stato e ciclo di vita. useState, useEffect, useContext. Nessuna classe necessaria.
```

### Benchmark:
- Riduzione dei token: 60-75%
- Precisione: 100% mantenuta
- Prestazioni: Nessun impatto sulla velocità

## Offrimi un caffè

<p align="center">
  <a href="https://buymeacoffee.com/vudovn">
    <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" />
  </a>
</p>

<p align="center"> - oppure - </p>

<p align="center">
  <img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Offrimi un caffè" width="200" />
</p>

## Licenza

MIT © Vudovn
