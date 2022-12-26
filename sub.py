from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./free-trail-784533-c826d36fc23f.json"
import sm
import datetime

# TODO(developer)
project_id = "free-trail-784533"
subscription_id = "stock-monitor-sub"
# Number of seconds the subscriber should listen for messages
timeout = 300

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# count = 1
def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()
    print("timestamp: ", datetime.datetime.now().strftime("%H:%M:%S"))
    # count=count+1
    sm.get_latest_stock_zjc_disclosure()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
mainCount = 1
while True:
    print("mainCount: ", mainCount)
    mainCount = mainCount+1
    # with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result()
    except TimeoutError:
        # streaming_pull_future.cancel()  # Trigger the shutdown.
        # streaming_pull_future.result()  # Block until the shutdown is complete.
        print("timeout error!!~~")
