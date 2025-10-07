using System;
using System.Collections;
using System.Collections.Generic;
using Azure;
using Azure.AI.OpenAI;
using Azure.Identity;

namespace BusinessAssistant.AgentFramework;

internal static class Program
{
    private static void Main()
    {
        var settings = LlmSettings.FromEnvironment();

        Console.WriteLine("🤖 LLM Configuration");
        Console.WriteLine($"   Provider: {settings.Provider}");
        Console.WriteLine($"   OpenAI Model: {settings.OpenAiModel}");
        Console.WriteLine($"   OpenAI API Key Set: {(!string.IsNullOrWhiteSpace(settings.OpenAiApiKey) ? "✓" : "✗")}");

        if (!string.IsNullOrWhiteSpace(settings.OpenAiEndpoint))
        {
            Console.WriteLine($"   OpenAI Endpoint: {settings.OpenAiEndpoint}");
        }

        if (!string.IsNullOrWhiteSpace(settings.AzureOpenAiEndpoint))
        {
            Console.WriteLine($"   Azure OpenAI Endpoint: {settings.AzureOpenAiEndpoint}");
        }

        if (!string.IsNullOrWhiteSpace(settings.AzureOpenAiApiKey))
        {
            Console.WriteLine($"   Azure OpenAI API Key Set: ✓");
        }

        if (!string.IsNullOrWhiteSpace(settings.AzureOpenAiDeployment))
        {
            Console.WriteLine($"   Azure OpenAI Deployment: {settings.AzureOpenAiDeployment}");
        }

        Console.WriteLine($"   Ollama Model: {settings.OllamaModel}");
        Console.WriteLine($"   Ollama URL: {settings.OllamaBaseUrl}");

        if (!string.IsNullOrWhiteSpace(settings.OllamaApiKey))
        {
            Console.WriteLine($"   Ollama API Key Set: ✓");
        }

        if (!string.IsNullOrWhiteSpace(settings.CustomHeadersDescription))
        {
            Console.WriteLine($"   Additional Headers: {settings.CustomHeadersDescription}");
        }

        var (client, clientMessage) = OpenAiClientFactory.TryCreate(settings);
        Console.WriteLine($"   OpenAI Client: {clientMessage}");

        if (client is not null)
        {
            Console.WriteLine("   Client is ready to invoke the quick start samples.");
        }
    }
}

internal sealed record LlmSettings(
    string Provider,
    string OpenAiModel,
    string? OpenAiApiKey,
    string? OpenAiEndpoint,
    string? AzureOpenAiEndpoint,
    string? AzureOpenAiApiKey,
    string? AzureOpenAiDeployment,
    string OllamaModel,
    string OllamaBaseUrl,
    string? OllamaApiKey,
    string? CustomHeadersDescription)
{
    private const string DefaultOpenAiModel = "gpt-4o-mini";
    private const string DefaultOllamaModel = "qwen";
    private const string DefaultOllamaUrl = "http://localhost:11434";
    private const string DefaultProvider = "openai";

    public static LlmSettings FromEnvironment()
    {
        var environment = Environment.GetEnvironmentVariables();

        string GetValue(string key, string? fallback = null)
        {
            if (environment.Contains(key) && environment[key] is string raw && !string.IsNullOrWhiteSpace(raw))
            {
                return raw.Trim();
            }

            return fallback ?? string.Empty;
        }

        static string? GetOptional(IDictionary environment, string key)
        {
            if (environment.Contains(key) && environment[key] is string raw && !string.IsNullOrWhiteSpace(raw))
            {
                return raw.Trim();
            }

            return null;
        }

        var provider = GetValue("LLM_PROVIDER", DefaultProvider);
        var openAiModel = GetValue("OPENAI_MODEL", DefaultOpenAiModel);
        var openAiApiKey = GetOptional(environment, "OPENAI_API_KEY");
        var openAiEndpoint = GetOptional(environment, "OPENAI_ENDPOINT") ?? GetOptional(environment, "OPENAI_BASE_URL");
        var azureOpenAiEndpoint = GetOptional(environment, "AZURE_OPENAI_ENDPOINT");
        var azureOpenAiApiKey = GetOptional(environment, "AZURE_OPENAI_API_KEY");
        var azureOpenAiDeployment = GetOptional(environment, "AZURE_OPENAI_DEPLOYMENT");
        var ollamaModel = GetValue("OLLAMA_MODEL", DefaultOllamaModel);
        var ollamaBaseUrl = GetValue("OLLAMA_BASE_URL", DefaultOllamaUrl);
        var ollamaApiKey = GetOptional(environment, "OLLAMA_API_KEY");
        var customHeadersDescription = BuildHeadersDescription(environment);

        return new LlmSettings(
            provider,
            openAiModel,
            openAiApiKey,
            openAiEndpoint,
            azureOpenAiEndpoint,
            azureOpenAiApiKey,
            azureOpenAiDeployment,
            ollamaModel,
            ollamaBaseUrl,
            ollamaApiKey,
            customHeadersDescription
        );
    }

    private static string? BuildHeadersDescription(IDictionary environment)
    {
        const string prefix = "LLM_HEADER_";
        var headers = new List<string>();

        foreach (DictionaryEntry entry in environment)
        {
            if (entry.Key is string key && key.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
            {
                headers.Add(key[prefix.Length..]);
            }
        }

        return headers.Count switch
        {
            0 => null,
            _ => string.Join(", ", headers)
        };
    }
}

internal static class OpenAiClientFactory
{
    public static (OpenAIClient? Client, string Message) TryCreate(LlmSettings settings)
    {
        try
        {
            if (!string.IsNullOrWhiteSpace(settings.AzureOpenAiEndpoint))
            {
                var endpoint = new Uri(settings.AzureOpenAiEndpoint);

                if (!string.IsNullOrWhiteSpace(settings.AzureOpenAiApiKey))
                {
                    var credential = new AzureKeyCredential(settings.AzureOpenAiApiKey);
                    var client = new OpenAIClient(endpoint, credential);
                    return (client, "initialized with Azure OpenAI API key");
                }

                var defaultCredential = new DefaultAzureCredential();
                var clientWithIdentity = new OpenAIClient(endpoint, defaultCredential);
                return (clientWithIdentity, "initialized with DefaultAzureCredential");
            }

            if (!string.IsNullOrWhiteSpace(settings.OpenAiApiKey))
            {
                var client = new OpenAIClient(settings.OpenAiApiKey);
                return (client, "initialized with OpenAI API key");
            }

            return (null, "no API credentials available");
        }
        catch (Exception ex)
        {
            return (null, $"failed to initialize client: {ex.Message}");
        }
    }
}
