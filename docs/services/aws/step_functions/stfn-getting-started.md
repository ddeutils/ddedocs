# Getting Started

## Orchestration

[Invoke AWS Step Functions from other services](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-invoke-sfn.html)

### Scheduler

**Amazon EventBridge Scheduler**

:   To solve this challenge, you can run a serverless workflow on a time-based schedule.
    **Amazon EventBridge** is a serverless event bus that helps you receive, filter, transform,
    route, and deliver events from AWS services, your own applications, and
    software-as-a-service (SaaS) applications. Many AWS services generate events that
    EventBridge receives. **Amazon EventBridge Scheduler** is a serverless scheduler that
    allows you to create, run, and manage tasks at scale from one central, managed service.
    With **AWS Step Functions**, you can define state machines that describe your workflow
    as a series of steps, their relationships, and their inputs and outputs.

    [Schedule a Serverless Workflow with AWS Step Functions and Amazon EventBridge Scheduler](https://aws.amazon.com/tutorials/scheduling-a-serverless-workflow-step-functions-amazon-eventbridge-scheduler/)
