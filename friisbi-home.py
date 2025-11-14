import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = False
    
    # Get user's subscribed feeds
    if frappe.session.user != "Guest":
        subscriptions = frappe.get_all(
            "Friisbi User Subscription",
            filters={"user": frappe.session.user},
            fields=["feed", "magazine"]
        )
        context.subscriptions = subscriptions
    else:
        context.subscriptions = []
    
    # Get recent posts
    posts = frappe.get_all(
        "Friisbi Post",
        filters={"published": 1},
        fields=["name", "title", "description", "link", "published_date", "feed", "image"],
        order_by="published_date desc",
        limit=20
    )
    context.posts = posts
    
    # Get available feeds
    feeds = frappe.get_all(
        "Friisbi Feed",
        filters={"active": 1},
        fields=["name", "title", "url", "category", "description"],
        order_by="title"
    )
    context.feeds = feeds
    
    context.title = "Friisbi Home"
    context.is_logged_in = frappe.session.user != "Guest"
