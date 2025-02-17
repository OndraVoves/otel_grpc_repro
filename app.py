import logging
import os

import opentelemetry.sdk.resources as otel_resources
from fastapi import FastAPI
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter as OTLPMetricExporterGRPC
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as OTLPMetricExporterHTTP
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

SERVICE_NAME = os.getenv("SERVICE_NAME")

HTTP_OR_GRPC = os.getenv("HTTP_OR_GRPC")

ENDPOINT_GRPC = "http://common-otel-collector:4317"
ENDPOINT_HTTP = "http://common-otel-collector:4318/v1/metrics"

app = FastAPI()

resource = Resource(
    attributes={
        otel_resources.SERVICE_NAME: SERVICE_NAME,
    }
)


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

###########
# Metrics #
###########
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporterGRPC(endpoint=ENDPOINT_GRPC) if HTTP_OR_GRPC == "grpc" else OTLPMetricExporterHTTP(endpoint=ENDPOINT_HTTP),
    export_interval_millis=10_000,

)
metrics_provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
metrics.set_meter_provider(metrics_provider)

# Creates a meter from the global meter provider
meter = metrics.get_meter(SERVICE_NAME, meter_provider=metrics_provider)

# create metric
meth_metric = meter.create_counter("meth", "crystal", "NO POLICE!!!")

####################################
# Instrumentation a.k.a time-saver #
####################################
FastAPIInstrumentor().instrument_app(app)
AioHttpClientInstrumentor().instrument()

@app.get("/")
async def index():
    logging.warning("INDEX INDEX INDEX")
    meth_metric.add(1)
    return "FOOO"
