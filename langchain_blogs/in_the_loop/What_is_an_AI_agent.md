# What is an AI agent?

Original URL: https://blog.langchain.dev/what-is-an-agent/


![What is an AI agent?](/content/images/size/w760/format/webp/2024/06/What-is-an-agent---with-title.png)

# What is an AI agent?

Introducing a new series of musings on AI agents, called "In the Loop".

[Harrison Chase](/tag/harrison-chase/)
4 min read
Jun 28, 2024



*“What is an agent?”*

I get asked this question almost daily. At LangChain, we build tools to help developers build LLM applications, especially those that act as a reasoning engines and interact with external sources of data and computation. This includes systems that are commonly referred to as “agents”.

Everyone seems to have a slightly different definition of what an AI agent is. My definition is perhaps more technical than most:

💡An AI agent is a system that uses an LLM to decide the control flow of an application.

Even here, I’ll admit that my definition is not perfect. People often think of agents as advanced, autonomous, and human-like — but what about a simple system where an LLM routes between two different paths? This fits my technical definition, but not the common perception of what an agent should be capable of. It’s hard to define *exactly* what an agent is!

That’s why I really liked Andrew Ng’s [tweet last week](https://x.com/AndrewYNg/status/1801295202788983136?ref=blog.langchain.dev). In it he suggests that “rather than arguing over which work to include or exclude as being a true AI agent, we can acknowledge that there are different degrees to which systems can be agentic.” Just like autonomous vehicles, for example, have levels of autonomy, we can also view AI agent capabilities as a spectrum. I really agree with this viewpoint and I think Andrew expressed it nicely. In the future, when I get asked about what an agent is, I will instead turn the conversation to discuss what it means to be “agentic”.

## What does it mean to be agentic?

I gave a TED talk last year about LLM systems and used the slide below to talk about the different levels of autonomy present in LLM applications.

![](https://blog.langchain.dev/content/images/2024/06/Screenshot-2024-06-28-at-7.33.10-PM.png)

A system is more “agentic” the more an LLM decides how the system can behave.

Using an LLM to route inputs into a particular downstream workflow has some small amount of “agentic” behavior. This would fall into the `Router` category in the above diagram.

If you do use multiple LLMs to do multiple routing steps? This would be somewhere between `Router` and `State Machine`.

If one of those steps is then determining whether to continue or finish - effectively allowing the system to run in a loop until finished? That would fall into `State Machine`.

If the system is building tools, remembering those, and then taking those in future steps? That is similar to what the [Voyager paper](https://arxiv.org/abs/2305.16291?ref=blog.langchain.dev) implemented, and is incredibly agentic, falling into the higher `Autonomous Agent` category.

These definitions of “agentic” are still pretty technical. I prefer the more technical definition of “agentic” because I think it’s useful when designing and describing LLM systems.

## Why is “agentic” a helpful concept?

As with all concepts, it’s worth asking why we even need the concept of “agentic”. What does it help with?

Having an idea of how agentic your system can guide your decision-making during the development process - including building it, running it, interacting with it, evaluating it, and even monitoring it.

The more agentic your system is, the more an orchestration framework will help. If you are designing a complex agentic system, having a framework with the right abstractions for thinking about these concepts can enable faster development. This framework should have first-class support for branching logic and cycles.

The more agentic your system is, the harder it is to run. It will be more and more complex, having some tasks that will take a long time to complete. This means you will want to run jobs as background runs. This also means you want durable execution to handle any errors that occur halfway through.

The more agentic your system is, the more you will want to interact with it while it’s running. You’ll want the ability to observe what is going on inside, since the exact steps taken may not be known ahead of time. You’ll want the ability to modify the state or instructions of the agent at a particular point in time, to nudge it back on track if it’s deviating from the intended path.

The more agentic your system is, the more you will want an evaluation framework built for these types of applications. You’ll want to run evals multiple times, since there is compounding amount of randomness. You’ll want the ability to test not only the final output but also the intermediate steps to test how efficient the agent is behaving.

The more agentic your system is, the more you will want a new type of monitoring framework. You’ll want the ability to drill down into all the steps an agent takes. You’ll also want the ability to query for runs based on steps an agent takes.

Understanding and leveraging the spectrum of agentic capabilities in your system can improve the efficiency and robustness of your development process.

## Agentic is new

One thing that I often think about is what is *actually new* in all this craze. Do we need new tooling and new infrastructure for the LLM applications people are building? Or will generic tools and infrastructure from pre-LLM days suffice?

To me, the more agentic your application is, the more critical it is to have new tooling and infrastructure. That’s exactly what motivated us to build [LangGraph](https://www.langchain.com/langgraph?ref=blog.langchain.dev), the agent orchestrator to help with building, running, and interacting with agents, and [LangSmith](https://www.langchain.com/langsmith?ref=blog.langchain.dev), the testing and observability platform for LLM apps. As we move further on the agentic spectrum, the entire ecosystem of supportive tooling needs to be reimagined.


### Tags

[Harrison Chase](/tag/harrison-chase/)[In the Loop](/tag/in-the-loop/)

### Join our newsletter

Updates from the LangChain team and community

Enter your email

Subscribe

Processing your application...

Success! Please check your inbox and click the link to confirm your subscription.

Sorry, something went wrong. Please try again.




### You might also like

[![How to think about agent frameworks](/content/images/size/w760/format/webp/2025/04/Screenshot-2025-04-20-at-10.19.41-AM.png)](/how-to-think-about-agent-frameworks/)
[## How to think about agent frameworks](/how-to-think-about-agent-frameworks/)
[In the Loop](/tag/in-the-loop/)
20 min read



[![How do I speed up my AI agent?](/content/images/size/w760/format/webp/2025/03/openart-image_zkfUurHZ_1742063594759_raw.jpg)](/how-do-i-speed-up-my-agent/)
[## How do I speed up my AI agent?](/how-do-i-speed-up-my-agent/)
[In the Loop](/tag/in-the-loop/)
4 min read



[![MCP: Flash in the Pan or Future Standard?](https://images.unsplash.com/photo-1620662736427-b8a198f52a4d?crop=entropy&cs=tinysrgb&fit=max&fm=webp&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDd8fGRlYmF0ZXxlbnwwfHx8fDE3NDEzNzcwMzZ8MA&ixlib=rb-4.0.3&q=80&w=760)](/mcp-fad-or-fixture/)
[## MCP: Flash in the Pan or Future Standard?](/mcp-fad-or-fixture/)
[In the Loop](/tag/in-the-loop/)
5 min read



[![Introducing Interrupt: The AI Agent Conference by LangChain](/content/images/size/w760/format/webp/2025/02/blog--1-.png)](/introducing-interrupt-langchain-conference/)
[## Introducing Interrupt: The AI Agent Conference by LangChain](/introducing-interrupt-langchain-conference/)
[Harrison Chase](/tag/harrison-chase/)
2 min read



[![Communication is all you need](/content/images/size/w760/format/webp/2024/10/https___replicate.delivery_yhqm_48NVpCrAS8pfVaHsDqTEoZnFJj390IVQsmrJDfn18A6s4eUnA_out-0.webp)](/communication-is-all-you-need/)
[## Communication is all you need](/communication-is-all-you-need/)
[In the Loop](/tag/in-the-loop/)
7 min read



[![LangChain's Second Birthday](/content/images/size/w760/format/webp/2024/10/Frame-5.png)](/langchain-second-birthday/)
[## LangChain's Second Birthday](/langchain-second-birthday/)
[Harrison Chase](/tag/harrison-chase/)
6 min read






