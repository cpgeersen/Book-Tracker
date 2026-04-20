import json

from flask import request, render_template, redirect, url_for

from app.services.mediator import read, update, delete


def settings_route(main_app):
    @main_app.route('/settings', methods=['GET', 'POST'])
    def settings_page():
        if request.method == 'GET':
            user_settings_values = read({}, 'user-settings')
            return render_template('new_settings.html', user_settings=user_settings_values), 200
        else: # Implicit POST
            user_action = dict(request.form)
            print(user_action)
            user_settings_values = read({}, 'user-settings')

            if user_action.get('Update') is not None:
                response = update(json.dumps(user_action), 'user-settings')

            if user_action.get('CSV') is not None:
                pass

            if user_action.get('Delete_Database') is not None:
                print('here')
                delete_status = delete({}, 'delete-database')
                return render_template('new_settings_delete_status_modal.html',
                                       user_settings=user_settings_values, delete_status=delete_status), 200

            if user_action.get('Delete_Cover-Images') is not None:
                pass

            if user_action.get('Dedupe') is not None:
                return redirect(url_for('dedup_page'))

            return render_template('new_settings.html', user_settings=user_settings_values), 200