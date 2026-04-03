from wdatabricks import QueryBuilder


def main():
    query = QueryBuilder().select("*").from_table("users").where("id = 1").build()
    print(query)


if __name__ == "__main__":
    main()
