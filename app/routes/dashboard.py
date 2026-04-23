from flask import render_template

from app.services.dashboard_analytics import analytics_for_dashboard


def dashboard_route(main_app):
    @main_app.route("/dashboard")
    def analytics():
        stats = analytics_for_dashboard()
        return render_template("dashboard.html", stats=stats), 200