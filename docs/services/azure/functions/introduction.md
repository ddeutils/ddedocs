# Azure Function

Azure Functions is a serverless compute service offered by Microsoft Azure,
designed to simplify the development of event-driven applications.
With Azure Functions, developers can write and deploy code without managing
the underlying infrastructure.
This allows for a more efficient development process, where developers
can focus on writing code that responds to events or triggers.

## Triggers vs Bindings

Azure Functions are event-driven functions triggered by specific events, known
as triggers.
Each function can have only one trigger, which defines the event source that
initiates the function’s execution.
When a trigger event occurs, Azure Functions automatically invokes the associated
function. Here are some common types of triggers that it offers:

- HTTP Trigger: Initiates function execution in response to HTTP requests, acts as an endpoint for a REST API.
- Timer Trigger: Executes functions on a predefined schedule or at specific intervals.
- Blob Trigger: Triggers function execution when new data is added to Azure Blob Storage.
- Queue Trigger: Starts function execution when a new message is added to an Azure Queue Storage queue.
- Event Grid Trigger: Fires when an event is published to an Azure Event Grid topic or domain.
- Cosmos DB Trigger: Initiates function execution when documents are added or modified in Azure Cosmos DB.

Bindings define the input and output connections between a function and external
resources. They provide a declarative way to integrate functions with data sources
and services without writing additional code for connectivity. Bindings abstract
away the complexities of interacting with external resources, simplifying
function development and enhancing productivity.

Some frequently used bindings:

- Blob Storage Binding: Allows functions to read from and write to Azure Blob Storage.
- Queue Storage Binding: Enables functions to interact with Azure Queue Storage queues.
- Table Storage Binding: Facilitates interactions with Azure Table Storage tables.
- Cosmos DB Binding: Provides integration with Azure Cosmos DB, allowing functions to read from and write to databases.
- Service Bus Binding: Allows functions to send and receive messages from Azure Service Bus queues or topics.
- HTTP Binding: Enables functions to make HTTP requests to external resources.

## How Costs are Calculated?

This pay-as-you-go approach contrasts with traditional hosting plans,
eliminating the need for fixed monthly payments.
It offers several hosting plans to suit different workloads and performance requirements:

- Consumption Plan: This is the default and most cost-effective option.
  With the Consumption plan, you only pay for the resources consumed during the
  execution of your functions.
  It automatically scales out to handle incoming events and scales back down when
  the workload decreases.
- Premium Plan: The Premium plan offers additional features and more predictable
  performance compared to the Consumption plan.
  It provides more advanced scaling options, larger instance sizes, and longer
  execution timeouts.
- App Service Plan: Azure Functions can also run on an App Service plan, which
  is shared with other Azure services like Web Apps and API Apps.
  This plan offers more control over the underlying infrastructure and is suitable
  for scenarios where you need more customization or have existing resources
  in an App Service environment.

## References

- [Azure Functions 101: Getting Started with Serverless Computing⚡](https://python.plainenglish.io/azure-functions-101-getting-started-with-serverless-computing-76669f4ce6c2)
