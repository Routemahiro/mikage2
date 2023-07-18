from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TimerTask(Base):
    __tablename__ = 'timer_task'

    id = Column(Integer, primary_key=True)
    timer_id = Column(Integer, ForeignKey('timer.timer_id'), nullable=False)
    task_id = Column(Integer, ForeignKey('task.task_id'), nullable=False)

    def __repr__(self):
        return f'<TimerTask(id={self.id}, timer_id={self.timer_id}, task_id={self.task_id})>'
