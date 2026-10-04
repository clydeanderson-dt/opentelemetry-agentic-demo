#!/usr/bin/env bash
# Deploy the OpenTelemetry demo with one or more components swapped to branch-tagged images.
#
# Usage:
#   ./scripts/deploy-branch.sh <branch-name> <component> [component...]
#
# Examples:
#   ./scripts/deploy-branch.sh feature/new-agent agent
#   ./scripts/deploy-branch.sh feature/new-agent agent chatbot mcp
#
# All other components continue using the default 'latest' tag from values.yaml.
# To revert to all-latest after merging, re-deploy without overrides:
#   helm upgrade -n otel-agentic-demo otel-agentic-demo open-telemetry/opentelemetry-demo \
#     -f docs/deployment/values.yaml

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <branch-name> <component> [component...]"
  echo ""
  echo "Example: $0 feature/new-agent agent"
  exit 1
fi

BRANCH="$1"
shift
COMPONENTS=("$@")

NAMESPACE="otel-agentic-demo"
RELEASE="otel-agentic-demo"
CHART="open-telemetry/opentelemetry-demo"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VALUES="${SCRIPT_DIR}/../docs/deployment/values.yaml"

# Sanitize branch name — must match the CI sanitization in component-build-images.yml
SANITIZED_BRANCH=$(echo "$BRANCH" | sed 's/[^a-zA-Z0-9._-]/-/g' | sed 's/^[-.]*//' | cut -c1-80)

SET_FLAGS=()
for COMPONENT in "${COMPONENTS[@]}"; do
  # imageOverride.tag replaces the ENTIRE tag (the Helm chart does not append
  # the component suffix), so we must include it ourselves.
  TAG="${SANITIZED_BRANCH}-${COMPONENT}"
  SET_FLAGS+=(--set "components.${COMPONENT}.imageOverride.tag=${TAG}")
done

echo "Deploying with branch '${BRANCH}' (sanitized tag prefix: ${SANITIZED_BRANCH})"
echo "Overriding components: ${COMPONENTS[*]}"
for COMPONENT in "${COMPONENTS[@]}"; do
  echo "  ${COMPONENT} -> :${SANITIZED_BRANCH}-${COMPONENT}"
done
echo ""

helm upgrade --install -n "$NAMESPACE" "$RELEASE" "$CHART" \
  -f "$VALUES" \
  "${SET_FLAGS[@]}"
