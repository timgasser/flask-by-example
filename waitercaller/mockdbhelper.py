import datetime

# Dictionary to store the mock users.
# Use the email as the key to give constant time checking
MOCK_USERS = {'test@example.com':  {'salt': "8Fb23mMNHD5Zb8pr2qWA3PE9bH0=",
                                    'hashed': '50083816777376adf481b192a920c0de377f2f3e54ff20f67833b9fbb608d17816ff9247e83bccc5b57ca1896c88657e0287480415d04a5f55e910521a1c6962'}
             }

MOCK_TABLES = [{"_id": "1",
                "number": "1",
                "owner": "test@example.com",
                "url": "mockurl"}]

MOCK_REQUESTS = [{"_id": "1",
                  "table_number": "1",
                  "table_id": "1",
                  "time": datetime.datetime.now()}]

class MockDBHelper(object):

    def get_user(self, email):
        if email in MOCK_USERS:
            return MOCK_USERS[email]
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS[email] = {'salt': salt,
                             'hashed': hashed}

    def add_table(self, number, owner):
        MOCK_TABLES.append({"_id": str(number),
                            "number": number,
                            "owner": owner})
        return number
    
    def get_tables(self, owner_id):
        return MOCK_TABLES

    def get_table(self, table_id):
        for table in MOCK_TABLES:
            if table.get("_id") == table_id:
                return table

    def update_table(self, _id, url):
        for table in MOCK_TABLES:
            if table.get("_id") == _id:
                table["url"] = url
                break

    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
            if table['id'] == table_id:
                del MOCK_TABLES[i]
                break

    def add_request(self, table_id, time):
        table = self.get_table(table_id)
        MOCK_REQUESTS.append({"_id": table_id, 
                              "owner": table["owner"],
                              "table_number": table["number"],
                              "table_id": table_id,
                              "time": time})
        return True

    def get_requests(self, owner_id):
        return MOCK_REQUESTS

    def delete_request(self, request_id):
        for idx, request in enumerate(MOCK_REQUESTS):
            if request['_id'] == request_id:
                del MOCK_REQUESTS[idx]
                break
