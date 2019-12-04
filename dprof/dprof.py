from flask import Flask, request, make_response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import pandas as pd
import numpy as np
import pandas_profiling

db_connect = create_engine('sqlite:///dprof.db', echo="debug")
app = Flask(__name__)
api = Api(app)

class TableStatistic(Resource):
    def get(self):
        df = pd.read_sql_query('select * from test',db_connect.connect())
        profile = df.profile_report(title='Pandas Profiling Report', plot={'histogram': {'bins': 8}})
        profile.to_file(output_file="output.html")
        with open('output.html', encoding='utf-8') as report:
            data=report.read()
        return make_response(data,200)

api.add_resource(TableStatistic, '/tablestatistic')

if __name__ == '__main__':
    app.run(port='5000')
