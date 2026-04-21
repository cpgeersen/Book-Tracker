import json
import os
from pathlib import Path

from flask import request, render_template, redirect, url_for

from app.services.mediator import read, update, delete
from app.services.user_settings.export_import import export_database_to_csv, import_database_from_csv

def settings_route(main_app):
    @main_app.route('/settings', methods=['GET', 'POST'])
    def settings_page():
        if request.method == 'GET':
            user_settings_values = read({}, 'user-settings')
            return render_template('settings/settings.html', user_settings=user_settings_values), 200
        else: # Implicit POST
            user_action = dict(request.form)
            user_settings_values = read({}, 'user-settings')

            if user_action.get('Update') is not None:
                response = update(json.dumps(user_action), 'user-settings')
                user_settings_values = read({}, 'user-settings')
                return render_template('settings/settings.html', user_settings=user_settings_values), 200

            if user_action.get('CSV_Export') is not None:
                response = export_database_to_csv()

                return render_template('settings/settings_export_import_modal.html',
                                       user_settings=user_settings_values, csv_status=response), 200

            if user_action.get('CSV_Import') is not None:
                file = request.files['CSV_Import']
                filename = str(file.filename)
                file_extension = file.content_type.split('/')[-1]

                if file_extension != 'csv':
                    return render_template('settings/settings_export_import_modal.html',
                                           user_settings=user_settings_values,
                                           csv_status={'Status': 'Failure',
                                                       'Message': 'File not supported. Must be a CSV'}), 200

                upload_folder = os.path.join("app", "data", "backups")
                file_path = os.path.join(upload_folder, Path(filename))
                file.save(file_path)
                response = import_database_from_csv(file_path, 'RESET')

                return render_template('settings/settings_export_import_modal.html',
                                       user_settings=user_settings_values, csv_status=response), 200

            if user_action.get('Delete_Database') is not None:
                delete_status = delete({}, 'delete-database')
                return render_template('settings/settings_delete_status_modal.html',
                                       user_settings=user_settings_values, delete_status=delete_status), 200

            if user_action.get('Delete_Cover_Images') is not None:
                delete_status = delete({}, 'all-cover-images')
                return render_template('settings/settings_delete_status_modal.html',
                                       user_settings=user_settings_values, delete_status=delete_status), 200

            if user_action.get('Dedupe') is not None:
                return redirect(url_for('dedup_page'))

            return render_template('settings/settings.html', user_settings=user_settings_values), 200