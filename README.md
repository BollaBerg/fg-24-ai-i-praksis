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

# Kjør word2vec

Last ned modellen med
```bash
python -m spacy download nb_core_news_lg
```

og kjør filen `word2vec.py`