# DevOps SRE Agentic AI Agent

## Overview

This DevOps SRE AI Agent leverages advanced AI reasoning models through **LiteLLM** to power autonomous debugging and troubleshooting of production-grade systems. The unified LiteLLM interface allows you to use any reasoning-capable LLM (Claude, GPT-4, Gemini, or others) as the core intelligence engine, providing flexibility in model selection based on your needs.

## Why AI Reasoning for DevOps/SRE?

### 1. **Advanced Reasoning & Problem-Solving**

Modern reasoning models excel at:

- Analyzing complex system logs and metrics
- Identifying root causes from distributed symptoms
- Generating actionable troubleshooting steps
- Understanding relationships between infrastructure components

### 2. **Multi-Agent Orchestration**

The AI orchestrator coordinates multiple specialized agents:

- **Observability Agent**: Analyzes Grafana metrics and alerts
- **Infrastructure Agent**: Queries Kubernetes cluster state
- **Knowledge Agent**: Searches Stack Overflow for solutions
- **Incident Agent**: Manages ServiceNow tickets
- **Code Agent**: Interfaces with GitHub for issues/PRs

### 3. **Context Understanding**

AI reasoning maintains awareness of:

- Current system state across multiple tools
- Historical incident patterns
- Best practices for cloud-native troubleshooting
- Security considerations in production environments

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│         AI Reasoning Engine (Orchestrator)          │
│            via LiteLLM Unified Interface            │
│     (Claude / GPT-4 / Gemini / Local Models)        │
│                                                     │
└──────────────┬──────────────────────────────────────┘
               │
               │ Coordinates & Reasons
               │
    ┌──────────┼──────────┬──────────┬──────────┐
    │          │          │          │          │
    ▼          ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Grafana │ │  K8s   │ │ Stack  │ │Service │ │ GitHub │
│  MCP   │ │  MCP   │ │Overflow│ │  Now   │ │  MCP   │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
```

## LiteLLM: Unified AI Interface

LiteLLM provides a single, consistent interface to 100+ LLM providers, allowing you to:

- Switch between models without code changes
- Compare model performance for your specific use cases
- Implement fallback strategies
- Optimize costs by using different models for different tasks

### Supported Providers

- **Anthropic**: Claude models (Opus, Sonnet, Haiku)
- **OpenAI**: GPT-4, GPT-4 Turbo, o1, o3
- **Google**: Gemini Pro, Gemini Flash
- **Open Source**: Llama, Mixtral, DeepSeek
- **Self-hosted**: Ollama, vLLM, LocalAI
- **And 100+ more…**

## Configuration

### Environment Variables

```bash
# LiteLLM Model Selection (choose your preferred provider)
LLM_MODEL=gpt-4o                    # OpenAI
# LLM_MODEL=claude-3-5-sonnet-20241022  # Anthropic
# LLM_MODEL=gemini/gemini-pro        # Google
# LLM_MODEL=ollama/llama2            # Local Ollama

# Provider API Keys (configure based on your choice)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# LangSmith (Optional - for observability)
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=devops-sre-agent
```

### LiteLLM Configuration

```python
import litellm

# Simple usage - LiteLLM handles provider routing
response = litellm.completion(
    model="gpt-4o",  # or claude-3-5-sonnet, gemini-pro, etc.
    messages=[{"role": "user", "content": "Analyze this pod crash..."}],
    temperature=0.1  # Lower temperature for consistent troubleshooting
)
```

### Model Selection Guide

Different models excel at different tasks:

|Task Type                  |Recommended Characteristics|Example Models                     |
|---------------------------|---------------------------|-----------------------------------|
|Real-time troubleshooting  |Fast, cost-effective       |GPT-4o, Claude Sonnet, Gemini Flash|
|Complex root cause analysis|Deep reasoning             |o1, Claude Opus, GPT-4 Turbo       |
|Routine automation         |Balanced cost/performance  |GPT-4o-mini, Claude Haiku          |
|Local/private deployment   |Self-hosted                |Llama 3, Mixtral, DeepSeek         |

### Fallback Configuration

Implement automatic fallback across models:

```python
import litellm

litellm.set_verbose = True

# Configure fallback models
litellm.fallback_models = [
    "gpt-4o",                      # Primary
    "claude-3-5-sonnet-20241022",  # Fallback 1
    "gemini/gemini-pro"            # Fallback 2
]

