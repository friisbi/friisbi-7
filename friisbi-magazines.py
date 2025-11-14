import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = False
    
    # Get all magazines
    magazines = frappe.get_all(
        "Friisbi Magazine",
        fields=["name", "title", "description", "created_by", "creation", "is_public"],
        order_by="creation desc"
    )
    
    # For each magazine, get feed count
    for magazine in magazines:
        feeds_count = frappe.db.count(
            "Friisbi Magazine Feed",
            filters={"parent": magazine.name}
        )
        magazine.feeds_count = feeds_count
    
    context.magazines = magazines
    context.title = "Magazines"
    context.is_logged_in = frappe.session.user != "Guest"
