#!/usr/bin/python

# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0


import asyncio
import logging
import os

from arize.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
from openinference.instrumentation.mcp import MCPInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

tracer_provider = register()
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
MCPInstrumentor().instrument(tracer_provider=tracer_provider)
HTTPXClientInstrumentor().instrument()

from src.agents.agents import Agent
from src.agents.feature_flags import init_feature_flags

logging.basicConfig(level=logging.INFO)

init_feature_flags()

async def start_servers():
    """Run the LangGraph Agent server"""
    agent = Agent()
    FastAPIInstrumentor.instrument_app(agent.app)
    await agent.launch()


if __name__ == "__main__":
    try:
        asyncio.run(start_servers())
    except KeyboardInterrupt:
        logging.info("Shutting down servers...")