response = litellm.completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Debug this issue..."}],
    fallbacks=litellm.fallback_models
)
```

## Key Features Powered by AI Reasoning

### 1. Intelligent Alert Triage

The AI analyzes incoming alerts and:

- Determines severity and urgency
- Identifies related alerts (noise reduction)
- Suggests immediate mitigation steps
- Routes to appropriate on-call engineer

### 2. Autonomous Root Cause Analysis

The AI orchestrates investigation across:

- Metrics (Grafana): Performance degradation patterns
- Logs (Kubernetes): Error messages and stack traces
- Knowledge base (Stack Overflow): Known issues and solutions
- Change history (GitHub): Recent deployments or config changes

### 3. Incident Documentation

The AI automatically:

- Generates incident timelines
- Creates postmortem templates
- Documents resolution steps
- Updates runbooks

### 4. Proactive Recommendations

The AI identifies:

- Resource optimization opportunities
- Potential reliability issues
- Security vulnerabilities
- Configuration drift

## Usage Examples

### Example 1: Pod Crash Investigation

```python
from devops_sre_agent import Agent

# Use any model via LiteLLM
agent = Agent(model="gpt-4o")  # or claude-3-5-sonnet, gemini-pro, etc.

result = agent.investigate(
    query="Pod 'payment-service-7d4f6b8c9-xyz' is crash-looping in production namespace",
    context={
        "cluster": "prod-us-west-2",
        "namespace": "production",
        "severity": "high"
    }
)

# AI orchestrates:
# 1. Query K8s for pod logs and events
# 2. Check Grafana for memory/CPU metrics
# 3. Search Stack Overflow for similar issues
# 4. Generate action plan
```

### Example 2: Alert Analysis

```python
alert = {
    "title": "High Error Rate - API Gateway",
    "severity": "critical",
    "metrics": {
        "error_rate": "15%",
        "p99_latency": "5000ms"
    }
}

result = agent.analyze_alert(alert)

# AI provides:
# - Root cause hypothesis
# - Recommended actions
# - Similar incidents
# - ServiceNow ticket draft
```

### Example 3: Capacity Planning

```python
result = agent.query(
    "Analyze resource utilization trends and recommend scaling strategy for Q1"
)

# AI analyzes:
# - Historical Grafana metrics
# - Growth patterns
# - Cost optimization opportunities
# - Scaling recommendations
```

### Example 4: Multi-Model Comparison

```python
# Compare different models for the same task
models = ["gpt-4o", "claude-3-5-sonnet-20241022", "gemini/gemini-pro"]

results = {}
for model in models:
    agent = Agent(model=model)
    results[model] = agent.investigate(query)
    
# Analyze which model performs best for your use case
```

## Best Practices

### 1. Temperature Settings

```python
# For deterministic troubleshooting
temperature = 0.1  

# For creative problem-solving
temperature = 0.7
```

### 2. System Prompts

Provide clear context about your infrastructure:

```python
system_prompt = """
You are a DevOps/SRE assistant for a microservices platform running on:
- Cloud: AWS
- Orchestration: Kubernetes (EKS)
- Monitoring: Grafana, Prometheus
- Services: 50+ microservices
- Traffic: 10K req/sec peak

Focus on production stability and follow incident response playbooks.
"""
```

### 3. Token Management

- Monitor token usage across different models
- Implement token tracking to manage API costs
- Cache common queries and responses
- Use cheaper models for routine tasks

### 4. Error Handling

```python
from litellm import exceptions as litellm_exceptions

try:
    result = agent.investigate(query)
except litellm_exceptions.RateLimitError as e:
    # Switch to fallback model
    logger.warning(f"Rate limit hit, switching to fallback: {e}")
except litellm_exceptions.APIError as e:
    # Escalate to human operator
    logger.error(f"AI API error: {e}")
```

## Observability with LangSmith

Track AI reasoning process across all models:

```python
from langsmith import trace

@trace
def investigate_incident(incident_id: str):
    # Automatically logged to LangSmith:
    # - Model used
    # - Input/output
    # - Token usage
    # - Latency
    # - Agent decisions
    return agent.investigate(incident_id)
```

View traces at: https://smith.langchain.com

## Cost Optimization

### Multi-Model Strategy

Use different models for different tasks:

```python
class OptimizedAgent:
    def __init__(self):
        self.fast_model = "gpt-4o-mini"      # Routine tasks
        self.balanced_model = "gpt-4o"       # Most incidents
        self.powerful_model = "o1"           # Critical issues
    
    def handle_incident(self, severity: str):
        if severity == "low":
            model = self.fast_model
        elif severity == "critical":
            model = self.powerful_model
        else:
            model = self.balanced_model
        
        return Agent(model=model)
