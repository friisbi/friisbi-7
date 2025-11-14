import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = False
    
    # Get all active feeds grouped by category
    feeds = frappe.get_all(
        "Friisbi Feed",
        filters={"active": 1},
        fields=["name", "title", "url", "category", "description", "feed_image"],
        order_by="category, title"
    )
    
    # Group feeds by category
    feeds_by_category = {}
    for feed in feeds:
        category = feed.category or "Uncategorized"
        if category not in feeds_by_category:
            feeds_by_category[category] = []
        feeds_by_category[category].append(feed)
    
    context.feeds_by_category = feeds_by_category
    context.total_feeds = len(feeds)
    context.title = "Feed Catalog"
    context.is_logged_in = frappe.session.user != "Guest"
