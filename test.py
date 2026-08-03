from neo4j import GraphDatabase, Result
import pandas as pd

URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "TesteDesktop")

#se conecta com o banco de dados e quando estiver fora desse bloco o with garante que o driver feche
with GraphDatabase.driver(URI, auth=AUTH) as driver:

    cypher = """
    MATCH (p:Person {name: $name})-[r:IS_DATING]->(m:Person)
    RETURN p.name AS name1, m.name AS name2
    """
    name = "Gustavo"
    
    records, summary, keys = driver.execute_query(
        cypher,    
        name=name
    )
    # records é uma lista com todas as linhas retornadas, onde cada elemento dessa lista é um dicionário
    # que pode ser usado através das keys retornadas.
    for record in records:
        print(record["name1"])  
        print(record["name2"])  


    # pode se fazer usando esse metodo result_transformer, para retorna de uma maneira diferente
    result = driver.execute_query(
        cypher,
        name=name,
        result_transformer_= lambda result: [
            f"{record['name1']} is dating {record['name2']}"
            for record in result
        ]
    )
    
    print(result)

    # baixar panda para pode vizualizar o data frame
    df = driver.execute_query(
        cypher,
        name=name,
        result_transformer_=Result.to_df,
    )

    print(df)


