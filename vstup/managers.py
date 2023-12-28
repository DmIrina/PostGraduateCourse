from django.db import models

class ElectronicQueueManager(models.Manager):
    def create_slots(self, start_date, end_date, work_hours, launch_hour, weekends, hollydays):
        print(' - ')
        slots = []
        for day in range((end_date - start_date).days + 1):
            current_date = start_date + datetime.timedelta(days=day)
            if current_date.weekday not in weekends and current_date not in hollydays:
                for hour in work_hours:
                    if hour != launch_hour:
                        for minute in range(0,60,5):
                            timing_datetime = datetime.datetime.combine(current_date, datetime.time(hour, minute))
                            print(timing_datetime)
                            slots.append(self.create(datetime=timing_datetime))
        slots.append(self.create(datetime=start_date))
        slots.append(self.create(datetime=end_date))

        return slots