```

### Cost Comparison (Approximate)

|Model Type                      |Cost Range         |Best For              |
|--------------------------------|-------------------|----------------------|
|Fast models (GPT-4o-mini, Haiku)|$0.01-0.05         |Routine operations    |
|Balanced models (GPT-4o, Sonnet)|$0.05-0.20         |Most incidents        |
|Reasoning models (o1, Opus)     |$0.20-1.00         |Complex analysis      |
|Local models (Ollama)           |Infrastructure only|Privacy-sensitive data|

### Tips to Reduce Costs

1. **Use cheaper models for routine tasks**: Reserve powerful models for critical incidents
1. **Implement caching**: Cache common queries and knowledge base lookups
1. **Optimize prompts**: Remove unnecessary context
1. **Batch operations**: Group related queries
1. **Set token limits**: Prevent runaway context
1. **Consider local models**: For high-volume, privacy-sensitive operations

## Security Considerations

### API Key Management

```bash
# Use environment variables or secrets manager
export OPENAI_API_KEY=$(aws secretsmanager get-secret-value \
    --secret-id prod/openai-api-key \
    --query SecretString \
    --output text)
```

### Data Privacy

- Review provider data retention policies
- Consider self-hosted models for sensitive data
- Use local models (Ollama, vLLM) for air-gapped environments

### Sensitive Data Handling

```python
# Redact sensitive information before sending to any LLM
def redact_sensitive_data(log: str) -> str:
    # Remove API keys, tokens, passwords
    log = re.sub(r'api[_-]?key["\s:=]+[\w-]+', '[REDACTED]', log)
    log = re.sub(r'password["\s:=]+[\w-]+', '[REDACTED]', log)
    return log
```

## Troubleshooting

### Common Issues

#### 1. Rate Limiting

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_llm(prompt, model="gpt-4o"):
    return litellm.completion(model=model, messages=[...])
```

#### 2. Context Window Exceeded

```python
# Different models have different context limits
# GPT-4o: 128k, Claude: 200k, Gemini: 1M+

def analyze_large_log(log_file: str, model: str):
    max_tokens = get_model_context_limit(model)
    chunks = split_into_chunks(log_file, max_tokens=max_tokens)
    results = [agent.analyze(chunk) for chunk in chunks]
    return agent.synthesize(results)
```

#### 3. Provider Outages

```python
# Automatic failover with LiteLLM
litellm.fallback_models = [
    "gpt-4o",
    "claude-3-5-sonnet-20241022",
    "gemini/gemini-pro",
    "ollama/llama2"  # Local fallback
]
```

## Advanced Features

### 1. Multi-Turn Conversations

```python
conversation = []
conversation.append({"role": "user", "content": "Pod is failing"})
response = agent.chat(conversation)
conversation.append({"role": "assistant", "content": response})
conversation.append({"role": "user", "content": "Check recent deployments"})
```

### 2. Function Calling / Tool Use

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_grafana",
            "description": "Query Grafana for metrics",
            "parameters": {...}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kubectl_logs",
            "description": "Get Kubernetes pod logs",
            "parameters": {...}
        }
    }
]

# LiteLLM automatically adapts tool format for each provider
response = litellm.completion(
    model="gpt-4o",  # Works with any tool-capable model
    messages=[...],
    tools=tools
)
```

### 3. Streaming Responses

```python
for chunk in litellm.completion(
    model="gpt-4o",
    messages=[...],
    stream=True
):
    print(chunk.choices[0].delta.content, end="")
```

### 4. Load Balancing Across Providers

```python
import litellm

# Configure load balancing
litellm.set_verbose = True

router = litellm.Router(
    model_list=[
        {"model_name": "gpt-4o", "litellm_params": {"model": "gpt-4o"}},
        {"model_name": "gpt-4o", "litellm_params": {"model": "azure/gpt-4o"}},
        {"model_name": "claude", "litellm_params": {"model": "claude-3-5-sonnet-20241022"}},
    ]
)

# Automatically distributes load
response = router.completion(model="gpt-4o", messages=[...])
```

## Self-Hosted / Local Models

### Using Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2

# Configure in your agent
export LLM_MODEL=ollama/llama2
```

```python
# Use in code
agent = Agent(model="ollama/llama2")
```

### Using vLLM

```bash
# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-70b-chat-hf \
    --port 8000

# Configure
export LLM_MODEL=openai/llama-2-70b
export OPENAI_API_BASE=http://localhost:8000/v1
```

## Resources

### LiteLLM Documentation

- [LiteLLM Docs](https://docs.litellm.ai)
- [Supported Models](https://docs.litellm.ai/docs/providers)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)

### Provider Documentation

- [OpenAI API](https://platform.openai.com/docs)
- [Anthropic Claude](https://docs.anthropic.com)
- [Google Gemini](https://ai.google.dev/docs)
- [Ollama](https://ollama.ai)

### Related Projects

- [LangGraph DeepAgent](https://github.com/langchain-ai/deepagents-quickstarts/)
- [LangSmith](https://docs.smith.langchain.com)

## License

This integration follows the same Apache-2.0 license as the parent project.
