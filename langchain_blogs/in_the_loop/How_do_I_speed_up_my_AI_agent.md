# How do I speed up my AI agent?

Original URL: https://blog.langchain.dev/how-do-i-speed-up-my-agent/


![How do I speed up my AI agent?](/content/images/size/w760/format/webp/2025/03/openart-image_zkfUurHZ_1742063594759_raw.jpg)

# How do I speed up my AI agent?

[In the Loop](/tag/in-the-loop/)
4 min read
Mar 15, 2025



I get this question a bunch. Developers generally first spend time getting the agent to work, but then they turn their attention to speed and cost. There are few things we see developers doing:

* Identifying where the latency is coming from
* Changing the UX to reduce the “perceived” latency
* Making fewer LLM calls
* Speeding up LLM calls
* Making LLM calls in parallel

## Identifying where the latency is coming from

This may sound basic, but how you approach reducing latency will depend entirely on your specific bottleneck. Is the latency coming from one big LLM call, or from multiple small ones that just add up? You’ll need to diagnose these before trying to speed it up.

[LangSmith](http://langchain.com/langsmith?ref=blog.langchain.dev) is an incredibly useful tool for this, providing complete visibility into your agent interactions. You can track the latency of each step of the agent, and we’ve also recently introduced a “waterfall” view to easily identify which steps contribute the most to overall latency.

## Changing the UX to reduce the “perceived” latency

Sometimes, the easiest way to reduce latency… is to not reduce latency.

While it might seem counterintuitive at first, but if we think about why latency matters — it often matters because people are concerned that if the agent takes too long to run, the user won’t like using it. This can often be solved by updating the UX of the agent. We see two main ways people do this.

* **Stream back results.** Streaming is pretty common place for most LLM applications, but if you aren’t doing it, you definitely should. It conveys to the user that the LLM is working, and they are less likely to leave the page.In addition to streaming response tokens, you can also stream things beyond just the final response. For example, you could stream the steps of the plan the agent is taking, the retrieval results, or the thinking tokens. [Perplexity does a fantastic job at this](https://www.langchain.com/breakoutagents/perplexity?ref=blog.langchain.dev) with their search interface. They’ve found that by making a UI change to show these intermediate steps, user satisfaction improved — despite the total completion time remaining unchanged.
* **Run agents in the background**. Have agents running in the background. For my email assistant, I don’t have visibility into how long the email agent takes. That’s because it is triggered by an event (an email) and I only get notified when it’s stuck. I hide **all** the latency from the user, and the agent just runs in the background.

## Making fewer LLM calls

Not everything needs to be an LLM call. If you can do things in a way other than making an LLM call - great! The agents we see being built are a combination of LLM calls and code. This hybrid approach of combining code with LLM calls is one of the guiding principles of LangGraph, and a core reason why [companies like Replit, Uber, LinkedIn and Klarna are adopting it](https://blog.langchain.dev/is-langgraph-used-in-production/).

A common path we see is “Single LLM call” → “ReAct Agent” → “Multi Agent” → “LangGraph”.

People start with a single LLM call. They run into some short comings, and step up to an agent. This works okay, but then they try to give it more tools and realize that a single agent can only support so many tools. They then go to a “multi-agent” setup, using a supervisor or swarm architecture.

The issue with this is that these architectures use a LOT of LLM calls. They are not super efficient in how the different agents communicate. That is by design - they are general purpose architectures, so they are not optimized for your use case.

That is when we see people reach for [LangGraph](http://langchain.com/langgraph?ref=blog.langchain.dev). LangGraph is low level, and allows you to specify exactly how these agents should communicate with each other (or when something is just an LLM call). Often times this leads to significantly less LLM calls, making the agent faster and cheaper (and often more reliable).

## Speeding up LLM calls

We generally see two ways developers have been speeding up LLM calls.

**Faster models**. Some models are faster than others. Google offers Gemini Flash which is very fast. OpenAI and Anthropic also have smaller, faster models. Open source model hosting platforms like Groq and Fireworks are constantly trying to make the best open source models faster and faster. Note: this often comes with a tradeoff of using **worse** models, as these faster models are usually smaller and thus less accurate.

**Less context.** The time an LLM takes to respond is proportional to the length of the input. In order to get faster results, you can pass less input! This is why you need to have **full control and visibility** over what **exactly** goes into each LLM call. Frameworks that obfuscate this (or don’t make it easy to control) are no good - that is why LangGraph comes with no hidden prompts — you have full control. If you are looking for a way to get better **visibility** into what is going into the LLM calls - check out LangSmith.

## Making LLM calls in parallel

Not applicable to all use cases, but if it is for your use case you should be doing this. LangGraph [supports parallelism](https://langchain-ai.github.io/langgraph/how-tos/branching/?ref=blog.langchain.dev) out of the box. Examples of where you can think about doing this:

* Doing a guardrail check and generation in parallel
* Doing extraction from multiple documents in parallel
* Calling multiple models in parallel and then combining the outputs

## Conclusion

Speeding up your AI agent is ultimately about making strategic tradeoffs between performance, cost, and capability. Start by first understanding your specific performance bottlenecks, then apply these techniques selectively based on your use case. And sometimes the most effective method isn't technical at all — but rather rethinking how users experience the interaction with your agent.

As you try out new strategies, we'd love to hear from you — what techniques have worked best for speeding up your agent? Drop us a line on [X](https://x.com/LangChainAI?ref=blog.langchain.dev) or [LinkedIn](https://www.linkedin.com/company/langchain/?ref=blog.langchain.dev).


### Tags

[In the Loop](/tag/in-the-loop/)

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



[![MCP: Flash in the Pan or Future Standard?](https://images.unsplash.com/photo-1620662736427-b8a198f52a4d?crop=entropy&cs=tinysrgb&fit=max&fm=webp&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDd8fGRlYmF0ZXxlbnwwfHx8fDE3NDEzNzcwMzZ8MA&ixlib=rb-4.0.3&q=80&w=760)](/mcp-fad-or-fixture/)
[## MCP: Flash in the Pan or Future Standard?](/mcp-fad-or-fixture/)
[In the Loop](/tag/in-the-loop/)
5 min read



[![Communication is all you need](/content/images/size/w760/format/webp/2024/10/https___replicate.delivery_yhqm_48NVpCrAS8pfVaHsDqTEoZnFJj390IVQsmrJDfn18A6s4eUnA_out-0.webp)](/communication-is-all-you-need/)
[## Communication is all you need](/communication-is-all-you-need/)
[In the Loop](/tag/in-the-loop/)
7 min read



[![Memory for agents](/content/images/size/w760/format/webp/2024/10/Screenshot-2024-10-19-at-9.59.50-AM.png)](/memory-for-agents/)
[## Memory for agents](/memory-for-agents/)
[In the Loop](/tag/in-the-loop/)
5 min read



[![UX for Agents, Part 3: Spreadsheet, Generative, and Collaborative UI/UX](/content/images/size/w760/format/webp/2024/08/UX-for-agents---spreadsheet---part-3.png)](/ux-for-agents-part-3/)
[## UX for Agents, Part 3: Spreadsheet, Generative, and Collaborative UI/UX](/ux-for-agents-part-3/)
[In the Loop](/tag/in-the-loop/)
4 min read



[![UX for Agents, Part 2: Ambient](/content/images/size/w760/format/webp/2024/08/UX-for-agents---ambient---part-2--1-.png)](/ux-for-agents-part-2-ambient/)
[## UX for Agents, Part 2: Ambient](/ux-for-agents-part-2-ambient/)
[In the Loop](/tag/in-the-loop/)
4 min read






