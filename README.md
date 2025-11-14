# Friisbi Reader

A Flipboard-style RSS feed reader for Frappe v16 with multi-user support, personalized feed subscriptions, and automatic RSS synchronization.

## Features

- 📰 **RSS Feed Parsing**: Automatic synchronization from any RSS/Atom feed
- 👥 **Multi-User Support**: Each user can subscribe to their own feeds
- 🔄 **Auto Sync**: Hourly background synchronization of all feeds
- 🎨 **Flipboard-style UI**: Modern, card-based interface
- 🔐 **User Registration**: Public registration with automatic approval
- 📱 **Responsive**: Works on desktop, tablet, and mobile

## Installation

### Prerequisites

- Frappe v16 or higher
- Python 3.10+
- Access to Frappe Bench CLI

### Install via Bench

```bash
# Get the app from GitHub
bench get-app https://github.com/YOUR_USERNAME/friisbi.git

# Install app on your site
bench --site YOUR_SITE install-app friisbi

# Restart bench
bench restart
```

### Install via Frappe Press Marketplace

1. Go to your Frappe Press dashboard
2. Navigate to Marketplace
3. Search for "Friisbi Reader"
4. Click "Install App"
5. Select your site
6. Click "Install"

## Configuration

### Required DocTypes

The app requires these DocTypes to be created in your Frappe site:

1. **Friisbi Feed**
   - title (Data)
   - url (Data)
   - category (Data, optional)

2. **Friisbi Post**
   - title (Data)
   - link (Data)
   - content (Text Editor)
   - feed (Link to Friisbi Feed)
   - published_date (Datetime)

3. **Friisbi Subscription**
   - user (Link to User)
   - feed (Link to Friisbi Feed)

### Permissions

Ensure the following permissions are set:

- **Friisbi Feed**: All users can read
- **Friisbi Post**: All users can read
- **Friisbi Subscription**: Users can create/read/update/delete their own subscriptions

## Usage

### For End Users

1. **Register**: Visit `/friisbi-signup` to create an account
2. **Browse Feeds**: Go to `/friisbi-home` to see posts from your subscribed feeds
3. **Add Feeds**: Use the "Aggiungi Feed" button to subscribe to new RSS feeds
4. **Infinite Scroll**: Scroll down to load more posts automatically

### For Administrators

#### Manual Sync

To manually trigger feed synchronization:

```python
# In Frappe console
frappe.call('friisbi.api.sync_all_feeds')
```

Or sync a specific feed:

```python
frappe.call('friisbi.api.sync_feed', feed_name='FEED_NAME')
```

#### Preview Feed

To test an RSS feed before adding:

```python
frappe.call('friisbi.api.get_feed_preview', url='https://example.com/feed.xml')
```

### Automatic Synchronization

The app automatically syncs all feeds **every hour** via Frappe's scheduler. No manual intervention required.

To change sync frequency, edit `hooks.py`:

```python
scheduler_events = {
    "hourly": [  # Change to "daily", "weekly", etc.
        "friisbi.api.sync_all_feeds"
    ],
}
```

## API Methods

All API methods are whitelisted and can be called via REST API:

### `sync_feed(feed_name)`

Sync a single feed.

**Parameters:**
- `feed_name`: Name of Friisbi Feed document

**Returns:**
```json
{
  "success": true,
  "feed": "FEED_NAME",
  "new_posts": 10,
  "skipped": 5,
  "total_entries": 15
}
```

### `sync_all_feeds()`

Sync all feeds.

**Returns:**
```json
{
  "total_feeds": 5,
  "successful": 5,
  "failed": 0,
  "total_new_posts": 42,
  "details": [...]
}
```

### `get_feed_preview(url)`

Preview a feed before subscribing.

**Parameters:**
- `url`: RSS feed URL

**Returns:**
```json
{
  "success": true,
  "feed_info": {
    "title": "Example Blog",
    "description": "A blog about...",
    "entry_count": 20
  },
  "sample_entries": [...]
}
```

## Development

### Project Structure

```
friisbi/
├── friisbi/
│   ├── __init__.py
│   ├── hooks.py          # App configuration and scheduler
│   ├── api.py            # RSS sync API methods
│   ├── config/           # Desk configuration
│   └── public/           # Static assets
├── setup.py              # Python package setup
├── requirements.txt      # Python dependencies
└── README.md
```

### Dependencies

- `frappe`: Frappe Framework
- `feedparser>=6.0.10`: RSS/Atom feed parsing

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Publishing to Frappe Press Marketplace

### Preparation

1. **Update Version**: Edit `friisbi/__init__.py` and bump version
2. **Tag Release**: Create a git tag matching the version
   ```bash
   git tag v0.0.1
   git push origin v0.0.1
   ```

3. **GitHub Release**: Create a release on GitHub with changelog

### Submit to Marketplace

1. Go to [Frappe Press Marketplace](https://frappecloud.com/marketplace)
2. Click "Submit App"
3. Fill in the form:
   - **App Name**: Friisbi Reader
   - **Repository URL**: Your GitHub repo URL
   - **Branch**: `main` or `master`
   - **Description**: Short description from above
   - **Category**: Content Management / Social
   - **License**: MIT
   - **Screenshots**: Add screenshots of the app
4. Submit for review

### Marketplace Guidelines

- Ensure all dependencies are in `requirements.txt`
- Include clear installation instructions
- Add screenshots showing key features
- Write comprehensive documentation
- Test on a clean Frappe v16 site before submitting

## Troubleshooting

### Feeds Not Syncing

1. Check Error Log: Go to Frappe Desk → Error Log
2. Verify feed URL is valid and accessible
3. Check scheduler is enabled: `bench enable-scheduler`
4. Manually trigger sync to see errors

### Posts Not Appearing

1. Verify user has subscriptions: Check `Friisbi Subscription` doctype
2. Check posts exist: Go to `Friisbi Post` list
3. Verify permissions on DocTypes

### Import Errors

Ensure `feedparser` is installed:
```bash
bench --site YOUR_SITE pip install feedparser
```

## License

MIT License - see LICENSE.txt

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Credits

Developed for Frappe v16 ecosystem.
