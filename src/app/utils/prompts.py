from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

def get_job_description_prompt():
    system_template = "You are an HR assistant creating professional job descriptions."
    human_template = """Generate a detailed job description using the following information:
    Job Title: {title}
    Company Info: {company_info}
    Required Tools: {required_tools}
    Company Culture: {company_culture}"""

    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])