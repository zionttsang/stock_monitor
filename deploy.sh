gcloud functions deploy python-http-function \
--gen2 \
--runtime=python312 \
--region=REGION \
--source=. \
--entry-point=hello_get \
--trigger-http 

# test deploy
gcloud functions deploy stock-monitor2 \
--gen2 \
--runtime=python39 \
--region=us-west1 \
--source=. \
--entry-point=get_latest_stock_zjc_disclosure \
--env-vars-file .env.yaml \
--trigger-topic=stock-monitor

# pub msg to test
gcloud pubsub topics publish stock-monitor --message="any msg?"

# log read
gcloud functions logs read \
  --gen2 \
  --region=us-central1 \
  --limit=5 \
  tssyTopClickThreads