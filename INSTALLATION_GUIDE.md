# Guida Installazione Friisbi Reader

Questa guida spiega come caricare l'app su GitHub e installarla sul tuo server Frappe.

## Passo 1: Carica su GitHub

1. **Crea un nuovo repository su GitHub**
   - Vai su https://github.com/new
   - Nome repository: `friisbi`
   - Descrizione: "RSS Feed Reader for Frappe v16"
   - Pubblico o Privato (a tua scelta)
   - Non aggiungere README, .gitignore, o license (sono già inclusi)

2. **Carica il codice**
   ```bash
   cd friisbi/
   git init
   git add .
   git commit -m "Initial commit - Friisbi Reader v0.0.1"
   git branch -M main
   git remote add origin https://github.com/TUO_USERNAME/friisbi.git
   git push -u origin main
   ```

3. **Crea un tag per la versione**
   ```bash
   git tag v0.0.1
   git push origin v0.0.1
   ```

## Passo 2: Installa sul Server Frappe

### Via SSH/Bench (Consigliato)

```bash
# Connettiti al tuo server Frappe
ssh user@your-server.com

# Vai nella directory bench
cd /path/to/frappe-bench

# Scarica l'app da GitHub
bench get-app https://github.com/TUO_USERNAME/friisbi.git

# Installa l'app sul tuo sito
bench --site YOUR_SITE_NAME install-app friisbi

# Riavvia bench
bench restart
```

### Via Frappe Press Marketplace

1. **Pubblica su Marketplace**
   - Vai su https://frappecloud.com/marketplace
   - Click "Submit App"
   - Compila il form:
     - App Name: Friisbi Reader
     - Repository: https://github.com/TUO_USERNAME/friisbi.git
     - Branch: main
     - Category: Content Management
   - Submit

2. **Installa dal Marketplace**
   - Dashboard Frappe Press → tuo sito → Apps
   - Search "Friisbi Reader"
   - Click "Install"

## Passo 3: Verifica Installazione

1. **Accedi al tuo sito Frappe**

2. **Verifica DocTypes esistenti**
   - Assicurati che questi DocTypes esistano già:
     - Friisbi Feed
     - Friisbi Post
     - Friisbi Subscription

3. **Testa la sincronizzazione**
   ```python
   # Apri Frappe Console (Desk → Developer → Console)
   
   # Testa preview di un feed
   frappe.call('friisbi.api.get_feed_preview', 
               url='https://feeds.bbci.co.uk/news/rss.xml')
   
   # Crea un feed di test
   feed = frappe.get_doc({
       'doctype': 'Friisbi Feed',
       'title': 'BBC News',
       'url': 'https://feeds.bbci.co.uk/news/rss.xml'
   })
   feed.insert()
   
   # Sincronizza il feed
   frappe.call('friisbi.api.sync_feed', feed_name=feed.name)
   ```

4. **Verifica Scheduler**
   ```bash
   # Sul server
   bench enable-scheduler
   
   # Verifica che sia attivo
   bench --site YOUR_SITE_NAME scheduler status
   ```

## Passo 4: Configurazione Finale

1. **Permessi**
   - Setup → Role Permission Manager
   - Assicurati che:
     - Tutti possono leggere Friisbi Feed
     - Tutti possono leggere Friisbi Post
     - Users possono creare/modificare Friisbi Subscription

2. **Homepage**
   - La homepage `/friisbi-home` dovrebbe già funzionare
   - La registrazione `/friisbi-signup` dovrebbe già funzionare

3. **Monitoraggio**
   - Error Log: Frappe Desk → Error Log (per vedere eventuali errori di sync)
   - Scheduled Jobs: Desk → Scheduled Job Type (per vedere quando girano i sync)

## Risoluzione Problemi

### Errore: "Module 'feedparser' not found"

```bash
bench --site YOUR_SITE_NAME pip install feedparser
bench restart
```

### Scheduler non funziona

```bash
bench enable-scheduler
bench --site YOUR_SITE_NAME set-config enable_scheduler 1
bench restart
```

### Feed non si sincronizzano

1. Verifica Error Log
2. Testa manualmente dalla console
3. Controlla che l'URL del feed sia accessibile

## Aggiornamenti Futuri

Quando fai modifiche all'app:

```bash
# Sul server
cd /path/to/frappe-bench
bench get-app friisbi --branch main
bench --site YOUR_SITE_NAME migrate
bench restart
```

## Supporto

Per problemi o domande, apri un issue su GitHub:
https://github.com/TUO_USERNAME/friisbi/issues
