from datetime import datetime

from flask_restful import Resource, reqparse, fields, marshal

from mta_tracker.models import db, Lines

# All subway lines
allowed_lines = ['1','2','3','4','5','6','7','A','C','E','B','D','F','M','G',
                 'J','Z','N','Q','R','W','L','SIR','S']

response_fields = {
    'line': fields.String,
    'date': fields.String,
    'query_type': fields.String,
    'value': fields.String
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('line', type=str, required=True, 
help="No subway line provided.", location='args')

class LineUptime(Resource):
    
    def __init__(self):
        self.reqparse = reqparse
    
    def get(self):
        """
        Return the uptime (fraction of time not delayed) for a given subway 
        line.
        
        :param line: Name of subway line
        :return: Information related to uptime
        """
        args = self.reqparse.parse_args()
        line_name = args['line'].upper()
        line = Lines.query.filter_by(line=line_name).first_or_404()
        
        # Calculate uptime
        total_time = datetime.now() - line.created
        total_time = total_time.total_seconds() / 60
        uptime = 1 - (line.total_min_delayed / total_time)

        response = {
            'line': line.line,
            'date': datetime.now(),
            'query_type': "Uptime",
            'value': uptime
        }
        
        return {'response':marshal(response, response_fields)}

class LineStatus(Resource):
    def __init__(self):
        self.reqparse = reqparse
    
    def get(self):
        """
        Return the realtime delayed / on-time status of a subway line.

        :param line: Name of subway line
        :return: Information related to on-time/delayed status
        """
        args = self.reqparse.parse_args()
        line_name = args['line'].upper()
        line = Lines.query.filter_by(line=line_name).first_or_404()
        response = {
            'line': line.line,
            'date': datetime.now(),
            'query_type': "Status",
            'value': line.current_status
        }
        
        return {'response':marshal(response, response_fields)}