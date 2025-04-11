from commandflow.commands.base import StepCommand
from commandflow.core import QueueCommands
from config import get_db, logger
from plugins.schedules.models import ScheduleBase, UserScheduleBase


@QueueCommands.register
class PrintHello(StepCommand):

    async def run(self, message, state, **context):
        await message.answer("Hello, World!")
        await self.next()



@QueueCommands.register
class Create(StepCommand):
    async def run(self, message, state, **context):
        try: 
            name = context.get("schedule_name")
            user_id = context.get("user_id")
        except Exception as e:
            logger.error(f"Can't get data from context: {e}")
            return
        

        db = next(get_db())
        schedule = ScheduleBase(name = name)
        try:
            db.add(schedule)
            db.commit()
            schedule_id = schedule.id
        except Exception as e:
            logger.error(f"Can't create schedule: {e}")
        try:
            user_schedule = UserScheduleBase(user_id = user_id, schedule_id = schedule.id)
            db.add(user_schedule)
            db.commit()
            await self.next()
        except Exception as e:
            logger.error(f"Can't create user_schedule: {e}")


@QueueCommands.register
class Update(StepCommand):
    async def run(self, message, state, **context):
        try: 
            schedule_id = context.get("schedule_id")
            name = context.get("schedule_name")
        except Exception as e:
            logger.error(f"Can't get data from context: {e}")
            return
    
        db = next(get_db())
        
        try:
            db.query(ScheduleBase).filter(ScheduleBase.id == schedule_id).update({"name": name})
            db.commit()
            await self.next()
        except Exception as e:
            logger.error(f"Can't create schedule: {e}")
       
@QueueCommands.register
class Delete(StepCommand):
    async def run(self, message, state, **context):
        try: 
            schedule_id = context.get("schedule_id")
        except Exception as e:
            logger.error(f"Can't get data from context: {e}")
            return
    
        db = next(get_db())
        
        try:
            db.query(ScheduleBase).filter(ScheduleBase.id == schedule_id).delete()
            db.commit()
            await self.next()
        except Exception as e:
            logger.error(f"Can't create schedule: {e}")
       