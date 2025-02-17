# OTEL GRPC reconnect problem repro repo

## GRPC (reconnect does not work)

1. ```bash
    # Run GRPC export based service 
    docker compose up common-experiments-agent-wc2-grpc
   ```
2. ```bash
    # Call service
    curl localhost:9293 
   ```

3. ```bash
    # Stop collector
    docker compose stop common-otel-collector
   ```

4. ```bash
    # Call service
    curl localhost:9293 
   ```

5. ```bash
    # Check logs (errors about collector down)
    docker compose logs common-experiments-agent-wc2-grpc
   ```

6. ```bash
    # Run collector again
    docker compose up common-otel-collector
   ```
7. ```bash
    # Call service
    curl localhost:9293 
   ```

8. ```bash
    # Check logs (errors are still here and you must restart service)
    docker compose logs common-experiments-agent-wc2-grpc
   ```

9. ```bash
    # Check new metrics from collector (no new metrics)
    curl localhost:8889/metrics
   ```

## HTTP (reconnect work)

1. ```bash
    # Run HTTP export based service 
    docker compose up common-experiments-agent-wc1-http
   ```
2. ```bash
    # Call service
    curl localhost:9292 
   ```

3. ```bash
    # Stop collector
    docker compose stop common-otel-collector
   ```

4. ```bash
    # Call service
    curl localhost:9292 
   ```

5. ```bash
    # Check logs (errors about collector down)
    docker compose logs common-experiments-agent-wc1-http
   ```

6. ```bash
    # Run collector again
    docker compose up common-otel-collector
   ```
7. ```bash
    # Call service
    curl localhost:9292 
   ```

8. ```bash
    # Check logs (errors are gone)
    docker compose logs common-experiments-agent-wc1-http
   ```

9. ```bash
    # Check new metrics from collector
    curl localhost:8889/metrics
   ```