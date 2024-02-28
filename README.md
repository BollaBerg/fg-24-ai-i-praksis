# fg-24-ai-i-praksis
Arbeid for faggruppe AI i praksis

## Hvordan kjøre

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Sett opp token

Hentes fra App -> `OAuth & Permissions` -> `Bot User OAuth Token`

```bash
export SLACK_BOT_TOKEN=xxx
```

## Sett opp App-Level Token

Hentes fra App -> `Basic information` -> `App-Level Tokens` -> Velg en token du vil bruke

```bash
export SLACK_APP_LEVEL_TOKEN=xxx
```