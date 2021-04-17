# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import yaml
from flask import redirect, request, jsonify, render_template, url_for, \
    make_response, session
from flask import Flask
from flask_jsonlocale import Locales
import pymysql

app = Flask(__name__, static_folder='../static')
__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, os.environ.get(
        'FLASK_CONFIG_FILE', 'config.yaml')))))
locales = Locales(app)
_ = locales.get_message

def connect():
    return pymysql.connect(
        database=app.config.get('DB_NAME', 'global_user_activity'),
        host=app.config.get('DB_HOST', 'localhost'),
        user=app.config.get('DB_USER'),
        password=app.config.get('DB_PASS'),
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userinfo')
def userinfo():
    username = request.args.get('username')

    graphType = request.args.get('type')
    if graphType == 'undos':
        return render_template('graph_undos.html', username=username)
    else:
        return render_template('graph_unknown.html')

@app.route('/api/userinfo/undos/<path:user_raw>.json')
def api_userinfo(user_raw):
    user = user_raw.replace('_', ' ')
    conn = connect()
    with conn.cursor() as cur:
        cur.execute('''
        SELECT
            LEFT(rev_timestamp, 6),
            ctd_name,
            COUNT(*)
        FROM undos
        WHERE
            actor_name=%s
        GROUP BY
            LEFT(rev_timestamp, 6),
            ctd_name
        ORDER BY rev_timestamp DESC''', (user, ))
        dataByTime = cur.fetchall()
    byTime = {}
    for row in dataByTime:
        if row[0] not in byTime:
            byTime[row[0]] = {}
        byTime[row[0]][row[1]] = row[2]
    
    for month in byTime:
        byTime[month]['total'] = sum([byTime[month][x] for x in byTime[month]])

        for tag in ['mw-rollback', 'mw-undo']:
            if tag not in byTime[month]:
                byTime[month][tag] = 0
    return jsonify({
        'user': user,
        'byTime': byTime
    })

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
