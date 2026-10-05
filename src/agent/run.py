#!/usr/bin/python

# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0


import asyncio
import logging
import os

from arize.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

from src.agents.agents import Agent
from src.agents.feature_flags import init_feature_flags

logging.basicConfig(level=logging.INFO)

tracer_provider = register()
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

init_feature_flags()

async def start_servers():
    """Run the LangGraph Agent server"""
    agent = Agent()
    await agent.launch()


if __name__ == "__main__":
    try:
        asyncio.run(start_servers())
    except KeyboardInterrupt:
        logging.info("Shutting down servers...")
