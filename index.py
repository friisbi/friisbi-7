import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = False
    
    # Se l'utente è loggato, mostra la home del reader
    if frappe.session.user != "Guest":
        frappe.redirect_to_message(
            title="Welcome to Friisbi Reader",
            message="Your personal RSS feed reader"
        )
    
    # Altrimenti mostra la landing page
    context.title = "Friisbi Reader"
    context.description = "RSS Feed Reader - Flipboard Style"
