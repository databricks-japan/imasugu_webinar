# Databricks notebook source
# MAGIC %md 
# MAGIC このノートブックの目的は、QA Botアクセラレータを構成するノートブックを制御するさまざまな設定値を設定することです。<br>
# MAGIC オリジナルコンテンツは https://github.com/databricks-industry-solutions/diy-llm-qa-bot から利用できます。
# MAGIC
# MAGIC クラスターは、DBR13.2ML 以降をご利用ください。

# COMMAND ----------

# MAGIC %md ## イントロダクション
# MAGIC
# MAGIC このソリューションアクセラレータのゴールは、特定のドメインや問題領域に特化した質問応答を可能とするインタラクティブなアプリケーションを作成するために、自分のデータと組み合わせてどのように大規模言語モデルを活用できるのかを説明することです。この背後にあるコアなパターンは、モデルに対する質問に回答するのに適切なコンテキストを提供するドキュメントやドキュメントの断片と質問を提供するというものです。そして、モデルは質問とコンテキストの両方を考慮した回答を出力します。
# MAGIC </p>
# MAGIC
# MAGIC <img src='https://sajpstorage.blob.core.windows.net/maruyama/webinar/llm/qabot-image1.png' width=1000>
# MAGIC
# MAGIC </p>
# MAGIC Q&Aチャットbotのようなアプリケーションを構築するには、提供したいドメインに適した一連のドキュメントを必要とします。与えられたユーザーの質問の高速検索を可能とするインデックスが必要となります。そして、プロンプトを生成するために質問とドキュメントを組み合わせ、レスポンスを生成するためにモデルにプロンプトを送信するコアのアプリケーションを構築する必要があります。最後に、さまざまなデプロイメントオプションを可能にするために、インデックスが付与されたドキュメントとコアアプリケーションコンポーネントをマイクロサービスとしてパッケージする必要があります。
# MAGIC
# MAGIC 以下の3つのノートブックを通じてこれら3つのステップに取り組みます:</p>
# MAGIC
# MAGIC * 01: Build Document Index(ドキュメントのインデックスの構築)
# MAGIC * 02: Assemble Application(アプリケーションの構築)
# MAGIC * 03: Deploy Application(アプリケーションのデプロイ)
# MAGIC
# MAGIC 本ノートブックでは、オリジナルにある Evaluationは省略しております。 Evaluationも試したい方はオリジナルノートブックをご覧ください。
# MAGIC </p>

# COMMAND ----------

# MAGIC %md # 初期設定
# MAGIC
# MAGIC こちらのノートブックを開き、必要な情報を初期設定ください。<br>
# MAGIC <a href="$./util/notebook-config">./util/notebook-config</a>

# COMMAND ----------

# MAGIC %md 
# MAGIC このアクセラレータを通じて使用するパスを初期化します。

# COMMAND ----------

# MAGIC %run "./util/notebook-config"

# COMMAND ----------

config['vector_store_path'][5:]

# COMMAND ----------

dbutils.fs.rm(config['vector_store_path'][5:], True)

# COMMAND ----------

# MAGIC %md © 2023 Databricks, Inc. All rights reserved. The source in this notebook is provided subject to the Databricks License. All included or referenced third party libraries are subject to the licenses set forth below.
# MAGIC
# MAGIC | library                                | description             | license    | source                                              |
# MAGIC |----------------------------------------|-------------------------|------------|-----------------------------------------------------|
# MAGIC | langchain | Building applications with LLMs through composability | MIT  |   https://pypi.org/project/langchain/ |
# MAGIC | tiktoken | Fast BPE tokeniser for use with OpenAI's models | MIT  |   https://pypi.org/project/tiktoken/ |
# MAGIC | faiss-cpu | Library for efficient similarity search and clustering of dense vectors | MIT  |   https://pypi.org/project/faiss-cpu/ |
# MAGIC | openai | Building applications with LLMs through composability | MIT  |   https://pypi.org/project/openai/ |
