from django.conf import settings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.output_parsers import CommaSeparatedListOutputParser
from io import StringIO
import pandas as pd
import re
from blogify.models import CsvDataDetail, AIPrompt, CSVData, CSVDataTest
from django.forms.models import model_to_dict
from datetime import datetime
import csv


def get_your_prompts_data(user_id):
    prompt = get_user_ai_prompts(user_id)

    date_title_chain = []
    blog_data = []
    if prompt:
        if prompt.date_prompt:
            date_chain = get_model_chain(
                prompt.date_model_name,
                prompt.date_model_temperature,
                prompt.date_prompt,
                "list_every_days",
            )
            date_title_chain.append(date_chain)

        if prompt.title_prompt:
            title_chain = get_model_chain(
                prompt.title_model_name,
                prompt.title_model_temperature,
                prompt.title_prompt,
                "list_date_title",
            )
            date_title_chain.append(title_chain)

        if date_title_chain:
            output_parser = CommaSeparatedListOutputParser()
            format_instructions = "Please respond in a two column table date in column 1 post title column 2"
            property_test_data = get_test_data()
            template_text = (
                prompt.title_prompt + prompt.date_prompt + "\n {format_instructions}"
            )
            prompt_inputs = re.findall(r"\{.*?\}", template_text)
            prompt_inputs = [
                prompt_input.replace("{", "").replace("}", "")
                for prompt_input in prompt_inputs
            ]
            # print(property_test_data)
            seq_chain = SequentialChain(
                chains=date_title_chain,
                input_variables=prompt_inputs,
                output_variables=["list_every_days", "list_date_title"],
                verbose=True,
            )
            current_month_year = datetime.now().strftime("%B %Y")
            property_test_data["date"] = current_month_year
            property_test_data["format_instructions"] = format_instructions
            # print(current_month_year)
            response = seq_chain(property_test_data)

            if "list_date_title" in response:
                output = StringIO(response["list_date_title"])
                df = pd.read_csv(output, sep="|")
                df.columns = df.columns.str.strip()
                df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
                df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
                df = df[
                    ~df.apply(
                        lambda row: row.astype(str).str.contains("---").any(), axis=1
                    )
                ]
                output_list = df.values.tolist()

            if prompt.blog_prompt:
                for title in output_list:
                    property_test_data["post_title"] = title[1]
                    property_test_data[
                        "format_instructions"
                    ] = "Please respond with a Table in markdown format that Includes:media,post,account, account type as account_type,publish at as publish_at,type "

                    blog_chain = get_model_chain(
                        prompt.blog_model_name,
                        prompt.blog_model_temperature,
                        prompt.blog_prompt,
                        "blog_post",
                    )
                    result = blog_chain(property_test_data)
                    if "blog_post" in result:
                        # result_output = get_blog_chain_output_process(result)
                        blog_data.append(
                            {"title": title[1], "post": result["blog_post"]}
                        )
                        print(result)
                        break

                print(blog_data)

    return blog_data


def get_user_ai_prompts(user_id):
    prompt = []
    if user_id != 0:
        prompt = AIPrompt.objects.filter(user_id=user_id).first()

    if not prompt:
        prompt = AIPrompt.objects.filter(user_id=None).first()

    # print(prompt)
    return prompt


def get_test_data():
    csvdatatest = CSVDataTest.objects.first()
    # Convert the model instance to a dictionary
    dict_csvdatatest = model_to_dict(csvdatatest)
    return dict_csvdatatest


def get_model_chain(
    model_name_text, temperature_text: 0.0, template_text, output_key_text
):
    template_text = template_text + "\n {format_instructions}"
    prompt_inputs = re.findall(r"\{.*?\}", template_text)
    prompt_inputs = [
        prompt_input.replace("{", "").replace("}", "") for prompt_input in prompt_inputs
    ]
    llm = ChatOpenAI(model_name=model_name_text, temperature=temperature_text)
    prompt = PromptTemplate(
        input_variables=prompt_inputs,
        template=template_text,
    )

    chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key_text)

    return chain


def get_blog_chain_output_process(result):
    return []


def generate_blog_property(property, user_id, blog_month_text, id):
    property["date"] = blog_month_text
    prompt = get_user_ai_prompts(user_id)
    date_title_chain = []
    blog_data = []
    if prompt:
        if prompt.date_prompt:
            date_chain = get_model_chain(
                prompt.date_model_name,
                prompt.date_model_temperature,
                prompt.date_prompt,
                "list_every_days",
            )
            date_title_chain.append(date_chain)

        if prompt.title_prompt:
            title_chain = get_model_chain(
                prompt.title_model_name,
                prompt.title_model_temperature,
                prompt.title_prompt,
                "list_date_title",
            )
            date_title_chain.append(title_chain)

        if date_title_chain:
            output_parser = CommaSeparatedListOutputParser()
            format_instructions = "Please respond in a two column table date in column 1 post title column 2"
            property_test_data = get_test_data()
            template_text = (
                prompt.title_prompt + prompt.date_prompt + "\n {format_instructions}"
            )
            prompt_inputs = re.findall(r"\{.*?\}", template_text)
            prompt_inputs = [
                prompt_input.replace("{", "").replace("}", "")
                for prompt_input in prompt_inputs
            ]
            # print(property_test_data)
            seq_chain = SequentialChain(
                chains=date_title_chain,
                input_variables=prompt_inputs,
                output_variables=["list_every_days", "list_date_title"],
                verbose=True,
            )
            current_month_year = datetime.now().strftime("%B %Y")
            property_test_data["date"] = current_month_year
            property_test_data["format_instructions"] = format_instructions
            # print(current_month_year)
            response = seq_chain(property_test_data)

            if "list_date_title" in response:
                output = StringIO(response["list_date_title"])
                df = pd.read_csv(output, sep="|")
                df.columns = df.columns.str.strip()
                df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
                df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
                df = df[
                    ~df.apply(
                        lambda row: row.astype(str).str.contains("---").any(), axis=1
                    )
                ]
                output_list = df.values.tolist()

            if prompt.blog_prompt:
                for title in output_list:
                    property_test_data["post_title"] = title[1]
                    property_test_data[
                        "format_instructions"
                    ] = "Please respond with a Table in markdown format that Includes:media,post,account, account type as account_type,publish at as publish_at,type "

                    blog_chain = get_model_chain(
                        prompt.blog_model_name,
                        prompt.blog_model_temperature,
                        prompt.blog_prompt,
                        "blog_post",
                    )
                    result = blog_chain(property_test_data)
                    if "blog_post" in result:
                        # result_output = get_blog_chain_output_process(result)
                        blog_data.append(
                            {"title": title[1], "post": result["blog_post"]}
                        )
                        print(result)
                        break

                print(blog_data)

    return blog_data
