# What is a "cognitive architecture"?

Original URL: https://blog.langchain.dev/what-is-a-cognitive-architecture/


![What is a "cognitive architecture"?](/content/images/size/w760/format/webp/2024/07/What-is-an-agent.png)

# What is a "cognitive architecture"?

The second installment in our "In the Loop" series, focusing on what cognitive architecture means.

[Harrison Chase](/tag/harrison-chase/)
3 min read
Jul 5, 2024



***Update: Several readers have pointed out that the term "cognitive architecture" has a*** [***rich history***](https://en.wikipedia.org/wiki/Cognitive_architecture?ref=blog.langchain.dev) ***in neuroscience and computational cognitive science. Per Wikipedia, "a cognitive architecture refers to both a theory about the structure of the human mind and to a computational instantiation of such a theory". That definition (and corresponding research and articles on the topic) are more comprehensive than any definition I attempt to offer here, and this blog should instead be read as a mapping of my experience building and helping build LLM-powered applications over the past year to this area of research.***

One phrase I’ve used a lot over the past six months (and will likely use more) is “cognitive architecture”. It’s a term I first heard from [Flo Crivello](https://x.com/Altimor?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor&ref=blog.langchain.dev) - all credit for coming up with it goes to him, and I think it's a fantastic term. So what exactly do I mean by this?

What I mean by cognitive architecture is *how your system thinks —* in other words, the flow of code/prompts/LLM calls that takes user input and performs actions or generates a response.

I like the word “cognitive” because agentic systems rely on using an LLM to reason about what to do.

I like the word “architecture” because these agentic systems still involve a good amount of engineering similar to traditional system architecture.

## Mapping levels of autonomy to cognitive architectures

If we refer back to this slide (originally from [my TED Talk](https://www.ted.com/talks/harrison_chase_the_magical_ai_assistants_of_the_future_and_the_engineering_behind_them?ref=blog.langchain.dev)) on the different levels of autonomy in LLM applications, we can see examples of different cognitive architectures.

![](https://blog.langchain.dev/content/images/2024/07/Screenshot-2024-06-28-at-7.33.10-PM.png)

First is just code - everything is hard coded. Not even really a cognitive architecture.

Next is just a single LLM call. Some data preprocessing before and/or after, but a single LLM call makes up the majority of the application. Simple chatbots likely fall into this category.

Next is a chain of LLM calls. This sequence can be either breaking the problem down into different steps, or just serve different purposes. More complex RAG pipelines fall into this category: use a first LLM call to generate a search query, then a second LLM call to generate an answer.

After that, a router. Prior to this, you knew all the steps the application would take *ahead* of time. Now, you no longer do. The LLM decides which actions to take. This adds in a bit more randomness and unpredictability.

The next level is what I call a state machine. This is combining an LLM doing some routing with a loop. This is even more unpredictable, as by combining the router with a loop, the system could (in theory) invoke an unlimited number of LLM calls.

The final level of autonomy is the level I call an *agent*, or really an “autonomous agent”. With state machines, there are still constraints on which actions can be taken and what flows are executed after that action is taken. With autonomous agents, those guardrails are removed. The system itself starts to decide which steps are available to take and what the instructions are: this can be done by updating the prompts, tools, or code used to power the system.

## **Choosing a cognitive architecture**

When I talk about "choosing a cognitive architecture,” I mean choosing which of these architectures you want to adopt. None of these are strictly “better” than others - they all have their own purpose for different tasks.

When building LLM applications, you’ll probably want to experiment with different cognitive architectures just as frequently as you experiment with prompts. We’re building [LangChain](https://www.langchain.com/langchain?ref=blog.langchain.dev) and [LangGraph](https://www.langchain.com/langgraph?ref=blog.langchain.dev) to enable that. Most of our development efforts over the past year have gone into building low-level, highly controllable orchestration frameworks (LCEL and LangGraph).

This is a bit of a departure from early LangChain which focused on easy-to-use, off-the-shelf chains. These were great for getting started but tough to customize and experiment with. This was fine early on, as everyone was just trying to get started, but as the space matured, the design pretty quickly hit its limits.

I’m extremely proud of the changes we’ve made over the past year to make LangChain and LangGraph more flexible and customizable. If you’ve only ever used LangChain through the high level wrappers, check out the low-level bits. They are much more customizable, and will really let you control the cognitive architecture of your application.

*If you’re building straight-forward chains and retrieval flows, check out LangChain in* [*Python*](https://python.langchain.com/v0.2/docs/introduction/?ref=blog.langchain.dev) *and* [*JavaScript*](https://js.langchain.com/v0.2/docs/introduction/?ref=blog.langchain.dev)*. For more complex agentic workflows, try out LangGraph in* [*Python*](https://langchain-ai.github.io/langgraph/tutorials/introduction/?ref=blog.langchain.dev) *and* [*JavaScript*](https://langchain-ai.github.io/langgraphjs/tutorials/quickstart/?ref=blog.langchain.dev)*.*


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






