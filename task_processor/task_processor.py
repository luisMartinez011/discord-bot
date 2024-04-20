
def lambda_handler(event, context):

    taskScheduler = TaskScheduler('DSJFJF0')
    taskScheduler.upload_to_database()
