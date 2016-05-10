from apscheduler.scheduler import Scheduler

sched = Scheduler()

@sched.interval_schedule(hours=1)
def some_job():
    print "Decorated job"

sched.configure(options_from_ini_file)
sched.start()