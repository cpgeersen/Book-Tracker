from flask import render_template

from app.services.dashboard_analytics import analytics_for_dashboard
from app.services.mediator import read


def dashboard_route(main_app):
    @main_app.route("/dashboard")
    def analytics():
        stats = analytics_for_dashboard()
        user_settings_values = read({}, 'user-settings')
        return render_template("dashboard.html", stats=stats,
                               user_settings=user_settings_values), 200