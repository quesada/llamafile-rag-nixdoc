#!/bin/bash

# Load config and virtualenv
. .env
if [ -z "${VIRTUAL_ENV}" ]; then source venv/bin/activate; fi

mkdir logs

# Start llamafiles
echo "Starting llamafile servers..."

"models/embedding_model.llamafile" \
--server \
-ngl 9999 \
--nobrowser \
--port "${EMBEDDING_MODEL_PORT}" > logs/embedding_model.log 2>&1 &
pid=$!
sleep 5
err=$?
if [ "${err}" -ne 0 ]; then
  echo "Failed to start embedding model llamafile"
  exit 1
fi
echo "${pid}" > .pid_embedding_model
echo "started embedding model"

date
"models/generation_model.llamafile" \
--server \
-ngl 9999 \
--nobrowser \
--port "${GENERATION_MODEL_PORT}" > logs/generation_model.log 2>&1 &
pid=$!
sleep 5
err=$?
if [ "${err}" -ne 0 ]; then
  echo "Failed to start generation model llamafile"
  exit 1
fi
echo "${pid}" > .pid_generation_model
echo "started generation model"
date

# Run RAG app
python app.py "$@"

# Shut down the llamafiles
kill "$(cat .pid_embedding_model)"
kill "$(cat .pid_generation_model)"

echo "exited."
