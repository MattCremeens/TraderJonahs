To force a cloud run:

gcloud run jobs execute traderjonahs \
  --region=us-central1 \
  --wait

To deploy to the cloud, run:

gcloud run jobs deploy traderjonahs \
  --source . \
  --region us-central1 \
  --set-secrets ALPACA_API_KEY=ALPACA_API_KEY:latest,ALPACA_SECRET_KEY=ALPACA_SECRET_KEY:latest,TAVILY_API_KEY=TAVILY_API_KEY:latest,GOOGLE_API_KEY=GOOGLE_API_KEY:latest,LANGSMITH_TRACING=LANGSMITH_TRACING:latest,LANGSMITH_ENDPOINT=LANGSMITH_ENDPOINT:latest,LANGSMITH_PROJECT=LANGSMITH_PROJECT:latest,LANGSMITH_API_KEY=LANGSMITH_API_KEY:latest