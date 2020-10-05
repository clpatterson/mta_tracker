from flask_restful import Resource, reqparse, fields, marshal


line_fields = {
    'name': fields.String
}


#  TODO: Define reqparser

class LineUptime(Resource):
    
    def __init__(self):
        self.parser = None
    
    def get(self):
        """
        Return the uptime (fraction of time not delayed) for a given subway 
        line.
        
        :param line: Name of subway line
        :return: Information related to uptime
        """
        
        return {"line":'uptime!'}

class LineStatus(Resource):
    def __init__(self):
        self.parser = None
    
    def get(self):
        """
        Return the realtime delayed / on-time status of a subway line.

        :param line: Name of subway line
        :return: Information related to on-time/delayed status
        """
        
        return {"line":'status!'}