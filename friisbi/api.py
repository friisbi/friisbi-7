import frappe
import feedparser
from datetime import datetime
from frappe import _


@frappe.whitelist()
def sync_feed(feed_name):
    """
    Synchronize a single RSS feed by parsing its URL and creating posts.
    
    Args:
        feed_name: Name of the Friisbi Feed doctype record
    
    Returns:
        dict: Summary of sync operation
    """
    feed = frappe.get_doc("Friisbi Feed", feed_name)
    
    if not feed.url:
        frappe.throw(_("Feed URL is required"))
    
    try:
        # Parse RSS feed
        parsed_feed = feedparser.parse(feed.url)
        
        if parsed_feed.bozo:
            # Feed has parsing errors but might still be usable
            frappe.log_error(
                f"RSS parsing warning for {feed.url}: {parsed_feed.bozo_exception}",
                "Friisbi RSS Parsing Warning"
            )
        
        new_posts_count = 0
        skipped_count = 0
        
        # Process each entry in the feed
        for entry in parsed_feed.entries:
            # Get required fields
            title = entry.get('title', 'Untitled')
            link = entry.get('link', '')
            
            if not link:
                skipped_count += 1
                continue
            
            # Check if post already exists
            existing_post = frappe.db.exists('Friisbi Post', {'link': link})
            
            if existing_post:
                skipped_count += 1
                continue
            
            # Get optional fields
            summary = entry.get('summary', entry.get('description', ''))
            published_date = None
            
            # Try to parse published date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    published_date = datetime(*entry.published_parsed[:6])
                except:
                    pass
            
            # Create new post
            post = frappe.get_doc({
                'doctype': 'Friisbi Post',
                'title': title,
                'link': link,
                'content': summary[:500] if summary else '',  # Limit content length
                'feed': feed_name,
                'published_date': published_date or datetime.now()
            })
            
            post.insert(ignore_permissions=True)
            new_posts_count += 1
        
        frappe.db.commit()
        
        return {
            'success': True,
            'feed': feed_name,
            'new_posts': new_posts_count,
            'skipped': skipped_count,
            'total_entries': len(parsed_feed.entries)
        }
        
    except Exception as e:
        frappe.log_error(
            f"Error syncing feed {feed_name}: {str(e)}",
            "Friisbi Feed Sync Error"
        )
        return {
            'success': False,
            'feed': feed_name,
            'error': str(e)
        }


@frappe.whitelist()
def sync_all_feeds():
    """
    Synchronize all active RSS feeds.
    Called by scheduler (hourly) or manually.
    
    Returns:
        dict: Summary of all sync operations
    """
    feeds = frappe.get_all('Friisbi Feed', fields=['name', 'title', 'url'])
    
    results = {
        'total_feeds': len(feeds),
        'successful': 0,
        'failed': 0,
        'total_new_posts': 0,
        'details': []
    }
    
    for feed in feeds:
        result = sync_feed(feed.name)
        
        if result.get('success'):
            results['successful'] += 1
            results['total_new_posts'] += result.get('new_posts', 0)
        else:
            results['failed'] += 1
        
        results['details'].append(result)
    
    return results


@frappe.whitelist()
def get_feed_preview(url):
    """
    Preview an RSS feed before adding it (for testing).
    
    Args:
        url: RSS feed URL to preview
    
    Returns:
        dict: Feed information and sample entries
    """
    try:
        parsed_feed = feedparser.parse(url)
        
        if parsed_feed.bozo:
            return {
                'success': False,
                'error': f"Feed parsing error: {parsed_feed.bozo_exception}"
            }
        
        feed_info = {
            'title': parsed_feed.feed.get('title', 'Unknown'),
            'description': parsed_feed.feed.get('description', ''),
            'link': parsed_feed.feed.get('link', ''),
            'entry_count': len(parsed_feed.entries)
        }
        
        # Get first 5 entries as preview
        sample_entries = []
        for entry in parsed_feed.entries[:5]:
            sample_entries.append({
                'title': entry.get('title', 'Untitled'),
                'link': entry.get('link', ''),
                'published': entry.get('published', '')
            })
        
        return {
            'success': True,
            'feed_info': feed_info,
            'sample_entries': sample_entries
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
