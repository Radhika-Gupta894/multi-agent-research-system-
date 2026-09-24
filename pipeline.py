from agent import build_reader_Agent, build_search_agent, writer_chain, critic_chain
import time

def run_research_pipeline(topic: str) -> dict:
    state = {}

    #search agent working 
    print("\n"+"="*50)
    print("Step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_agent_out = search_agent.invoke({
        "messages": [("user", f"Search the web for recent and reliable information and sources about: {topic}")]
    })
    urls = search_agent_out.get("output")

    state["search_results"] = search_agent_out['messages'][-1].content
    print("\n search result", state["search_results"])
    

    # step 2 
    print("\n"+"="*50)
    print("Step 2 - reader agent is scraping top resources..")
    print("="*50)

    reader_agent = build_reader_Agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
        f"Based on the following search results about '{topic}',"
        f"pick the most relevant URL and scrape it for deeper content. \n\n"
        f"Search Results: \n{state['search_results'][:800]}"
        
         )]
    })
    state["scraped_content"] = reader_result['messages'][-1].content
    print("\nscraped content: \n", state['scraped_content'])

    #step 3 - writer chain
    time.sleep(2)
    print("\n" + "="*50)
    print("Step 3 - writer agent is writing report...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']}\n\n"
        f"SCRAPED CONTENT: \n {state['scraped_content']}\n\n"
    )

    report = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    state["report"] = report
    print("\nResearch report: \n", state['report'])

    # step 4 - critic chain
    time.sleep(2)
    print("\n" + "="*50)
    print("Step 4 - critic agent is reviewing the report...")
    print("="*50)

    critic_result = critic_chain.invoke({
        "report": state['report']
    })
    state["critic_review"] = critic_result
    print("\nCritic Review: \n", state['critic_review'])

    return state

if __name__ == "__main__":
    topic = input("\nEnter your topic: ")
    run_research_pipeline(topic)

        