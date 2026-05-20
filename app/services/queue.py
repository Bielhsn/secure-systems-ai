from queue import Queue

job_queue = Queue()

def add_job(job):
    job_queue.put(job)

def get_job():
    if not job_queue.empty():
        return job_queue.get()
    return None