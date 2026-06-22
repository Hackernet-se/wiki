# Winget - Windows Package Manager

Winget är Microsofts officiella pakethanterare för Windows. Det gör det möjligt att installera, uppdatera och hantera programvara own via kommandoraden.

## Installation av program

För att installera ett program använder du kommandot `winget install`.

```bash
winget install <program//id>
```

**Exempel:**
För att installera Google Chrome:
```bash
winget install Google.Chrome
```

## Uppdatering av program

För att uppdatera alla installerade program som har tillgängliga uppdateringar, använd kommandot `winget upgrade --all`.

```bash
winget upgrade --all
```

## Andra användbara kommandon

| Kommando | Beskrivning |
| --- | --- |
| `winget search <sökord>` | Söker efter ett program i winget-biblioteket |
| `winget list` | Listar alla installerade program som kan hanteras av winget |
| `winget uninstall <program>` | Avinstallerar ett program |

## Tips
- Om du är osäker på det exakta ID:t för ett program, använd `winget search` för att hitta det.
- Kör kommandoraden (PowerShell eller CMD) som administratör för att undvika rättighetsfel vid installation.