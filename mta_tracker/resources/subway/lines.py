from flask_restful import Resource, reqparse, fields, marshal


line_fields = {
    'line': fields.String,
    'query_type': fields.String,
    
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
        line = args['line_name']

        return {"line":f'{line.upper()} uptime!'}

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
        line = args['line_name']
        
        return {"line":f'{line.upper()} status!'}