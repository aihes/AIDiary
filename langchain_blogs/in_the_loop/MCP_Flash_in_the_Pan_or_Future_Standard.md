# MCP: Flash in the Pan or Future Standard?

Original URL: https://blog.langchain.dev/mcp-fad-or-fixture/


![MCP: Flash in the Pan or Future Standard?](https://images.unsplash.com/photo-1620662736427-b8a198f52a4d?crop=entropy&cs=tinysrgb&fit=max&fm=webp&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDd8fGRlYmF0ZXxlbnwwfHx8fDE3NDEzNzcwMzZ8MA&ixlib=rb-4.0.3&q=80&w=760)

# MCP: Flash in the Pan or Future Standard?

[In the Loop](/tag/in-the-loop/)
5 min read
Mar 8, 2025



*Model Context Protocol (MCP) is creating quite the stir on Twitter – but is it actually useful, or just noise? In this back and forth, Harrison Chase (LangChain CEO) and Nuno Campos (LangGraph Lead) debate whether MCP lives up to the hype.*

***Harrison:*** I’ll take the position that MCP is actually useful. I was skeptical on it at first, but I’ve begun to see its value. Essentially: **MCP is useful when you want to bring tools to an agent you don’t control.** 

Let me give an example. For Claude Desktop, Cursor, Windsurf - as a user, I don’t control the underlying agent. That agent has access to a few built-in tools.

But what if I want to give it access to a tool that it doesn’t have by default? In order to do that, there needs to be some protocol that exists – otherwise how would it know how to call the tool?

I believe this will be useful for non-developers to create agents as well. One of the trends we are seeing is the people want to make agent building accessible to subject matter experts, regardless of their technical expertise. I think these builders will rarely want to (or be able to) edit the agent logic itself - but they will want to give it access to certain tools. MCP will be useful here.

***Nuno:*** I think you’re underestimating the degree to which the rest of the agent needs to be tailored to the tools you give it access to. Sure, if Windsurf (god forbid) ships with a crappy web search tool and you want to replace it with a good one, that will work. But that’s not a real use case.

The compelling use case – the one where you give Cursor new capabilities even its creators didn’t dream of by just injecting your one magical tool – won’t actually work most of the time in practice. In pretty much all production agents I’ve seen, you need to tailor the system message and even other parts of the architecture to the tools you make available.

***Harrison:*** Well, these agents might not be 99% reliable... but they can probably still be good enough to be useful? Tool descriptions and instructions definitely matter! But we also know:

1. MCP has tool definitions - and the good MCP servers will probably have better tool descriptions than you would write quickly.
2. MCP allows for prompts - so you can include instructions.
3. The off-the-shelf tool calling agent will get way better as the underlying models get better.

I don’t think anyone is going to build the next Cursor based solely on MCP integrations and a tool calling agent, but surely there is some value there? Internal or personal agents, for example.

***Nuno:*** Well, our own tool calling benchmarks show that current models fail to call the right tool about half the time – and this is in agents with architecture and prompts tailor-made for that exact set of tools. Even a personal agent that fails half the time is not terribly useful…

And yes, models will get better – but so will user’s expectations. Don’t take my word for it, take it from Bezos: “One thing I love about ***customers*** is that they are divinely discontent. Their ***expectations*** are never static – they go up. It's human nature.”

If you own the entire stack – UI, prompts, architecture, tools – you can actually deliver on those expectations. Otherwise, good luck.

***Harrison:*** Models will continue to get better - I’m comfortable betting on that. So whatever the success rate of agents now, it will only go up.

I don’t think the right comparison is comparing an agent I could build with MCP to a polished agent with those tools. I think real value will come in the long tail of connections and integrations I want to make.

Like Zapier, it’s about connecting email to Google Sheets, Slack, etc. There’s an infinite number of workflows I could create, and there likely won’t be a polished agent for each one of them. With MCP, I can create my own versions of them.

What do you think of the Zapier analogy?

***Nuno:*** At LangChain, we’ve had a library of 500 tools for two years, and I haven’t seen them used often in production. They were all implemented to the same “protocol”, compatible with any model, and swappable. So what’s the difference here – is it the amazing MCP form factor of having to run a million servers in my terminal locally and only being compatible with desktop apps? That doesn’t sound like a plus to me. Honestly, I do think Zapier is the upper bound on MCP potential.

***Harrison:*** I think the difference between LangChain tools and MCP tools is that MCP is not for developers of the agent. They are most useful when bringing tools to an agent you **can’t** develop.

To be clear - if I was writing an agent to do XYZ - there is zero chance I would use MCP. But I don’t think that is the target use case for MCP. MCP is bringing tools to an agent you don’t control. It also enables non-developers to bring tools to agents (while LangChain tools are developer focused). There are **many more non-developers** than developers.

As for the current MCP form factor? Yeah, it sucks. But its going to get better, right? I’m imagining a future state of MCP, where you one-click install MCP apps (no more running servers in terminal locally) and they're accessible on web apps. I would bet that is where MCP is headed.

What do you think MCP needs to change, and would that be enough to convince you they are useful?

***Nuno:*** Okay, so MCP needs to become more like OpenAI’s Custom GPTs, and that’s when the current hype will be justified. But Custom GPTs aren’t that popular either. So what gives – what was missing in GPTs that MCP has?

***Harrison:*** I mean, MCP is more like Plugins, which also didn’t succeed 🙂 I kind of forget the Plugin experience (not sure I ever used it) so any comparisons I make may be off. But I would argue:

* The ecosystem of MCP is far greater already than the ecosystem of plugins
* The models have gotten better and more capable of using these tools

***Nuno:*** Well, I don’t know if that the ecosystem is larger. Some [random directory](https://glama.ai/mcp/servers?ref=blog.langchain.dev) I found in 5 seconds lists 893 servers at the time of writing. I think you might be counting number of tweets in your timeline mentioning MCP instead of actual things built with it 🙂 But returning to your unanswered question, in my opinio, if MCP is ever to become more than a footnote in the history of AI, it needs to:

* **Become less complicated.** Why does a tool protocol need to also serve prompts and LLM completions?
* **Become easier to implement.** Why does a protocol to serve tools need to have two-way communication? Yes, I’ve read all the reasons they list, and no, sorry, receiving logs from the server is not a good enough reason.
* **Become usable on a server**. A stateless protocol is key for this – just because we’re building with LLMs doesn’t mean we should forget all the hard earned lessons of scaling stuff online. And once usable on a server, a number of other issues pop up, like auth (which isn’t easy to solve in a distributed way).
* **Make up for the quality hit** that comes from plugging in random tools into an agent that knows nothing about them.

***Harrison:*** You're probably right that I have some recency bias from my Twitter timeline. But there’s also a lot of skepticism on there as well!

So, let’s turn it back to them. Cast your vote at the Twitter poll below - is MCP a flash in the pan or future standard?

> ❓MCP - flash in the pan or future standard?  
>   
> Lots of buzz around MCP. [@hwchase17](https://twitter.com/hwchase17?ref_src=twsrc%5Etfw&ref=blog.langchain.dev) and [@nfcampos](https://twitter.com/nfcampos?ref_src=twsrc%5Etfw&ref=blog.langchain.dev) debate whether it's here for the long run. Covers:   
>   
> - use cases for MCP  
> - Comparison to OpenAI Plugins  
> - Limitations of MCP  
>   
> Read the debate: [https://t.co/n1ZDzMHRWe](https://t.co/n1ZDzMHRWe?ref=blog.langchain.dev)  
>   
> Vote below:
> 
> — LangChain (@LangChainAI) [March 8, 2025](https://twitter.com/LangChainAI/status/1898410721215750487?ref_src=twsrc%5Etfw&ref=blog.langchain.dev)



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



[![How do I speed up my AI agent?](/content/images/size/w760/format/webp/2025/03/openart-image_zkfUurHZ_1742063594759_raw.jpg)](/how-do-i-speed-up-my-agent/)
[## How do I speed up my AI agent?](/how-do-i-speed-up-my-agent/)
[In the Loop](/tag/in-the-loop/)
4 min read



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






