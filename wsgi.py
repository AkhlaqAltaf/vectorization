# from src.sql_db.queries.populate_data import populate_data
from src.sql_db.queries.fetch_evaluation_data import fetch_phrases,fetch_sentences, fetch_paragraphs
from src.sql_db.queries.populate_data import PopulateData, create_all_one_time
from src.views import db
from src.views.test_server import app, test_vect_post


def test_to_use_sql():
    with app.app_context():
        create_all_one_time(db)
        populate_data = PopulateData(db)  # Call your function inside the app context
        populate_data.populate_data("./data_files/processed_data2.csv")


print("Starting the WSGI script")
if __name__ == '__main__':
    # test_to_use_sql()
    # with app.app_context():
    #    print(fetch_phrases())
    #    print(fetch_sentences())
    app.run(debug=True)
    # test_vect_post()




