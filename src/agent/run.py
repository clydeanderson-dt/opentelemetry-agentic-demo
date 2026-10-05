#!/usr/bin/python

# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0



import asyncio
import logging

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

from arize.otel import register  # noqa: E402
from openinference.instrumentation.langchain import LangChainInstrumentor  # noqa: E402

tracer_provider = register(project_name="opentelemetry-agentic-demo")
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

from src.agents.agents import Agent  # noqa: E402
from src.agents.feature_flags import init_feature_flags  # noqa: E402

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
