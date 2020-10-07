from mta_tracker.extensions import db

class Lines(db.Model):
    __tablename__ = 'lines'
    line = db.Column(db.String, primary_key=True)
    current_status = db.Column(db.String, nullable=False)
    total_min_delayed = db.Column(db.Integer, nullable=False) 
    created = db.Column(db.DateTime, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Line {self.line}>'
    
    def add_line(self):
        db.session.add(self)
        db.session.commit()

class Delays(db.Model):
    __tablename__ = 'delays'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    delayed_lines = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Delay {self.time}>'
    
    def add_delay(self):
        db.session.add(self)
        db.session.commit()