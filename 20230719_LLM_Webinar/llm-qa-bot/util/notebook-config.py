# Databricks notebook source
if 'config' not in locals():
  config = {}

# COMMAND ----------

# DBTITLE 1,ドキュメントパスの設定
# VectorDBを保存するパスを指定します。
config['vector_store_path'] = '/dbfs/tmp/qabot_ja/vector_store' 

# COMMAND ----------

# DBTITLE 1,カタログ＆データベースの作成
config['catalog_name'] = '<catalog>'
config['schema_name'] = 'qabot_ja'

# create catalog & database if not exists
_ = spark.sql(f"create catalog if not exists {config['catalog_name']}")
_ = spark.sql(f"use catalog {config['catalog_name']}")
_ = spark.sql(f"create schema if not exists {config['schema_name']}")

# set current datebase context
_ = spark.sql(f"use {config['catalog_name']}.{config['schema_name']}")

# COMMAND ----------

# DBTITLE 1,OpenAI APIトークンのための環境変数の設定
import os

# 実際に設定したシークレットのスコープとキーを指定します
os.environ['OPENAI_API_KEY'] = dbutils.secrets.get("<scope>", "<key>")  

# COMMAND ----------

# DBTITLE 1,mlflowの設定
import mlflow
# Model　Nameの指定
config['registered_model_name'] = 'databricks_llm_qabot_jpn' 

# 以下は設定不要です。
config['model_uri'] = f"models:/{config['registered_model_name']}/production"
username = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
_ = mlflow.set_experiment('/Users/{}/{}'.format(username, config['registered_model_name']))

# COMMAND ----------

# DBTITLE 1,OpenAIモデルの設定
# 適宜、プロンプトなど変更ください。このままでも動作します。

config['openai_embedding_model'] = 'text-embedding-ada-002'
config['openai_chat_model'] = "gpt-3.5-turbo"
config['system_message_template'] = """あなたはDatabricksによって開発された有能なアシスタントであり、指定されたコンテキストに基づいて質問に回答することを得意としており、コンテキストはドキュメントです。コンテキストが回答を決定するのに十分な情報を提供しない場合には、わかりませんと言ってください。コンテキストが質問に適していない場合にも、わかりませんと言ってください。問い合わせが完全な質問になっていない場合にも、わからないと言ってください。コンテキストから良い回答が得られた場合には、質問に回答するためにコンテキストを要約してください。"""
config['human_message_template'] = """指定されたコンテキスト: {context}。 質問に回答してください {question}."""
config['temperature'] = 0.15

# COMMAND ----------

# DBTITLE 1,デプロイメントの設定
# Model Serving Endpointに設定する情報です。
# Secret Scope / Key を変更ください。
config['openai_key_secret_scope'] = "<scope>" 
config['openai_key_secret_key'] = "<key>" 

# Model Serving Endpoint Nameを指定ください。
config['serving_endpoint_name'] = "llm-qabot-endpoint-jmaru-jpn" 
